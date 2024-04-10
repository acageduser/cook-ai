from flask import Flask, render_template, request
import openai
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    # Render the HTML page for user interaction
    return render_template('Kitchen — CookAI.html')

@app.route('/generate', methods=['POST'])
def generate():

    api_key = request.form['api_key']
    user_input = request.form['user_input']

    if not api_key:
        return "API key is required", 400
    if not user_input:
        return "User input is required", 400

    # Part 1 of the prompt (setup)
    prompt_part1 = ("Generate a recipe with an 'ingredients', 'prepare' and 'cook' section. ")

    # Part 2 of the prompt (serving size)
    prompt_part2 = ("The serving size is 4. ")

    # Part 3 of the prompt (allergens)
    prompt_part3 = ("I'm allergic to "
                   "sesame seeds, peanuts"
                   ". Do not include the allergens in the recipe!")
    
    # Part 4 of the prompt (formatting)
    prompt_part4 = ("List out the ingredients using only JSON formatting, preperation steps, and "
                    " how to cook the food and format it in a step by step list"
                    " using new lines, headings, and bulleted lists"
                    "Provide your answer in JSON form. Reply with only the answer in JSON form and "
                    "include no other commentary: ")
    

    # Part 5 of the prompt (Ingredients list)
    # NOTE: This part MUST be the final part of the prompt.
    prompt_part5 = ("Include how much of each ingredient you need. "
                    "Use only this list of ingredients to create a step "
                    "by step recipe: "
                    "Garlic, Carrots, Celery, Jalapenos, Cilantro, Parsley, Dill, "
                    "Potatoes, Bell Pepper, Spinach, Lemon, Lime, Vinegar, Chicken Wings, "
                    "Eggs, Butter, Yogurt, Parmesan, Garbanzo Beans, White Rice, Tomato Paste, "
                    "Olive Oil, Canola Oil, Cumin, Smoked Paprika, Cayenne, Oregano, "      
                    "Milk, Peanuts, Table Salt, Pepper Shredded Beef, "
                    "Angel Hair Pasta, Brown Sugar, Shredded Cheese, Tomato, "
                    "Ketchup, Lettuce, Salmon, Onion, Black Beans, Sesame Seeds. "
                    "The food I want to make is: ")


    # Combine all the prompt_partX together with user input to create the final_prompt
    final_prompt = prompt_part1 + prompt_part2 + prompt_part3 + prompt_part4 + prompt_part5 + user_input

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
        return f"An error occurred: {str(e)}", 500

    # Save the generated text to a JSON file in the 'response' folder
    output_data = {'generated_text': generated_text}
    with open('response/out.json', 'w') as outfile:
        json.dump(output_data, outfile)

    # Send the generated text back to the client
    return generated_text

if __name__ == '__main__':
    app.run(debug=True)
