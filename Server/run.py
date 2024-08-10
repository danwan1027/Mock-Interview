import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
from mock_interview import create_app
import dlib

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app & print(dlib.__version__+"sdcscsdcdsc")
app = create_app()

CORS(app)  # Enable CORS

# Read the HEYGEN API key from environment variables
HEYGEN_API_KEY = os.getenv('HEYGEN_API_KEY')

@app.route('/get-access-token', methods=['POST'])
def get_access_token():
    try:
        # Ask the server for a secure Access Token
        response = requests.post(
            'https://api.heygen.com/v1/streaming.create_token',
            headers={'x-api-key': HEYGEN_API_KEY}
        )
        response.raise_for_status()  # Raise an exception for bad responses
        token = response.json()['data']['token']
        return jsonify({"token": token})
    except requests.RequestException as error:
        print(f'Error retrieving access token: {error}')
        return jsonify({"error": "Failed to retrieve access token"}), 500

if __name__ == '__main__':
    app.run(port=3001)