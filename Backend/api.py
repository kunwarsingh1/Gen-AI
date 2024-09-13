from flask import Flask, request
import os
from dotenv import load_dotenv
import json
import google.generativeai as genai
from flask_cors import CORS

# Initialize environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.environ.get('KEY'))

# Define the generative model
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
CORS(app)


@app.route('/convert')
def text_output():
    # Fetch 'data' and 'language' from query parameters
    data = request.args.get('data')
    language = request.args.get('language')

    # Generate content using the model
    response = model.generate_content(f'Convert the given "{data}" into the "{language}" language in format--- "{language}": "content" in json')
    
    # Access and clean the generated text
    generated_text = response._result.candidates[0].content.parts[0].text
    clean_text = generated_text.strip('```json \n')

        # Parse the JSON content
    json_output = json.loads(clean_text)
    return json_output[language]


@app.route('/')
def hello():
    return "Hello World"