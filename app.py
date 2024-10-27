from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import json
from openai import OpenAI
import os
import base64
import requests
import shutil            
import logging
import webbrowser
from threading import Timer
import webview


print("Current working directory:", os.getcwd())

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

food_list_file = os.path.join(app.root_path, 'haul', 'haul.json')

@app.route('/response/<filename>')
def response(filename):
    return send_from_directory('response', filename)

@app.route('/')
def home():
    return render_template('CookAI.html')

@app.route('/kitchen')
def kitchen():
    return render_template('Kitchen — CookAI.html')

@app.route('/fridge')
def fridge():
    return render_template('Fridge — CookAI.html')
    
# ---
# Use the current working directory to store haul.json
current_working_dir = os.getcwd()
haul_directory = os.path.join(current_working_dir, 'haul')

# Ensure the directory exists
if not os.path.exists(haul_directory):
    os.makedirs(haul_directory)

# Define the path for haul.json
food_list_file = os.path.join(haul_directory, 'haul.json')
# ---

# Auto open the broswer here
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

@app.route('/login')
def login():
    return render_template('Login — CookAI.html')

@app.route('/profile')
def profile():
    return render_template('Profile — CookAI.html')

def validate_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        if "generated_text" in data:
            recipe_data = json.loads(data["generated_text"])
            if all(key in recipe_data for key in ["title", "serving_size", "ingredients", "instructions"]):
                return True
        return False
    except Exception as e:
        print(f"Validation error: {e}")
        return False

# Improved flatten_ingredients function with underscore handling
def flatten_ingredients(ingredients):
    if isinstance(ingredients, list):
        return [f"{item['ingredient'].replace('_', ' ')}: {item['measurement']}" for item in ingredients if 'ingredient' in item and 'measurement' in item]
    return ingredients

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        logger.debug("Received POST request to /generate")
        try:
            data = request.get_json()
            logger.debug(f"Request JSON data: {data}")

            if not data:
                logger.error("No JSON data received")
                return jsonify({"error": "No JSON data received"}), 400

            api_key = data.get('api_key')
            user_input = data.get('user_input')

            if not api_key:
                logger.error("API key is required")
                return jsonify({"error": "API key is required"}), 400
            if not user_input:
                logger.error("User input is required")
                return jsonify({"error": "User input is required"}), 400

               # No longer using the hard coded haul_filepath
            # haul_filepath = os.path.join(app.root_path, 'haul', 'haul.json')
            if not os.path.exists(food_list_file):
                logger.error("No ingredients found. Please add items to your fridge first.")
                return jsonify({"error": "No ingredients found. Please add items to your fridge first."}), 400

            with open(food_list_file, 'r') as file:
                ingredients_list = json.load(file)
                if not ingredients_list:
                    logger.error("No ingredients found in haul.json")
                    return jsonify({"error": "No ingredients found in haul.json"}), 400

            prompt_parts = [
                "We are creating a recipe. The output should be in JSON format with specific sections with no additional comments.",
                "The JSON structure should include 'title', 'serving_size', 'ingredients', and 'instructions' in that order.",
                "Start with a 'title' section, followed by 'serving_size'. Then, 'serving_size' should be 4.",
                "Each ingredient must have a measurement indicating how much to use of that ingredient.",
                (
                    "Finally, provide 'instructions' as an ordered list. You do not have to use all the ingredients in the following list. "
                    "The 'instructions' section needs to include the minutes it will take to cook each ingredient in plain sentence format. "
                    "Only use what you need for the recipe. If the following list does not include an ingredient, do NOT include it. "
                    f"Here is the list of ingredients to choose from: {', '.join(ingredients_list)}"
                ),
                "Please format the ingredients as a JSON object.",
                f"The food I want to make is: {user_input}"
            ]
            final_prompt = " ".join(prompt_parts)
            logger.debug(f"Final prompt for OpenAI: {final_prompt}")

            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": final_prompt}],
                model="gpt-4o-mini"
            )

            generated_text = response.choices[0].message.content
            logger.debug(f"Generated text from OpenAI: {generated_text}")

            # Clean up the response to ensure valid JSON format
            generated_text = generated_text.strip("```json").strip("```").strip()
            # Remove escape characters
            generated_text = generated_text.replace('\n', '').replace('\\"', '"')

            # Validate the response JSON directly from OpenAI
            try:
                recipe_data = json.loads(generated_text)
            except json.JSONDecodeError as e:
                logger.error(f"Generated text is not valid JSON: {e}")
                return jsonify({"error": "Failed to generate a valid recipe. Please try again."}), 500

            recipe_data['ingredients'] = flatten_ingredients(recipe_data['ingredients'])

            directory = os.path.join(app.root_path, 'response')
            if not os.path.exists(directory):
                os.makedirs(directory)

            response_file_path = os.path.join(directory, 'out.json')
            with open(response_file_path, 'w') as outfile:
                json.dump({'generated_text': json.dumps(recipe_data)}, outfile)

            logger.debug(f"Recipe successfully generated and saved.")
            return jsonify(recipe=recipe_data)

        except Exception as e:
            logger.exception("Error during processing")
            return jsonify({"error": str(e)}), 500

    if request.method == 'GET':
        logger.debug("Received GET request to /generate")
        response_file_path = os.path.join(app.root_path, 'response', 'out.json')
        if os.path.exists(response_file_path):
            with open(response_file_path, 'r') as outfile:
                response_data = json.load(outfile)
                generated_text = response_data.get('generated_text', '')
                recipe_data = json.loads(generated_text)
                return render_template('generate — CookAI.html', recipe=recipe_data)
        else:
            logger.error("No recipe found. Please generate a recipe first.")
            return "No recipe found. Please generate a recipe first.", 400

