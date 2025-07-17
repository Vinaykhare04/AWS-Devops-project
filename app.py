from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    data['timestamp'] = str(datetime.now())

    if not os.path.exists("data.json"):
        with open("data.json", "w") as f:
            json.dump([], f)

    with open("data.json", "r+") as f:
        current = json.load(f)
        current.append(data)
        f.seek(0)
        json.dump(current, f, indent=4)

    return jsonify({"message": "Inquiry received successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
