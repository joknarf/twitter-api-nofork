from datetime import datetime
from app import db

class Tweet(db.Model):
    __table__name = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Tweet #{self.id}>"

class User(db.Model):
    __table__name = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(280))
    api_token = db.Column(db.String(280))
    children = db.relationship("Tweet")
