from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
app = Flask(__name__)
@app.route('/')
def index():
   return render_template('index.html')
@app.route('/submit', methods=['POST'])
def submit():
   data = request.form.to_dict()
   data['timestamp'] = str(datetime.now())
   with open('data.json', 'a') as f:
       json.dump(data, f)
       f.write('\n')
   return jsonify({"message": "Inquiry received successfully!"})
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)