@app.route('/upload-haul', methods=['POST'])
def upload_haul():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    api_key = request.form['api_key']

    if file.filename == '':
        return "No selected file", 400
    
    if file and api_key:
        # Correct usage of haul_directory instead of directory
        if not os.path.exists(haul_directory):
            os.makedirs(haul_directory)

        filepath = os.path.join(haul_directory, 'haul.jpeg')
        file.save(filepath)
        
        with open(filepath, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Put a name to all of these ingredients in a JSON formatted list with no extra jargon. Include the label 'ingredients'"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            json_response = response.json()
            content = json_response['choices'][0]['message']['content']
            
            # Extract the JSON part from the content
            start = content.find('{')
            end = content.rfind('}') + 1
            json_data = content[start:end]
            
            # Debug prints to check the extracted JSON data
            print(f"Full content:\n{content}\n")
            print(f"Extracted JSON data:\n{json_data}\n")
            
            if json_data.strip():  # Check if json_data is not empty
                json_filepath = os.path.join(haul_directory, 'haul.json')
                new_ingredients = json.loads(json_data).get('ingredients', [])

                # Append to the existing haul.json file
                if os.path.exists(json_filepath):
                    with open(json_filepath, 'r') as json_file:
                        existing_data = json.load(json_file)
                    existing_ingredients = existing_data.get('ingredients', [])
                else:
                    existing_ingredients = []

                # Append new ingredients to existing ones and remove duplicates
                combined_ingredients = existing_ingredients + new_ingredients
                # Remove duplicates while preserving order
                seen = set()                                                                                     
                combined_ingredients = list(dict.fromkeys(combined_ingredients))  # Remove duplicates while preserving order

                with open(json_filepath, 'w') as json_file:
                    json.dump({'ingredients': combined_ingredients}, json_file, indent=2)

                return jsonify({'ingredients': combined_ingredients})
            else:
                return "Extracted JSON data is empty", 500
        else:
            return f"OpenAI API request failed: {response.text}", 500

    return "File upload failed", 500
    
@app.route('/generate-recipes', methods=['POST'])
def generate_recipes():
    try:
        api_key = request.json.get('api_key_recipes')
        if not api_key:
            return jsonify(error="API key is required"), 400

        # Check if the haul.json file exists
        if not os.path.exists(food_list_file):
            return jsonify(error="No ingredients found. Please add items to your fridge first."), 400

        try:
            with open(food_list_file, 'r') as file:
                ingredients_data = json.load(file)
                ingredients_list = ingredients_data.get('ingredients', [])
                if not ingredients_list:
                    return jsonify(error="No ingredients found in haul.json"), 400
        except Exception as e:
            return jsonify(error=f"Error reading haul.json: {str(e)}"), 500

        # Ensure ingredients_list is a list of strings
        if isinstance(ingredients_list, list):
            ingredients_list = [ingredient if isinstance(ingredient, str) else str(ingredient) for ingredient in ingredients_list]

        # Load additional conditions from genConditions.json
        gen_conditions_path = os.path.join(app.root_path, 'haul', 'genConditions.json')
        haul_conditions_path = os.path.join(app.root_path, 'haul', 'haulConditions.json')

        # Initialize variables for conditions
        serving_size = None
        prep_time = None
        recipe_type = None
        allergies = None

        # Load general conditions (serving size and prep time)
        if os.path.exists(gen_conditions_path):
            with open(gen_conditions_path, 'r') as conditions_file:
                gen_conditions = json.load(conditions_file)
                serving_size = gen_conditions.get('serving_size')
                prep_time = gen_conditions.get('prep_time')

        # Load specific conditions (diet and allergies)
        if os.path.exists(haul_conditions_path):
            with open(haul_conditions_path, 'r') as conditions_file:
                haul_conditions = json.load(conditions_file)
                recipe_type = haul_conditions.get('diets')
                allergies = haul_conditions.get('allergies')                                             
        # Construct the OpenAI prompt with all available conditions
        prompt_parts = [
            f"Generate 10 different meals I can make with this set of food: {', '.join(ingredients_list)}."
                                                                                                                                              
        ]

        if serving_size:
            prompt_parts.append(f"Each recipe should serve {serving_size} people.")
        
        if prep_time:
            prompt_parts.append(f"Each recipe should take no more than {prep_time} minutes to prepare.")
        
        if recipe_type:
            prompt_parts.append(f"Each recipe should be suitable for a {', '.join(recipe_type)} diet.")
        
        if allergies:
            prompt_parts.append(f"Make sure to exclude any ingredients that may trigger these allergies: {', '.join(allergies)}.")
        
        # Final format for JSON output
        prompt_parts.append("Please format the recipes as a JSON array with each recipe containing 'meal', 'serving_size', 'type (diet)', 'allergies', 'prep_time', 'ingredients' with quantities, and 'instructions'.")

        final_prompt = " ".join(prompt_parts)

        # Create an OpenAI client instance
        client = OpenAI(api_key=api_key)

        # Generate a chat completion
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": final_prompt}],
            model="gpt-4o-mini"
        )

        # Extract the generated text
        generated_text = response.choices[0].message.content

        # Debug print to check the raw API response
        print(f"Raw API response: {generated_text}")

        # Find the JSON object within the text
        start_index = generated_text.find('[')
        end_index = generated_text.rfind(']')
        if start_index == -1 or end_index == -1:
            return jsonify(error="Failed to find JSON in response"), 500

        json_text = generated_text[start_index:end_index + 1]

        # Convert the extracted JSON text to a Python object
        recipes = json.loads(json_text)

        # Save the extracted JSON to recipes.json in the local haul folder
        recipes_filepath = os.path.join(haul_directory, 'recipes.json')  # Use the local haul_directory
        with open(recipes_filepath, 'w') as json_file:
            json.dump(recipes, json_file, indent=2)

        # Return the generated recipes
        return jsonify(recipes=recipes)

    except Exception as e:
        return jsonify(error=f"Failed to generate recipes: {str(e)}"), 500
        
