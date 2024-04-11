from flask import Flask, render_template, request, send_from_directory
import openai
import json

app = Flask(__name__)

@app.route('/response/<filename>')
def response(filename):
    """Serve a file from the 'response' directory."""
    return send_from_directory('response', filename)

@app.route('/', methods=['GET'])
def home():
    """Render the home page."""
    # Render the HTML page for user interaction
    return render_template('Kitchen — CookAI.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Handle the generation of the recipe."""
    api_key = request.form['api_key']
    user_input = request.form['user_input']

    # Check for API key and user input
    if not api_key:
        return "API key is required", 400
    if not user_input:
        return "User input is required", 400
    
    # Construct the prompt for the OpenAI API
    prompt_part0 = "Decide on a name for the recipe and output the name section first."
    prompt_part1 = "Generate a recipe in this order with a 'title', 'serving size', 'ingredients', and 'cook' sections. "
    prompt_part2 = "The serving size is 4. "
    prompt_part3 = "I'm allergic to sesame seeds, peanuts. Do not include the allergens in the recipe!"
    prompt_part4 = ("List out the ingredients using only JSON formatting and cooking steps "
                    "and format it in a step by step list using new lines, headings, and bulleted lists"
                    "Provide your answer in JSON form. Reply with only the answer in JSON form and "
                    "include no other commentary: ")
    prompt_part5 = ("Include how much of each ingredient you need. "
                    "Use only this list of ingredients to create a step by step recipe: "
                    "Garlic, Carrots, Celery, Jalapenos, Cilantro, Parsley, Dill, Potatoes, Bell Pepper, "
                    "Spinach, Lemon, Lime, Vinegar, Chicken Wings, Eggs, Butter, Yogurt, Parmesan, "
                    "Garbanzo Beans, White Rice, Tomato Paste, Olive Oil, Canola Oil, Cumin, "
                    "Smoked Paprika, Cayenne, Oregano, Milk, Peanuts, Table Salt, Pepper, "
                    "Shredded Beef, Angel Hair Pasta, Brown Sugar, Shredded Cheese, Tomato, "
                    "Ketchup, Lettuce, Salmon, Onion, Black Beans, Sesame Seeds. "
                    "The food I want to make is: ")

    # Combine all the parts to create the final prompt
    final_prompt = prompt_part0 + prompt_part1 + prompt_part2 + prompt_part3 + prompt_part4 + prompt_part5 + user_input

    try:
        # Create an OpenAI client instance
        client = openai.OpenAI(api_key=api_key)
        
        # Generate a chat completion
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": final_prompt}],
            model="gpt-3.5-turbo"
        )
        
        # Extract the generated text
        generated_text = response.choices[0].message.content
    except Exception as e:
        # Return an error if something goes wrong
        return f"An error occurred: {str(e)}", 500

    # Save the generated text to a JSON file in the 'response' folder
    output_data = {'generated_text': generated_text}
    with open('response/out.json', 'w') as outfile:
        json.dump(output_data, outfile)

    # Return the generated text to the client by rendering a template
    return render_template('generate — CookAI.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
