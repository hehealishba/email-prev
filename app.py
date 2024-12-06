from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_email(subject, recipient_name, purpose, key_points, tone="formal"):
    """
    Generates a business email draft based on user inputs.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that writes professional business emails.",
        },
        {
            "role": "user",
            "content": (
                f"Write a {tone} business email with the following details:\n"
                f"- Subject: {subject}\n"
                f"- Recipient: {recipient_name}\n"
                f"- Purpose: {purpose}\n"
                f"- Key points: {key_points}\n\n"
                "The email should start with a greeting, address the recipient properly, "
                "cover all key points clearly, and end with an appropriate closing."
            ),
        },
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating email: {e}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        subject = request.form["subject"]
        recipient_name = request.form["recipient_name"]
        purpose = request.form["purpose"]
        key_points = request.form["key_points"]
        tone = request.form["tone"]

        email_draft = generate_email(subject, recipient_name, purpose, key_points, tone)
        return render_template("index.html", email_draft=email_draft)

    return render_template("index.html", email_draft=None)

if __name__ == "__main__":
    app.run(debug=True)
