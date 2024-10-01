# Made by najasnake12
# also known as the official -10x developer.
# Shoutout to Chris Sawyer


from flask import Flask, render_template, request, redirect, url_for
import hashlib

app = Flask(__name__)

users_file = 'C:/Users/pessi/OneDrive/Desktop/Social Media For Keyboards/src/instance/users.txt' # For now the database is in a txt file, probably going to change this later

# Routes
@app.route('/')
def index():
    return render_template('feed.html')

@app.route('/feed')
def feed():
    return render_template('feed.html')

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
                        
                        file.write(f'{username},{hashed_password}')
                except BaseException as e:
                    print(f'Error: {e}')
                    return render_template('error.html')
                    # maybe also give them a small message that they signed up?
                return redirect(url_for('login_page')) # Redirect to login if the user signed up succesfully
            else:
                return redirect(url_for('signup_page')) # For now, if the the username and or password was empty redirect to signup again.
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
            with open(users_file, 'r') as file:
                
                for line in file:
                    stored_username, stored_password = line.strip().split(',')
                    
                    check_if_user_entered_the_correct_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

                    if stored_username == username and stored_password == check_if_user_entered_the_correct_password:
                        return render_template('my_account.html')
                else:
                    return render_template('error1.html')
                    
        except BaseException as e:
            print(f'Error: {e}')
            return render_template('error.html')
        
    return render_template('login.html')

@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

@app.route('/post')
def post():
    return render_template('post.html')

if __name__ == '__main__':
    app.run(debug=True)
