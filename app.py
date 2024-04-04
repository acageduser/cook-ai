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

    # Part 1 of the prompt
    prompt_part1 = ("Generate a recipe with an 'ingredients', 'prepare' and 'cook' section. "
                    "Include how much of each ingredient you need. "
                    "Use only this list of ingredients to create a step "
                    "by step recipe to feed 4 people: "
                    "Milk, Peanuts, Table, Pepper/Salt, Shredded Beef, "
                    "Angel Hair Pasta, Brown Sugar, Shredded Cheese, Tomato, "
                    "Ketchup, Lettuce, Salmon, Onion, Black Beans. "
                    "The food I want to make is: ")

    # Combine part 1 and user input to create the final prompt
    final_prompt = prompt_part1 + user_input

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
