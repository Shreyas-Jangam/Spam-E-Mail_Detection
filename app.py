from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

# Load models
try:
    with open('Pickle Files/feature.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    with open('Pickle Files/model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading models: {e}")
    tfidf = None
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        email_text = data.get('email_text', '')
        
        if not email_text.strip():
            return jsonify({'error': 'Please enter an email message to analyze.'})
        
        if tfidf is None or model is None:
            return jsonify({'error': 'Model not loaded properly.'})
        
        # Transform and predict
        vector_input = tfidf.transform([email_text])
        result = model.predict(vector_input)[0]
        
        if result == 0:
            return jsonify({
                'result': 'spam',
                'message': 'SPAM DETECTED! This email appears to be spam.',
                'warning': 'This message has characteristics commonly found in spam emails. Please be cautious and avoid clicking any links or providing personal information.'
            })
        else:
            return jsonify({
                'result': 'ham',
                'message': 'LEGITIMATE EMAIL - This email appears to be genuine.',
                'warning': 'This message appears to be a legitimate email. However, always exercise caution with unknown senders.'
            })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)