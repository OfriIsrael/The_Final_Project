from Crypto.Random import get_random_bytes
from flask import Flask, render_template, url_for, request, redirect, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from Data import db, User, Map
from werkzeug.serving import run_simple
import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from App_Python_Cmds import *

import socket

# default database setup
app = Flask(__name__)
app.secret_key = get_random_bytes(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# default log-in startup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'unlogged_starting_page'


# command for returning user information
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Logs out of the website once user requests
@app.route("/Logout")
@login_required
def Logout():
    logout_user()
    return redirect(url_for('unlogged_starting_page'))


# basic website entery page
@app.route("/", methods=['POST', 'GET'])
def unlogged_starting_page():
    return render_template('unlogged_Opening_Page.html')


# api request to return the user files which he can create maps from
@app.route("/api/get_template_files", methods=['POST'])
def get_template_files():
    folder_path = 'C:/The_Final_Project (2)/The_Final_Project/static'
    file_names = get_all_file_names(folder_path)
    file_amount = len(file_names)
    return jsonify({"path_list": file_names})


# api request to return the user files which he can play
@app.route("/api/get_play_files", methods=['POST'])
def get_play_files():
    paths = Map.query.with_entities(Map.path).all()
    filename_list = [os.path.basename(path) for (path,) in paths]
    file_amount = len(filename_list)
    return jsonify({"path_list": filename_list})


# used to handle the registration process, does many checks to make sure input is correct
# and then registers the user to the website and its database and sends him to the opening page
@app.route("/unlogged_registration_page", methods=['POST', 'GET'])
def unlogged_registration_page():
    if request.method == 'POST':
        user_name = request.form['Username']
        user_password = request.form['Password']
        user_cpassword = request.form['Confirm_Password']
        user_Email = request.form['Email']
        user_Age = request.form['Age']

        if (user_Age == "" or user_name == "" or user_password == "" or user_Age == "" or user_cpassword == ""):
            return render_template('unlogged_registration_page.html', msg='Please enter all fields', Username=user_name,
                                   Password=user_password, Confirm_Password=user_cpassword, Email=user_Email,
                                   Age=user_Age)

        Year_Of_Birth = int(user_Age[0:4])
        if (Year_Of_Birth < 1900):
            return render_template('unlogged_registration_page.html', msg='Please enter Valid Age', Username=user_name,
                                   Password=user_password, Confirm_Password=user_cpassword, Email=user_Email,
                                   Age=user_Age)

        if (6 > datetime.datetime.now().year - Year_Of_Birth):
            return render_template('unlogged_registration_page.html', msg='Must be around the age of 6 or more to play',
                                   Username=user_name, Password=user_password, Confirm_Password=user_cpassword,
                                   Email=user_Email, Age=user_Age)

        if (len(user_password) < 6):
            return render_template('unlogged_registration_page.html', msg='Password Must be longer than 6 characters',
                                   Username=user_name, Password=user_password, Confirm_Password=user_cpassword,
                                   Email=user_Email, Age=user_Age)
        if (len(user_name) < 6):
            return render_template('unlogged_registration_page.html', msg='Username Must be longer than 6 characters',
                                   Username=user_name, Password=user_password, Confirm_Password=user_cpassword,
                                   Email=user_Email, Age=user_Age)
        if (user_cpassword == user_password):
            pass
        else:
            return render_template('unlogged_registration_page.html', msg='Passwords do not match', Username=user_name,
                                   Password=user_password, Confirm_Password=user_cpassword, Email=user_Email,
                                   Age=user_Age)

        user = User.query.filter_by(name=user_name).first()
        if (user is None):
            has_email = User.query.filter_by(email=user_Email).first()
            if (has_email is None):
                user_password = generate_password_hash(request.form['Password'])
                User_Info = User(name=user_name, password=user_password, email=user_Email, Age=user_Age)
                db.session.add(User_Info)
                db.session.commit()
                user = User.query.filter_by(name=user_name).first()
                login_user(user)
                return render_template('Opening_Page.html')
            else:
                return render_template('unlogged_registration_page.html', msg='email already exists',
                                       Username=user_name, Password=user_password, Confirm_Password=user_cpassword,
                                       Email=user_Email, Age=user_Age)
        else:
            return render_template('unlogged_registration_page.html', msg='user already exists', Username=user_name,
                                   Password=user_password, Confirm_Password=user_cpassword, Email=user_Email,
                                   Age=user_Age)
    else:
        return render_template('unlogged_registration_page.html')


# used to handle the user's login process, and if he's correct, redirects him to the opening page
@app.route("/unlogged_login", methods=['POST', 'GET'])
def unlogged_login():
    if request.method == 'POST':
        user_name = request.form['Username']
        user_password = request.form['Password']
        if (user_name == "" or user_password == ""):
            return render_template('unlogged_login.html', msg="Please Enter All Fields", Username=user_name,
                                   Password=user_password)

        UserData = User.query.filter_by(name=user_name).first()
        if (UserData != None):
            if (check_password_hash(UserData.password, user_password)):
                user = User.query.filter_by(name=user_name).first()
                login_user(user)
                return render_template('Opening_Page.html')
            else:
                return render_template('unlogged_login.html', msg="Login Credentials Incorrect", Username=user_name,
                                       Password=user_password)
        else:
            return render_template('unlogged_login.html', msg="Login Credentials Incorrect", Username=user_name,
                                   Password=user_password)
    else:
        return render_template('unlogged_login.html')


# redirects user to the logged opening page
@app.route("/start", methods=['POST', 'GET'])
@login_required
def starting_page():
    return render_template('Opening_Page.html')


# redirects user to the file uploading page
@app.route("/create_map", methods=['POST', 'GET'])
@login_required
def create_map():
    return render_template('create_map.html')


# function which recieves the user's uploaded file and does many procedures to make sure it doesnt have
# malware, and then sends it to the unsafe_files folder for the admins to check
@app.route('/upload_file', methods=['POST'])
@login_required
def upload():
    uploaded_file = request.files['file']
    if uploaded_file:
        file_size = len(uploaded_file.read())
        uploaded_file.seek(0)
        max_file_size = 10 * 1024 * 1024  # 10 MB
        if file_size > max_file_size:
            return render_template('create_map.html', msg="File size exceeds limit")
        if not allowed_file(uploaded_file.filename):
            return render_template('create_map.html', msg="File type not allowed")
        #uploaded_file.save('The_Final_Project/Unsafe_Files_Server/' + uploaded_file.filename) for checks in sockets
        uploaded_file.save('The_Final_Project/static/' + uploaded_file.filename)
        return render_template('create_map.html', msg="File Uploaded Successfully! wait a bit until map gets accepted")
    else:
        return render_template('create_map.html', msg=" No File Uploaded ")


# function to handle the creation on the map
@app.route('/map_maker', methods=['POST', 'GET'])
@login_required
def map_maker():
    if request.method == 'POST':
        data = request.get_json()
        link_text = data.get('link_text')
        current_user.current_map = link_text
        db.session.commit()
        return jsonify({"status": "success", "received": link_text})
    else:
        return render_template('map_maker.html', file=current_user.current_map)


# used to redirect the user to the actual game based on the map he chose
@app.route('/game', methods=['POST', 'GET'])
@login_required
def game():
    global link
    if request.method == 'POST':
        data = request.get_json()
        link_text = data.get('link_text')
        link = link_text
        current_user.current_map = link
        db.session.commit()
        return jsonify({"status": "success", "received": link_text})
    else:
        # works when entered directly

        return render_template('game.html', file=link)


# used to re-dirent the user to the template gallery from which he choose a map to edit
@app.route("/Template_Gallery", methods=['POST', 'GET'])
@login_required
def Template_Gallery():
    return render_template('Template_Gallery.html')


# redirects user to the playable map gallery
@app.route('/play', methods=['POST', 'GET'])
@login_required
def play():
    return render_template('play.html')


# redirects user to the profile page
@app.route('/Profile', methods=['POST', 'GET'])
@login_required
def Profile():
    return render_template('Profile.html')


# api request to return the user's info
@app.route("/api/get_profile_info", methods=['POST'])
def get_profile_info():
    return jsonify({"username": current_user.name, "email": current_user.email})


# creates a new map and adds it to the database
@app.route('/api/map_creation', methods=['POST'])
def map_creation():
    data = request.json
    map_points = data.get('MAP_POINTS')
    map_name = data.get('MAP_NAME')
    map_link = os.path.basename(data.get('MAP_LINK'))
    New_Map = Map(name=map_name, path=map_link, map_points=map_points)
    db.session.add(New_Map)
    db.session.commit()


# gets the points of a created map and sends it to the game
@app.route("/api/get_game_points", methods=['POST', 'GET'])
@login_required
def get_game_points():
    MAP_POINTS = Map.query.filter_by(
        path=current_user.current_map).first().map_points
    return jsonify({"map_name": current_user.current_map, "map_points": MAP_POINTS})


@app.route("/change_account_info", methods=['POST', 'GET'])
@login_required
def change_account_info():
    if request.method == 'POST':
        user_name = request.form['Username']
        user_password = request.form['Password']
        user_cpassword = request.form['Confirm_Password']
        user_Email = request.form['Email']

        if (user_password != '' and user_cpassword != ''):
            if (len(user_password) < 6):
                return render_template('change_account_info.html', msg='Password Must be longer than 6 characters',
                                       Username=user_name, Password=user_password, Confirm_Password=user_cpassword,
                                       Email=user_Email)
            if (user_cpassword != user_password):
                return render_template('change_account_info.html', msg='Passwords do not match', Username=user_name,
                                       Password=user_password, Confirm_Password=user_cpassword, Email=user_Email)
        else:
            if (user_password != '' or user_cpassword != ''):
                return render_template('change_account_info.html', msg='Please fill both password fields',
                                       Username=user_name,
                                       Password=user_password, Confirm_Password=user_cpassword, Email=user_Email)

        if (user_name != ""):
            if (len(user_name) < 6):
                return render_template('change_account_info.html', msg='Username Must be longer than 6 characters',
                                       Username=user_name, Password=user_password, Confirm_Password=user_cpassword,
                                       Email=user_Email)

        user = User.query.filter_by(name=user_name).first()
        if (user is None):
            has_email = User.query.filter_by(email=user_Email).first()
            if (has_email is None):
                if (user_password != ''):
                    current_user.password = generate_password_hash(user_password)
                if (user_name != ''):
                    current_user.name = user_name
                if (user_Email != ''):
                    current_user.email = user_Email
                db.session.commit()
                login_user(current_user)
                return render_template('change_account_info.html', msg='Account Info Changed Successfully!')
            else:
                return render_template('change_account_info.html', msg='Email already exists',
                                       Username=user_name, Password=user_password, Confirm_Password=user_cpassword,
                                       Email=user_Email)
        else:
            return render_template('change_account_info.html', msg='User already exists', Username=user_name,
                                   Password=user_password, Confirm_Password=user_cpassword, Email=user_Email)
    else:
        return render_template('change_account_info.html')


@app.route("/api/delete_user", methods=['POST', 'GET'])
@login_required
def delete_user():
    deleted_user = User.query.filter_by(id=current_user.id).first()
    logout_user()
    db.session.delete(deleted_user)
    db.session.commit()
    return render_template('unlogged_Opening_Page.html')


# runs the flask server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    run_simple('0.0.0.0', 5000, app, threaded=True)
