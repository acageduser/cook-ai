from flask import Flask, render_template, request
import openai

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

    # Part 4 of the prompt (Ingredients list)
    # NOTE: This part MUST be the final part of the prompt.
    prompt_part4 = ("Include how much of each ingredient you need. "
                    "Use only this list of ingredients to create a step "
                    "by step recipe: "
                    "Milk, Peanuts, Table, Pepper, Salt, Shredded Beef, "
                    "Angel Hair Pasta, Brown Sugar, Shredded Cheese, Tomato, "
                    "Ketchup, Lettuce, Salmon, Onion, Black Beans, sesame seeds. "
                    "The food I want to make is: ")


    # Combine all the prompt_partX together with user input to create the final_prompt
    final_prompt = prompt_part1 + prompt_part2 + prompt_part3 + prompt_part4 + user_input

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

    # Send the generated text back to the client
    return generated_text

if __name__ == '__main__':
    app.run(debug=True)
