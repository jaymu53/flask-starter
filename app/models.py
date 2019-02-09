from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.column(db.String(128))
    email = db.Column(db.String(128), index = True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()


    