# Route to get the current food list
@app.route('/get-food-list', methods=['GET'])
def get_food_list():
    try:
        # Load haul.json file
        if os.path.exists(food_list_file):
            with open(food_list_file, 'r') as file:
                data = json.load(file)
                return jsonify(data)  # Expecting data to include 'ingredients'
        else:
            return jsonify({"ingredients": []})  # If no file, send empty list
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to save an edited food item
@app.route('/save-food', methods=['POST'])
def save_food():
    try:
        data = request.json
        index = data['index']
        new_name = data['new_name']

        # Load the current food list
        with open(food_list_file, 'r') as file:
            food_data = json.load(file)

        # Validate index to ensure it is within the range of the list
        if not 0 <= index < len(food_data['ingredients']):
                                                      
                                                   
                                                    
                                                                          
             
            return jsonify({"error": "Index out of range"}), 400

        # Update the food item
        food_data['ingredients'][index] = new_name
        
        # Save the updated list back to haul.json
        with open(food_list_file, 'w') as file:
            json.dump(food_data, file, indent=2)
            
        return jsonify({"message": "Food name updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to delete a food item
@app.route('/delete-food', methods=['POST'])
def delete_food():
    try:
        data = request.json
        index = data['index']

        with open(food_list_file, 'r') as file:
            food_data = json.load(file)

        if 0 <= index < len(food_data['ingredients']):
            food_data['ingredients'].pop(index)
            with open(food_list_file, 'w') as file:
                json.dump(food_data, file, indent=2)
            return jsonify({"message": "Food deleted successfully!"})
        else:
            return jsonify({"error": "Index out of range"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add-food', methods=['POST'])
def add_food():
    try:
        logger.debug(f"Current working directory: {os.getcwd()}")
        logger.debug(f"Expected haul.json location: {food_list_file}")

        data = request.json
        new_food = data['newFood']

        # Ensure the directory exists
        os.makedirs(os.path.dirname(food_list_file), exist_ok=True)

        # Check if the file exists and create it if not
        if not os.path.exists(food_list_file):
            food_data = {'ingredients': []}
        else:
            with open(food_list_file, 'r') as file:
                food_data = json.load(file)

        # Check for duplicates before adding
        if new_food in food_data['ingredients']:
            return jsonify({"error": "Food item already exists"}), 400

        food_data['ingredients'].append(new_food)
        with open(food_list_file, 'w') as file:
            json.dump(food_data, file, indent=2)
        
        return jsonify({"message": "Food added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to clear the food list
@app.route('/clear-food-list', methods=['POST'])
def clear_food_list():
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(food_list_file), exist_ok=True)

        # Clear the food list by overwriting with an empty list
        food_data = {'ingredients': []}
        with open(food_list_file, 'w') as file:
            json.dump(food_data, file, indent=2)

        return jsonify({"message": "All food items cleared successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check-haul', methods=['GET'])
def check_haul():
    logger.debug("Received request to /check-haul")
    try:
        food_list_file = os.path.join(app.root_path, 'haul', 'haul.json')
        if os.path.exists(food_list_file):
            logger.debug("Haul file exists")
            return jsonify({"exists": True})
        else:
            logger.debug("Haul file does not exist")
            return jsonify({"exists": False})
    except Exception as e:
        logger.exception("Error during haul check")
        return jsonify({"error": str(e)}), 500

# Function to create a backup of the current ingredient list
def create_backup():
    haul_filepath = os.path.join(app.root_path, 'haul', 'haul.json')
    haul_backup_filepath = os.path.join(app.root_path, 'haul', 'haulBackup.json')
    
    # Check if haul.json exists before attempting to copy
    if os.path.exists(haul_filepath):
        shutil.copy(haul_filepath, haul_backup_filepath)
    else:
        raise FileNotFoundError("No haul.json file found to backup")

gen_conditions_file = os.path.join(app.root_path, 'haul', 'genConditions.json')
haul_conditions_file = os.path.join(app.root_path, 'haul', 'haulConditions.json')

# Route to get the general conditions (serving size and prep time)
@app.route('/get-gen-conditions', methods=['GET'])
def get_gen_conditions():
    try:
        if os.path.exists(gen_conditions_file):
            with open(gen_conditions_file, 'r') as file:
                data = json.load(file)
            return jsonify(data)
        else:
            return jsonify({"serving_size": "", "prep_time": ""}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to save or update general conditions (serving size or prep time)
@app.route('/save-gen-conditions', methods=['POST'])
def save_gen_conditions():
    try:
        data = request.json

        # Ensure genConditions.json exists, or create a default one
        if not os.path.exists(gen_conditions_file):
            gen_conditions_data = {"serving_size": "", "prep_time": ""}
        else:
            with open(gen_conditions_file, 'r') as file:
                gen_conditions_data = json.load(file)

        # Update serving size or prep time based on input
        if 'serving_size' in data:
            gen_conditions_data['serving_size'] = data['serving_size']
        if 'prep_time' in data:
            gen_conditions_data['prep_time'] = data['prep_time']

        # Save the updated data back to genConditions.json
        with open(gen_conditions_file, 'w') as file:
            json.dump(gen_conditions_data, file, indent=2)

        return jsonify({"message": "General conditions updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get the haul conditions (including allergies, diets, and spice tolerance)
@app.route('/get-haul-conditions', methods=['GET'])
def get_haul_conditions():
    try:
        if os.path.exists(haul_conditions_file):
            with open(haul_conditions_file, 'r') as file:
                data = json.load(file)
            return jsonify(data)
        else:
            return jsonify({"allergies": [], "diets": [], "spiciest_food": ""}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to save or update spice tolerance in haulConditions.json
@app.route('/save-spice-tolerance', methods=['POST'])
def save_spice_tolerance():
    try:
        data = request.json
        spiciest_food = data.get('spiciest_food', '')

        # Ensure haulConditions.json exists, or create a default one
        if not os.path.exists(haul_conditions_file):
            haul_conditions_data = {"allergies": [], "diets": [], "spiciest_food": ""}
        else:
            with open(haul_conditions_file, 'r') as file:
                haul_conditions_data = json.load(file)

        # Update spiciest food
        haul_conditions_data['spiciest_food'] = spiciest_food

        # Save the updated data back to haulConditions.json
        with open(haul_conditions_file, 'w') as file:
            json.dump(haul_conditions_data, file, indent=2)

        return jsonify({"message": "Spice tolerance updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/modify-ingredients', methods=['POST'])
def modify_ingredients():
    try:
        # Create a backup of the current ingredient list before making changes
        create_backup()

        data = request.get_json()
        api_key = data.get('api_key')

        if not api_key:
            return jsonify({"error": "API key is required"}), 400

        # Load the current conditions from haulConditions.json (allergies, diets, spiciest food)
        with open(haul_conditions_file, 'r') as file:
            haul_conditions_data = json.load(file)
        
        dietary_preferences = haul_conditions_data.get('diets', [])
        allergies = haul_conditions_data.get('allergies', [])
        spiciest_food = haul_conditions_data.get('spiciest_food', '')

        # Load the current ingredient list from haul.json
        haul_filepath = os.path.join(app.root_path, 'haul', 'haul.json')
        with open(haul_filepath, 'r') as file:
            ingredients_data = json.load(file)

        # Construct the prompt dynamically, adding logic to remove ingredients based on the conditions
        prompt = (
            f"Edit the ingredient list to fit the following criteria: {', '.join(dietary_preferences)} "
            f"and free of: {', '.join(allergies)}. "
            f"Here is the current ingredient list: {', '.join(ingredients_data['ingredients'])}. "
            f"Additionally, please identify and remove any ingredients spicier than {spiciest_food}. "
            f"Return the output in a valid JSON format, and only include the updated list of ingredients under an 'ingredients' key."
        )

        # Send the prompt to OpenAI using the provided API key
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini"
        )

        # Handle potential errors with the OpenAI response
        if response is None or not response.choices or not response.choices[0].message.content:
            return jsonify({"error": "Failed to get a valid response from OpenAI"}), 500

        generated_text = response.choices[0].message.content
        logger.debug(f"Generated text from OpenAI: {generated_text}")

        # Parse the response ensuring valid JSON
        try:
            generated_text = generated_text.strip("```json").strip("```").strip()
            new_ingredients = json.loads(generated_text).get('ingredients', [])
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse generated text as JSON: {e}")
            return jsonify({"error": "OpenAI response is not valid JSON"}), 500

        # Overwrite the haul.json file with the modified list
        with open(haul_filepath, 'w') as file:
            json.dump({'ingredients': new_ingredients}, file, indent=2)

        return jsonify({"message": "Ingredient list modified successfully!", "ingredients": new_ingredients})

    except Exception as e:
        logger.exception("Error occurred during ingredient modification")
        return jsonify({"error": str(e)}), 500

# Allergies routes
@app.route('/save-allergy', methods=['POST'])
def save_allergy():
    data = request.json
    index = data.get('index')
    new_name = data.get('new_name')

    # Load the current conditions from haulConditions.json
    with open(haul_conditions_file, 'r') as file:
        haul_conditions_data = json.load(file)

    # Validate index and update allergy
    if 0 <= index < len(haul_conditions_data['allergies']):
        haul_conditions_data['allergies'][index] = new_name
        with open(haul_conditions_file, 'w') as file:
            json.dump(haul_conditions_data, file, indent=2)
        return jsonify({"message": "Allergy updated successfully!"})
    return jsonify({"error": "Index out of range"}), 400

@app.route('/delete-allergy', methods=['POST'])
def delete_allergy():
    data = request.json
    index = data.get('index')

    with open(haul_conditions_file, 'r') as file:
        haul_conditions_data = json.load(file)

    # Validate index and remove allergy
    if 0 <= index < len(haul_conditions_data['allergies']):
        haul_conditions_data['allergies'].pop(index)
        with open(haul_conditions_file, 'w') as file:
            json.dump(haul_conditions_data, file, indent=2)
        return jsonify({"message": "Allergy deleted successfully!"})
    return jsonify({"error": "Index out of range"}), 400

@app.route('/add-allergy', methods=['POST'])
def add_allergy():
    try:
        data = request.json
        new_allergy = data.get('newAllergy')

        # Check if the file exists, if not, create it with a default structure
        if not os.path.exists(haul_conditions_file):
            haul_conditions_data = {"allergies": [], "diets": [], "spiciest_food": ""}
        else:
            with open(haul_conditions_file, 'r') as file:
                haul_conditions_data = json.load(file)

        # Add allergy if it doesn't already exist
        if new_allergy not in haul_conditions_data['allergies']:
            haul_conditions_data['allergies'].append(new_allergy)
            with open(haul_conditions_file, 'w') as file:
                json.dump(haul_conditions_data, file, indent=2)
            return jsonify({"message": "Allergy added successfully!"})
        else:
            return jsonify({"error": "Allergy already exists"}), 400

    except Exception as e:
        logger.exception("Error adding allergy")
        return jsonify({"error": str(e)}), 500


@app.route('/clear-allergies', methods=['POST'])
def clear_allergies():
    with open(haul_conditions_file, 'r') as file:
        haul_conditions_data = json.load(file)

    # Clear all allergies
    haul_conditions_data['allergies'] = []
    with open(haul_conditions_file, 'w') as file:
        json.dump(haul_conditions_data, file, indent=2)
    return jsonify({"message": "All allergies cleared successfully!"})

# Diet routes
@app.route('/save-diet', methods=['POST'])
def save_diet():
    data = request.json
    index = data.get('index')
    new_name = data.get('new_name')

    # Load the current conditions from haulConditions.json
    with open(haul_conditions_file, 'r') as file:
        haul_conditions_data = json.load(file)

    # Validate index and update diet
    if 0 <= index < len(haul_conditions_data['diets']):
        haul_conditions_data['diets'][index] = new_name
        with open(haul_conditions_file, 'w') as file:
            json.dump(haul_conditions_data, file, indent=2)
        return jsonify({"message": "Diet updated successfully!"})
    return jsonify({"error": "Index out of range"}), 400

@app.route('/delete-diet', methods=['POST'])
def delete_diet():
    data = request.json
    index = data.get('index')

    with open(haul_conditions_file, 'r') as file:
        haul_conditions_data = json.load(file)

    # Validate index and remove diet
    if 0 <= index < len(haul_conditions_data['diets']):
        haul_conditions_data['diets'].pop(index)
        with open(haul_conditions_file, 'w') as file:
            json.dump(haul_conditions_data, file, indent=2)
        return jsonify({"message": "Diet deleted successfully!"})
    return jsonify({"error": "Index out of range"}), 400

@app.route('/add-diet', methods=['POST'])
def add_diet():
    data = request.json
    new_diet = data.get('newDiet')

    with open(haul_conditions_file, 'r') as file:
        haul_conditions_data = json.load(file)

    # Add diet if it doesn't already exist
    if new_diet not in haul_conditions_data['diets']:
        haul_conditions_data['diets'].append(new_diet)
        with open(haul_conditions_file, 'w') as file:
            json.dump(haul_conditions_data, file, indent=2)
        return jsonify({"message": "Diet added successfully!"})
    return jsonify({"error": "Diet already exists"}), 400

@app.route('/clear-diets', methods=['POST'])
def clear_diets():
    with open(haul_conditions_file, 'r') as file:
        haul_conditions_data = json.load(file)

    # Clear all diets
    haul_conditions_data['diets'] = []
    with open(haul_conditions_file, 'w') as file:
        json.dump(haul_conditions_data, file, indent=2)
    return jsonify({"message": "All diets cleared successfully!"})

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    import threading
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()

    # Open the local server in a webview window
    webview.create_window("CookAI", "http://127.0.0.1:5000", width=1024, height=768)
    webview.start()
