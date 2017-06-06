from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    timing = db.Column(db.DateTime  , nullable=False)

    def __init__(self,username,content,state,timing):
        self.username=username
        self.content=content
        self.state=state
        self.timing=timing

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password