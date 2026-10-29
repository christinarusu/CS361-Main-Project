from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import pickle
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if os.path.exists("user_credentials.json"):
    with open("user_credentials.json", "rb") as user_credentials:
        user_dict = pickle.load(user_credentials)
else:
     user_dict = {}
@app.route('/', methods=['GET', 'POST'])
def welcome():
    message = None
    # if the user clicks the register button
    if request.form.get('action') == 'Register':
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            password2 = request.form.get('password2')
            if password == password2:
                if email not in user_dict.keys():
                    user_dict[email] = password
                    message = "You are now registered!"
                    with open("user_credentials.json", "wb") as user_credentials:
                        pickle.dump(user_dict, user_credentials)
                    return render_template('index.html', message=message )
                else:
                    message = "A user has already registered with this email!"
                    return render_template('index.html', message=message )
            else:
                message = "Passwords do not match"
        return render_template('index.html', message=message)
    
    # if the user clicks the login button
    login_tracker = 0
    if request.form.get('action') == 'Login':
        if request.form.get("log_email") not in user_dict:
            message = "This email has not been registered!"
            return render_template('index.html', message=message )
        if request.form.get('log_email') in user_dict:
            if request.form.get('log_password') == user_dict[request.form.get('log_email')]:
                message = "Login Successful!"
                login_tracker = 1
                return render_template('home.html', message=message )
            else:
                message = "Email or Password do not match"

    return render_template('index.html', message=message)

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
    
if __name__ == "__main__":
    app.run(debug=True)