from flask import Flask, request, jsonify, render_template
import csv
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Configuration
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        responses = request.form.get('responses')
        image_id = request.form.get('image_id')
        
        if not responses or not image_id:
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Parse responses
        responses = json.loads(responses)
        
        # Generate confirmation code
        confirmation_code = str(uuid.uuid4())
        
        # Write to CSV
        timestamp = datetime.now().isoformat()
        csv_file = os.path.join(OUTPUT_DIR, f'annotations_{datetime.now().strftime("%Y%m%d")}.csv')
        
        file_exists = os.path.exists(csv_file)
        
        with open(csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'image_id', 'question_id', 'rating', 'confirmation_code'])
            
            if not file_exists:
                writer.writeheader()
                
            for question_id, rating in responses.items():
                writer.writerow({
                    'timestamp': timestamp,
                    'image_id': image_id,
                    'question_id': question_id,
                    'rating': rating,
                    'confirmation_code': confirmation_code
                })
        
        return jsonify({
            'status': 'success',
            'confirmation_code': confirmation_code
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 