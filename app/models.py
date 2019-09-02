from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, logout_user


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    weigh_ins = db.relationship('WeighIn', backref='weighee', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
class WeighIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float(4))
    bf = db.Column(db.Float(4))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<WeighIn {}-{}>'.format(self.weighee.username,self.timestamp)
        
    def __init__(self,user_id,weight,bf,date,time):
        self.user_id = user_id
        self.weight = weight
        self.bf = bf
        self.timestamp = datetime.combine(date=date,time=datetime.time(time))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))