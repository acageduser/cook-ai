from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import json
from openai import OpenAI
import os
import base64
import requests

app = Flask(__name__)

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

def flatten_ingredients(ingredients):
    flattened = {}
    for key, value in ingredients.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flattened[f"{key} - {sub_key}"] = sub_value
        else:
            flattened[key] = value
    return flattened

@app.route('/generate', methods=['POST'])
def generate():
    api_key = request.form['api_key']
    user_input = request.form['user_input']

    # Check for API key and user input
    if not api_key:
        return "API key is required", 400
    if not user_input:
        return "User input is required", 400
        
    # Check if the haul.json file exists
    haul_filepath = os.path.join(app.root_path, 'haul', 'haul.json')
    if not os.path.exists(haul_filepath):
        return "No ingredients found. Please add items to your fridge first.", 400

    try:
        with open(haul_filepath, 'r') as file:
            ingredients_list = json.load(file)
            if not ingredients_list:
                return "No ingredients found in haul.json", 400
    except Exception as e:
        return f"Error reading haul.json: {str(e)}", 500

    # Construct the prompt for the OpenAI API
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
    
    max_attempts = 15
    attempt_counter = 0
    response_file_path = os.path.join(app.root_path, 'response', 'out.json')

    while attempt_counter < max_attempts:
        attempt_counter += 1
        try:
            # Create an OpenAI client instance
            client = OpenAI(api_key=api_key)

            # Generate a chat completion
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": final_prompt}],
                model="gpt-3.5-turbo"
            )

            # Extract the generated text
            generated_text = response.choices[0].message.content

            # Check and create the 'response' directory if it does not exist
            directory = os.path.join(app.root_path, 'response')
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save the generated text to a JSON file in the 'response' folder
            with open(response_file_path, 'w') as outfile:
                json.dump({'generated_text': generated_text}, outfile)

            # Validate the JSON file
            if validate_json(response_file_path):
                break  # Exit the loop if the JSON is valid
            else:
                print(f"Attempt {attempt_counter} failed. Invalid JSON format. Retrying...")

        except Exception as e:
            print(f"Attempt {attempt_counter} failed with error: {str(e)}. Retrying...")

    if attempt_counter == max_attempts:
        return "Failed to generate a valid recipe after multiple attempts.", 500

    # Read the generated text from the JSON file
    with open(response_file_path, 'r') as outfile:
        response_data = json.load(outfile)
        generated_text = response_data.get('generated_text', '')

    # Parse the generated JSON and flatten the ingredients
    recipe_data = json.loads(generated_text)
    recipe_data['ingredients'] = flatten_ingredients(recipe_data['ingredients'])

    # Log the number of attempts
    with open('attempt_log.txt', 'w') as log_file:
        log_file.write(f"Number of attempts: {attempt_counter}")

    # Print the number of attempts to the console
    print(f"++++++++++++++++++++++++++++++++++++++++++++")
    print(f"+    Number of attempts: {attempt_counter}                 +")
    print(f"++++++++++++++++++++++++++++++++++++++++++++")

    # Return the generated text to the client by rendering a template
    return render_template('generate — CookAI.html', recipe=recipe_data)

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
                        {"type": "text", "text": "Put a name to all of these ingredients in a JSON formatted list with not extra jargon. Include the label 'ingredients'"},
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
                try:
                    with open(json_filepath, 'w') as json_file:
                        json.dump(json.loads(json_data), json_file, indent=2)
                    return jsonify(json.loads(json_data))
                except Exception as e:
                    return f"Failed to save JSON: {str(e)}", 500
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
    if os.path.exists(food_list_file):
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})


if __name__ == '__main__':
    app.run(debug=True)
