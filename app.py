from flask import Flask, request
from dotenv import dotenv_values
from flask_cors import CORS
import openai, json


def chat_request(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    ).choices[0].message.content


config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]
 
app = Flask(__name__)

CORS(app)

@app.route("/palette")
def palette():
    messages = [
        {"role": "system", "content": """
            You are a color palette generating assistant tat responds to text prompts for color palettes.
            You should generate color palettes that fit the theme, mood, or instructions in the prompt.
            The palettes should be between 2 and 8 colors.
            Desired Format: a JSON array of hexadecimal color codes without any dictionary surrounding it.
         
            Example Response: ["#FF0000", "#00FF00", "#0000FF"]
         """},
         {"role": "user", "content": request.args.get("prompt")},
    ]
    return json.loads(chat_request(messages))


if __name__ == "__main__":
    app.run(debug=True)
