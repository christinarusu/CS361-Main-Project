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
    # Determines purse dictionary exists 
    if os.path.exists("purses.json"):
        with open("purses.json", "rb") as purse_dict:
            purses = pickle.load(purse_dict)
    #If no user directory exits, initiate one
    else:
        purse_dict = {
            "1": {
                "name": "Coach Brown Leather Mia Bag",
                "color": "brown, tan",
                "serial": "M1382-1111A",
                "price": "$150",
                "img": "../static/img/1.jpg"
            },
            "2": {
                "name": "Coach Purple Demi Stripe Bag",
                "color": "purple, tan",
                "serial": "M1382-28206E",
                "price": "$125",
                "img": "../static/img/2.jpg"
            },
            "3": {
                "name": "Coach Red Leather Bleeker Bag",
                "color": "red, burgundy",
                "serial": "M1382-3333C",
                "price": "$175",
                "img": "../static/img/3.jpg"
            },
            "4": {
                "name": "Coach Brown Ergo Kisslock Bag",
                "color": "brown",
                "serial": "M1382-4444D",
                "price": "$195",
                "img": "../static/img/4.jpg"
            },
            "5": {
                "name": "Coach Black Signature Clasp Bag",
                "color": "black",
                "serial": "M1382-5555E",
                "price": "$75",
                "img": "../static/img/5.jpg"
            },
            "6": {
                "name": "Coach Brown Signature Mia Bag",
                "color": "brown",
                "serial": "M1382-6666F",
                "price": "$160",
                "img": "../static/img/6.jpg"
            },
            "7": {
                "name": "Coach Tan Belted Ergo Bag",
                "color": "tan",
                "serial": "M1382-7777G",
                "price": "$180",
                "img": "../static/img/7.jpg"
            }
        }
        with open("purses.json", "wb") as purses:  # adds purses to json file
            pickle.dump(purse_dict, purses)
        purses = purse_dict
    # implements search function for purse color, name, or serial number
    if request.form.get('action') == 'search':  
        search_purses = {}
        if request.method == 'POST':
            search_request = request.form.get("search").strip().lower()  # controls for capitalization
            for key, val in purses.items():
                if search_request in val['name'].lower() or search_request in val['serial'].lower():
                    search_purses[key] = val  # adds purse matching search to new dictionary
            if not search_purses:
                return render_template('home.html', purses=purses)
            else:
                return render_template('home.html', purses=search_purses)
    return render_template('home.html', purses=purses)
    
@app.route('/logout')
def logout():
    #clears session if user presses logout
    session.clear()
    return render_template('index.html')

@app.route('/help')
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

    #pulls user info to be rendered on the account page
    user_info = {
        "name": matched_user.get("name"),
        "email": matched_user.get("email"),
        "address": matched_user.get("address"),
        }

    return render_template("account.html", user=user_info)

@app.route("/buy/<bag_id>", methods=["GET", "POST"])
def buy(bag_id):
    with open("purses.json", "rb") as purse_dict:
        purses = pickle.load(purse_dict)
        selected_purse = purses.get(bag_id) # purse that user clicked on
        message = "Are you sure you want to purchase this bag? " \
        "Once purchased, your account will be charged the total amount"
        return render_template("buy.html", bag=selected_purse, message=message)
    
if __name__ == "__main__":
    app.run(debug=True)