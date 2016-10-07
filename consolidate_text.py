import app
from app.models import Chat, Text

db = app.db


def consolidate_text(email):
    """ This takes all chats from `email` and consolidates them
    into one text field. This makes it easier to do full text searches.

    Note: it doesn't append, but replaces everything in Text.text. but
    it's fast. whatever.
    """
    chats = Chat.query.filter_by(sender=email).all()

    print("Getting all text.")
    all_text = ""
    for chat in chats:
        all_text += u" {}".format(chat.text)

    print("Creating new Text entry.")
    existing = Text.query.filter_by(sender=email).first()
    if existing:
        existing.text = all_text
    else:
        new_text = Text(sender=email, text=all_text)
        db.session.add(new_text)

    db.session.commit()
    print("Finished consolidating text for {}".format(email))


if __name__ == "__main__":
    users = [
        "mskeving@gmail.com",
        "philrha@gmail.com",
    ]
    for u in users:
        consolidate_text(u)
