import os
import json
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas Connection String
MONGO_URI = os.getenv("MONGO_URI")

# Initialize MongoDB Client
try:
    if not MONGO_URI:
        raise Exception("MONGO_URI not found in environment variables. Please check your .env file.")
    
    client = MongoClient(MONGO_URI)
    # Use 'tutedude_db' as the database name
    db = client.get_database('tutedude_db')
    collection = db.submissions
    # Test connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def get_api_data():
    """Returns JSON list read from data.json"""
    try:
        data_file_path = os.path.join(os.path.dirname(__file__), 'data.json')
        with open(data_file_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "data.json file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding data.json"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit_data():
    """Inserts data into MongoDB Atlas and redirects or shows error"""
    name = request.form.get('name')
    message = request.form.get('message')

    if not name or not message:
        return render_template('index.html', error="All fields are required.")

    try:
        # Check if client is initialized
        if 'client' not in globals() or client is None:
            raise Exception("MongoDB client not initialized. Please check your connection string.")

        # Insert into MongoDB
        submission = {
            "name": name,
            "message": message
        }
        collection.insert_one(submission)
        
        # On success, redirect to success page
        return redirect(url_for('success'))

    except PyMongoError as e:
        # On database error, display on same page
        return render_template('index.html', error=f"Database error: {str(e)}")
    except Exception as e:
        # On other errors, display on same page
        return render_template('index.html', error=f"Error: {str(e)}")

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
