from .app import db

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)  
    password = db.Column(db.String(150))
    # notes = db.relationship('Note')

    def __init__(self, iusername, iemail, ipassword):
        self.username = iusername
        self.email = iemail
        self.password = ipassword


