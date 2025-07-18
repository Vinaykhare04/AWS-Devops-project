from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'Vinay@1234'

# Helper to load/save users
def load_users():
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump([], f)
    with open('users.json') as f:
        return json.load(f)

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        email = request.form['email']
        password = request.form['password']
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['user'] = email
                return redirect(url_for('index'))
        flash("Please register first or check your credentials.", "error")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        email = request.form['email']
        password = request.form['password']
        # Check if user exists
        if any(u['email'] == email for u in users):
            flash("Email already registered.", "error")
            return redirect(url_for('register'))
        users.append({'email': email, 'password': password})
        save_users(users)
        flash("Registered successfully! Please login.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/enquiry')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit():
    if 'user' not in session:
        return jsonify({"message": "Unauthorized!"}), 401
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
