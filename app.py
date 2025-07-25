from flask import Flask, request, jsonify, render_template
from wipo_selenium_fetcher import fetch_wipo_with_selenium
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('PCT_Estimator.html')

@app.route('/fetch_wipo', methods=['POST'])
def fetch_wipo():
    data = request.json
    pct_number = data.get('pct_number')
    if not pct_number:
        return jsonify({'error': 'No PCT number provided'}), 400
    result = fetch_wipo_with_selenium(pct_number)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
