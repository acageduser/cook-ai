from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import json
from openai import OpenAI
import os
import base64
import requests
import logging

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

            haul_filepath = os.path.join(app.root_path, 'haul', 'haul.json')
            if not os.path.exists(haul_filepath):
                logger.error("No ingredients found. Please add items to your fridge first.")
                return jsonify({"error": "No ingredients found. Please add items to your fridge first."}), 400

            with open(haul_filepath, 'r') as file:
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
        directory = os.path.join(app.root_path, 'haul')
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, 'haul.jpeg')
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
                json_filepath = os.path.join(directory, 'haul.json')
                new_ingredients = json.loads(json_data).get('ingredients', [])

                # Append to the existing haul.json file
                if os.path.exists(json_filepath):
                    with open(json_filepath, 'r') as json_file:
                        existing_data = json.load(json_file)
                    existing_ingredients = existing_data.get('ingredients', [])
                else:
                    existing_ingredients = []

                # Append new ingredients to existing ones
                combined_ingredients = existing_ingredients + new_ingredients

                # Remove duplicates while preserving order
                seen = set()
                combined_ingredients = [item for item in combined_ingredients if not (item in seen or seen.add(item))]

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
        haul_filepath = os.path.join(app.root_path, 'haul', 'haul.json')
        if not os.path.exists(haul_filepath):
            return jsonify(error="No ingredients found. Please add items to your fridge first."), 400

        try:
            with open(haul_filepath, 'r') as file:
                ingredients_data = json.load(file)
                ingredients_list = ingredients_data.get('ingredients', [])
                if not ingredients_list:
                    return jsonify(error="No ingredients found in haul.json"), 400
        except Exception as e:
            return jsonify(error=f"Error reading haul.json: {str(e)}"), 500

        # Ensure ingredients_list is a list of strings
        if isinstance(ingredients_list, list):
            ingredients_list = [ingredient if isinstance(ingredient, str) else str(ingredient) for ingredient in ingredients_list]

        # Construct the prompt for the OpenAI API
        prompt_parts = [
            f"Generate 10 different meals I can make with this set of food: {', '.join(ingredients_list)}.",
            "Please format the recipes as a JSON array with each recipe containing 'meal', 'serving_size', 'ingredients', and 'instructions'."
        ]
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

        # Save the extracted JSON to recipes.json
        json_filepath = os.path.join(app.root_path, 'haul', 'recipes.json')
        with open(json_filepath, 'w') as json_file:
            json.dump(recipes, json_file, indent=2)

        # Render the updated HTML template with recipes
        return jsonify(recipes=recipes)

    except Exception as e:
        return jsonify(error=f"Failed to generate recipes: {str(e)}"), 500
        
# Route to get the current food list
@app.route('/get-food-list', methods=['GET'])
def get_food_list():
    try:
        haul_filepath = os.path.join(app.root_path, 'haul', 'haul.json')
        if not os.path.exists(haul_filepath):
            return jsonify({"ingredients": []}), 200
        with open(haul_filepath, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to save an edited food item
@app.route('/save-food', methods=['POST'])
def save_food():
    try:
        data = request.json
        index = data['index']
        new_name = data['new_name']

        with open(food_list_file, 'r') as file:
            food_data = json.load(file)

        if 0 <= index < len(food_data['ingredients']):
            food_data['ingredients'][index] = new_name
            with open(food_list_file, 'w') as file:
                json.dump(food_data, file, indent=2)
            return jsonify({"message": "Food name updated successfully!"})
        else:
            return jsonify({"error": "Index out of range"}), 400
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

if __name__ == '__main__':
    app.run(debug=True)
