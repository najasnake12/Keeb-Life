from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from flask_session import Session
import os
from PIL import Image
import time

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users_file = 'C:/Users/pessi/OneDrive/Desktop/Social Media For Keyboards/Keeb-Life/src/instance/users.txt'
img_folder = 'C:/Users/pessi/OneDrive/Desktop/Social Media For Keyboards/Keeb-Life/src/static/images'
posts = 'C:/Users/pessi/OneDrive/Desktop/Social Media For Keyboards/Keeb-Life/src/instance/posts.txt'

@app.route('/')
def index():
    return render_template('feed.html')

@app.route('/feed')
def feed():
    pass
    # show the posts to the feed :)
    # remember to pass the variable to the template
    
@app.route('/signup_page', methods=['GET', 'POST'])
def signup_page():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
        
            if username and password:
                try:
                    with open(users_file, 'a') as file:
                        sha256_hash = hashlib.sha256()
                        sha256_hash.update(password.encode('utf-8'))
                        hashed_password = sha256_hash.hexdigest()
                        file.write(f'{username},{hashed_password}\n')  # Add newline to avoid writing all users on one line
                except BaseException as e:
                    print(f'Error: {e}')
                    return render_template('error.html')

                return redirect(url_for('login_page'))
            else:
                return redirect(url_for('signup_page')) 
    except BaseException as e:
        print(f'Error: {e}')
        return render_template('error.html')
    
    return render_template('signup.html')

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            with open(users_file, 'r', encoding='utf-8') as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(',')
                    check_if_user_entered_the_correct_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

                    if stored_username == username and stored_password == check_if_user_entered_the_correct_password:
                        session["username"] = username  # create the session if the user logged in
                        # Perhaps give the user a message if they logged in with no issues?
                        return redirect(url_for('my_account'))
                else:
                    return render_template('error1.html')
                    
        except BaseException as e:
            print(f'Error: {e}')
            return render_template('error.html')
        
    return render_template('login.html')

@app.route('/my_account')
def my_account():
    if "username" in session:
        return render_template('my_account.html', username=session["username"])  # pass the username to the template
    else:
        return render_template('error.html')


@app.route("/logout")
def logout():
    session.pop("username", None)  # clear the session
    return redirect(url_for('index'))

@app.route('/post', methods=['GET', 'POST'])
def post():
    title = ""
    description = ""
    resized_image = None
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            image = request.files.get('image')
            
            if image:
                    
                # extract the image name and extension
                image_name, file_extension = os.path.splitext(image.filename)
                image_name = f"{image_name}_{int(time.time())}{file_extension}"
                image_path = os.path.join(img_folder, image_name)

                # resize the image
                open_image = Image.open(image)
                dimension = (1000, 1000)
                resized_image = open_image.resize(dimension)
                resized_image.save(image_path)  # save the resized image
                
                with open(posts, 'a') as file:
                    file.write(f'{title},{description},{image_name}\n')
            
            else:
                with open(posts, 'a') as file:
                    file.write(f'{title},{description},no_image\n')
                
        except BaseException as e:
            print(f'Error: {e}')
            return render_template('error.html')
    
    return render_template('post.html')



if __name__ == '__main__':
    app.run(debug=True)
