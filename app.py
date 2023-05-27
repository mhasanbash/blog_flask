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


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flask_blog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.permanent_session_lifetime = timedelta(days = 1)


class User(db.Model):
    __tablename__ = 'users'
    _id = db.Column('id',db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)  
    password = db.Column(db.String(150))
    
    def __init__(self, iusername, iemail, ipassword):
        self.username = iusername
        self.email = iemail
        self.password = ipassword



class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column('id',db.Integer, primary_key=True)
    title = db.Column('title',db.String(100))
    text = db.Column(db.String(500))
    slug = db.Column(db.String(100))
    author = db.Column(db.String(50))


    def __init__(self, text, iuser, ititle):
        self.user = iuser
        self.text = text
        self.title = ititle
    


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
            return redirect(url_for('home')) 
            
            
        else:
            flash('username or password is incorrect!')
            print("not exist")
            return render_template("signin.html")
        
    return render_template("signin.html")


@app.route('/')
def home():
    articles = Article.query.all()

    return render_template("article_list.html", content=articles)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        print(session["user"], '\n', content)
        new_article = Article(ititle= title, text= content, iuser= session["user"])
        db.session.add(new_article)
        db.session.commit()
        flash(f'your content has been posted !')
        time.sleep(5)
        return redirect(url_for('home')) 
    
    return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)


