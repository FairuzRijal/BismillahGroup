from flask import Flask, request, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

uri = "mongodb+srv://aslamsyadzili2:Aslam160208@bismillahsensordht.fjuui.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client["Esp32Sensor"]
collection = db["sensor"]

@app.route('/')
def check():
    return "Bisa cuy!!!!!!!"

@app.route('/profile')
def profile():
    return """Nama: Ilham
    Umur: 76
    Lokasi: Di depan
    """

@app.route('/data', methods=['POST'])
def collect_data():
    data = request.get_json()

    print("Data dari Ubidots:", json.dumps(data, indent=4))

    temperature = data["temperature"]
    humidity = data["humidity"]
    motion = data["motion"]

    post = {"temperature": temperature, "humidity": humidity, "motion": motion}

    # Send to mongodb
    collection.insert_one(post)
    return jsonify({"status": "success", "message": "Data saved"}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)