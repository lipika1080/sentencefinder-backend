from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = "mongodb://sentencefinder:5hUAZosH4RAcnepAdmBByyb8BOaZWqrhNW0Mq92NB3DPLT7v2dNLYqkRHHjyHCk3gfOFdQqry0pLACDbBdMqSw==@sentencefinder.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@sentencefinder@"  # Store your Cosmos DB connection string in .env
client = MongoClient(MONGO_URI)
db = client["finder_app"]
sentences_collection = db["sentences"]

# Add a new sentence and save vowel/consonant count
@app.route("/sentences/vowels-consonants", methods=["POST"])
def get_vowel_consonant():
    data = request.json
    if "sentence" not in data:
        return jsonify({"error": "Sentence is required"}), 400

    sentence = data["sentence"].lower()
    vowels = "aeiou"
    
    vowel_count = sum(1 for char in sentence if char in vowels)
    consonant_count = sum(1 for char in sentence if char.isalpha() and char not in vowels)

    # Save result in database
    sentence_data = {
        "sentence": data["sentence"],
        "vowels": vowel_count,
        "consonants": consonant_count
    }
    sentences_collection.insert_one(sentence_data)

    return jsonify({
        "message": "Sentence processed and saved successfully",
        "vowels": vowel_count,
        "consonants": consonant_count
    }), 201

# Fetch all saved sentences with counts
@app.route("/sentences", methods=["GET"])
def get_sentences():
    sentences = list(sentences_collection.find({}, {"_id": 0}))  # Exclude _id field
    return jsonify(sentences), 200

if __name__ == "__main__":
    app.run(debug=True)
