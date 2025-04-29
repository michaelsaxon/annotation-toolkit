from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import random
import string
from datetime import datetime
import traceback
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ensure data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def generate_completion_code():
    """Generate a random 4-character code"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

def read_prompts(prompt_file):
    try:
        with open(prompt_file, 'r') as f:
            return [line.strip() for line in f]
    except Exception as e:
        app.logger.error(f"Error reading prompts file: {str(e)}")
        return None

@app.route('/')
def home():
    return "Server is running"

@app.route('/submit', methods=['POST'])
def submit_ratings():
    try:
        # Get the ratings data
        data = request.json
        if not data or 'ratings' not in data:
            return jsonify({
                'success': False,
                'error': 'No ratings data received'
            }), 400
        
        app.logger.info(f"Received data: {data}")
        
        # Extract ratings and metadata
        ratings = data['ratings']
        source = data.get('image_source', 'FLUX-country')
        annotator_country = data.get('annotator_country', 'XX')  # Default if not provided
        
        # Filter out example ratings
        image_ratings = {k: v for k, v in ratings.items() if k.startswith('rating_')}
        
        # Generate timestamp and completion code
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        completion_code = generate_completion_code()
        
        # Create CSV filename with annotator country code
        filename = f'ratings_{annotator_country}_{source}_{completion_code}_{timestamp}.csv'
        filepath = os.path.join(DATA_DIR, filename)
        
        # Convert ratings dict to rows
        rows = []
        for rating_key, value in image_ratings.items():
            try:
                # Parse the key format "rating_concept_country"
                parts = rating_key.split('_')
                if len(parts) != 3 or parts[0] != 'rating':
                    raise ValueError(f"Invalid rating key format: {rating_key}")
                concept, country = parts[1], parts[2]
                rows.append([concept, country, value])
            except Exception as e:
                app.logger.error(f"Error processing rating {rating_key}: {str(e)}")
                raise
            
        # Write to CSV
        try:
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['concept', 'country', 'score'])  # New header
                writer.writerows(rows)
                app.logger.info(f"Successfully wrote {len(rows)} ratings to {filename}")
        except Exception as e:
            app.logger.error(f"Error writing to CSV: {str(e)}")
            raise
            
        return jsonify({
            'success': True,
            'completion_code': completion_code
        })
        
    except Exception as e:
        app.logger.error(f"Error in submit_ratings: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 