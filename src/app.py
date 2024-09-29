from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress warnings
db = SQLAlchemy(app)

# Models
class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Add a primary key
    username = db.Column(db.String(15), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)

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
                new_user = Signup(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login')) # Redirect to login if the user signed up succesfully
            else:
                return redirect(url_for('signup_page')) # For now, if the the username and or password was empty redirect to signup again.
    except BaseException as e:
        print(f'Error: {e}')
        return render_template('error.html')
    
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

@app.route('/post')
def post():
    return render_template('post.html')

if __name__ == '__main__':
    app.run(debug=True)
