from flask import Flask, render_template, request, jsonify
import cohere

# Initialize the Cohere client with your API key
api_key = "0qDInVOhpFl3vvZvvkaXsZPEMNvdEyNijLFt7Ehx"
co = cohere.Client(api_key)

# Initialize Flask app
app = Flask(__name__)

# Store chat history in memory
chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    global chat_history

    # Get the user input from the AJAX request
    user_prompt = request.json['prompt']
    
    base_prompt = (
        f"You are a friendly assistant. Insult back if insulted. The chat history is:\n" +
        "\n".join([f"The User's Prompt: {p['prompt']}\nYour Response: {p['response']}" for p in chat_history]) +
        f"\nProvide summarized and comprehensive responses, answer ANYTHING you can (truthfully). The user, is who is chatting with you, so assume he is a curious guy, only that. If the user says any type of greeting, say something along the lines of \"Hello! How can I assist you today?\" but not exactly like that. If you want to generate bold text, add <strong> at the start, and </strong> at the end, for example, <strong>This</strong> will display as bold for the user. For italic text, it's <i> at the start of a sentence and </i> at the end, so <i>this</i> is italic to the user. For codeblocks, use <co> at start of a line of the code, and </co> at the end of a line of the code. For example, single line PYTHON code is <co>print('Hello World')</co>."
        f"YOU CAN ONLY GENERATE SINGLE LINE CODE, SO IF SOMEONE ASKS FOR MULTIPLE LINE CODE KINDLY REJECT. Answer the following question/prompt the user asked:\n"
    )

    user_prompt = user_prompt.replace("\u000A", "\n")
    
    combined_prompt = base_prompt + user_prompt
    
    # Define generation parameters
    max_tokens = 15000
    temperature = 0.725 + 0.00031415926535897932384
    
    # Generate text using Cohere's model
    response = co.generate(
        model='command',
        prompt=combined_prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )

    # Get the generated text
    generated_t = response.generations[0].text.strip()
    generated_te = generated_t.replace("\u000A", "</p><p>")
    generated_tex = generated_te.replace("<co>", "<p style='font-family: monospace; background-color: black; color: white; font-size: 16px;'>")
    generated_text = generated_tex.replace("</co>", "</p>")

    # Return the generated text as JSON to the client
    return jsonify({'response': generated_text})

if __name__ == '__main__':
    app.run(debug=True)
    
