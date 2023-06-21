from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    request, 
    flash,
    session
)
import secrets
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
from flask_migrate import Migrate
from datetime import timedelta
import time
from slugify import slugify
import uuid
import jwt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask import jsonify

#config
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flask_blog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.permanent_session_lifetime = timedelta(days = 1)


#login managing
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#models
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    _id = db.Column('id',db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)  
    password = db.Column(db.String(150))
    
    def __init__(self, iusername, iemail, ipassword):
        self.username = iusername
        self.email = iemail
        self.password = ipassword

    def get_id(self):
        return str(self._id)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column('id',db.Integer, primary_key=True)
    title = db.Column('title',db.String(100))
    text = db.Column(db.String(500))
    slug = db.Column(db.String(100))
    author = db.Column(db.String(50))

    def generate_unique_slug(slef):
        unique_id = str(uuid.uuid4())
        newslug = slugify(unique_id)
        return newslug
    

    def __init__(self, text, iuser, ititle):
        self.author = iuser
        self.text = text
        self.title = ititle
        self.slug = self.generate_unique_slug()
    

#views
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            flash(f'password is not match !')
            return render_template("signup.html")
        
        founded_user = User.query.filter_by(username=username).first()
        if founded_user:
            flash(f'username has been used !')
            return render_template("signup.html")
        else:
            new_user = User(iusername=username, iemail=email, ipassword=password)
            db.session.add(new_user)
            db.session.commit()

        session["user"] = username

        flash(f'Signup successful for user: {username}', 'success')
        return redirect(url_for('login'))  

    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        founded_user = User.query.filter_by(username=username, password=password).first()

        if founded_user:
            flash(f'login successful for user: {username}', 'success')
            session["user"] = username
            session["password"] = password
            session["email"] = founded_user.email
            time.sleep(5)
            print(session['user'])
            login_user(founded_user)
            return redirect(url_for('home')) 
            
            
        else:
            flash('username or password is incorrect!')
            print("not exist")
            return render_template("signin.html")
        
    return render_template("signin.html")

@app.route('/article/<slug>', methods=['GET'])
@login_required
def article_detail(slug):
    post = Article.query.filter_by(slug = slug).first()
    if post:
        return render_template("article_detail.html", post=post)


@app.route('/')
def home():
    print(get_objects_count())
    articles = Article.query.all()
    
    user_own = session.get('user')
    

    return render_template("article_list.html", content=articles , user= user_own)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        print(session["user"], '\n', content)
        new_article = Article(ititle= title, text= content, iuser= session.get("user"))
        db.session.add(new_article)
        db.session.commit()
        flash(f'your content has been posted !')
        time.sleep(5)
        return redirect(url_for('home')) 
    
    return render_template("create.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))


@app.route('/objects/count', methods=['GET'])
@login_required
def get_objects_count():
    count = User.query.count()
    
    return str(count)

if __name__ == "__main__":
    app.run(debug=True)
