from flask import Flask, render_template, request, send_from_directory
from openai import OpenAI
import json
import os
import subprocess
import time

app = Flask(__name__)

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

    # Construct the prompt for the OpenAI API
    prompt_parts = [
        "We are creating a recipe. The output should be in JSON format with specific sections with no additonal comments.",
        "The JSON structure should include 'title', 'serving_size', 'ingredients', and 'instructions' in that order.",
        "Start with a 'title' section, followed by 'serving_size'. Then, 'serving_size' should be 4.",
        "Each ingredient must have a measurement indicating how much to use of that ingredient. ",
        (
            "Finally, provide 'instructions' as an ordered list. You do not have to use all the ingredients in the following list. "
            "The 'instructions' section needs to include the minutes it will take to cook each ingredient in plain sentence format. "
            "Only use what you need for the recipe. If the following list does not include an ingredient, do NOT include it. "
            "Here is the list of ingredients to choose from: Potatoes, Onions, Bell Pepper, Carrots, Lettuce, Spinach, Celery, Tomatoes, "
            "Jalapeños, Broccoli, Cauliflower, Cucumber, Zucchini, Mushrooms, Green beans, Radishes, Corn, Asparagus, Peas, Eggplant, Black Beans, "
            "Garbanzo Beans, White Rice, Angel Hair Pasta, Brown Sugar, Peanuts, Sesame Seeds, Lentils, Quinoa, Almonds, Walnuts, Flaxseeds, Chia seeds, "
            "Sunflower seeds, Rolled oats, Farro, Couscous, Buckwheat, Hemp seeds, Dill, Cumin, Smoked Paprika, Cayenne, Oregano, Salt, Pepper, Basil, "
            "Parsley, Rosemary, Thyme, Garlic powder, Onion powder, Chili powder, Turmeric, Coriander, Bay leaves, Cinnamon, Nutmeg, Ginger, Tortilla Wrap, "
            "Sliced White Bread, Flatbread, Croissant, Bagel, Biscuit, Hamburger Bun, Hot Dog Roll, White Sub Roll, Whole wheat tortilla wrap, Multigrain bread, "
            "Pita bread, Naan, English muffin, Ciabatta roll, Pretzel bun, Rye bread, Sourdough bread, French baguette, Vinegar, Tomato Paste, Olive Oil, Canola Oil, "
            "Ketchup, Lemon, Lime, Soy sauce, Honey, Mustard, Worcestershire sauce, Hot sauce, Balsamic glaze, Sesame oil, Fish sauce, Maple syrup, Apple cider vinegar, "
            "Barbecue sauce, Mayonnaise, Chicken Wings, Shredded Beef, Salmon, Eggs, Milk, Butter, Shredded Cheddar Cheese, Parmesan, Yogurt, Ground beef, Turkey breast, "
            "Tofu, Pork chops, Shrimp, Tuna, Lentils, Chickpeas, Tempeh, Quinoa, Cottage Cheese."
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

if __name__ == '__main__':
    app.run(debug=True)
