from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Connect to MySQL database

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  # ← put your password here if needed
    database="college_chatbot"
)


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("query", "").lower()

    cursor = db.cursor(dictionary=True)

    # Fetch all question-answer pairs from the table
    cursor.execute("SELECT question, answer FROM chatbot_responses")
    results = cursor.fetchall()

    # Match user input with questions
    for row in results:
        if row["question"].lower() in user_input:
            return jsonify({"response": row["answer"]})

    return jsonify({"response": "Sorry, I don't have that information right now."})

if __name__ == '__main__':
    app.run(debug=True)
