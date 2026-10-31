#Christina Rusu

from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
import pickle
import os

#Initiates Flask App
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Determines user credentials and if they have registered or need to register
if os.path.exists("user_credentials.json"):
    with open("user_credentials.json", "rb") as user_credentials:
        user_dict = pickle.load(user_credentials)

#If no user directory exits, initiate one
else:
     user_dict = {}
@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    # if the user clicks the register button
    if request.form.get('action') == 'Register':
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            password2 = request.form.get('password2') #confirm password
            name = request.form.get('name')
            address = request.form.get('address')
            if password == password2:  # if passwords match
                if email not in user_dict.keys(): # if user has not previously registered
                    user_dict[email] = {
                        "password": password,
                        "name": name,  # Default username from email
                        "email": email,
                        "address": address}
                    message = "You are now registered!"
                    with open("user_credentials.json", "wb") as user_credentials:
                        pickle.dump(user_dict, user_credentials)
                    return render_template('index.html', message=message )
                else: # if user email has already been registered
                    message = "A user has already registered with this email!"
                    return render_template('index.html', message=message )
            else:  # if passwords do not match
                message = "Passwords do not match"
        return render_template('index.html', message=message)
    
    # if the user clicks the login button
    if request.form.get('action') == 'Login':
        if request.form.get("log_email") not in user_dict:  # if user not registered
            message = "This email has not been registered!"
            return render_template('index.html', message=message )
        if request.form.get('log_email') in user_dict:
            #compares login password input to stored user password
            if request.form.get('log_password') == user_dict[request.form.get('log_email')].get("password"):
                session['login_tracker'] = '1'
                session['log_email'] = request.form.get('log_email')
                message = "Login Successful!"
                return render_template('index.html', message=message)
            else:
                message = "Email or Password do not match"
    return render_template('index.html', message=message)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.form.get('action') == 'Search':
        if request.form.get("search"):
            return render_template('home.html')
    return render_template('home.html')
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    #clears session if user presses logout
    session.clear()
    return render_template('index.html')

@app.route('/help', methods=['GET', 'POST'])
def help():
    return render_template('help.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    #makes sure only logged in user can access account info
    if "log_email" not in session:
        return render_template("index.html")
    
    email = session.get("log_email")
    #pulls user info from credential directory based on session email
    matched_user = user_dict.get(email) 
    if not matched_user:
        session.clear()
        return redirect(url_for("index"))

  # 2. Check if pickle returned a structured dictionary or an old password string
    user_info = {
        "name": matched_user.get("name"),
        "email": matched_user.get("email"),
        "address": matched_user.get("address"),
        }

    return render_template("account.html", user=user_info)

    
if __name__ == "__main__":
    app.run(debug=True)