from app import db


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String(128), unique=True)
    thread_id = db.Column(db.String(128))
    data = db.Column(db.Text())
    text = db.Column(db.Text())
    send_time = db.Column(db.String(64))  # unix
    sender = db.Column(db.String(128))


class Text(db.Model):
    __tablename__ = "text"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    sender = db.Column(db.String(128))
