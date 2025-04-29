from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import datetime
import random
import string

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create a directory for storing CSV files if it doesn't exist
os.makedirs('responses', exist_ok=True)

@app.route('/')
def home():
    return "Server is running"

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        ratings = data.get('ratings', [])
        country = data.get('country', 'Unknown')
        completion_code = data.get('completion_code', '')
        is_debug = data.get('debug', False)
        country_id = data.get('country_id', 'unknown')
        
        if not ratings:
            return jsonify({"error": "No ratings provided"}), 400
        
        # Sort ratings by index
        ratings.sort(key=lambda x: int(x.get('index', 0)))
        
        # Get current timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename with prefix based on debug mode
        prefix = 'debug_' if is_debug else ''
        filename = f'{prefix}ratings_{completion_code}_{country_id}_{timestamp}.csv'
        filepath = os.path.join('responses', filename)
        
        # Write to CSV
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['index', 'input_cultural', 'output_cultural', 'input_text', 'output_text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for rating in ratings:
                writer.writerow({
                    'index': rating.get('index', ''),
                    'input_cultural': rating.get('input_cultural', ''),
                    'output_cultural': rating.get('output_cultural', ''),
                    'input_text': rating.get('input_text', ''),
                    'output_text': rating.get('output_text', '')
                })
        
        return jsonify({"success": True, "message": "Ratings saved successfully", "filename": filename})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # In production, don't use debug mode
    app.run(host='0.0.0.0', port=5050, debug=False) 