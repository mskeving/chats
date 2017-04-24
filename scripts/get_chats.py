import base64
import json
import re
import sys

from apiclient import errors

import app
from app.models import Chat
from gmail_api import GmailApi

service = GmailApi().get_service()

# Sender comes in as "FirstName LastName <email@address.com>".
# Keep the email address.
email_regex = re.compile('<(.*?)>')

db = app.db
CHUNK_SIZE = 200


def get_message_ids(q):

    print("finding new message ids...")

    try:
        response = service.users().messages().list(userId='me', q=q).execute()
    except errors.HttpError as error:
        print("An error occurred: {}".format(error))

    if not response.get('messages'):
        return

    messages = [msg for msg in response.get('messages')]

    while response.get('nextPageToken'):
        pt = response['nextPageToken']
        try:
            response = service.users().messages().list(userId='me',
                                                       q=q,
                                                       pageToken=pt,
                                                       ).execute()
        except errors.HttpError as error:
            print("An error occurred: {}".format(error))
            continue
        messages.extend(response.get('messages'))

    existing_messages = Chat.query.all()
    existing_ids = [msg.message_id for msg in existing_messages]

    message_ids = [
        msg['id'] for msg in messages
        if msg['id'] not in existing_ids
    ]

    return message_ids


def commit_messages():
    try:
        db.session.commit()
    except:
        print("failed to commit some chats: ", sys.exc_info()[0])


def add(query):
    message_ids = get_message_ids(query)

    if not message_ids:
        print("no new messages found.")
        return

    print("adding messages...")
    for i, msg_id in enumerate(message_ids):
        response = service.users().messages().get(userId='me',
                                                  id=msg_id,
                                                  format='full').execute()
        data = json.dumps(response)

        thread_id = response.get('thread_id') or response.get('threadId')
        if not thread_id:
            print("No thread_id found for {}".format(msg_id))
            continue

        encoded_text = response['payload']['body']['data'].encode('utf-8')
        text = base64.urlsafe_b64decode(encoded_text)
        send_time = response['internalDate']

        for header in response['payload']['headers']:
            if header['name'] == "From":
                try:
                    sender = header['value']
                    email_address = email_regex.findall(sender)[0].lower()
                except:
                    raise("Couldn't get email from {}".format(sender))

        new_chat = Chat(
            message_id=msg_id,
            data=data,
            thread_id=thread_id,
            text=text,
            send_time=send_time,
            sender=email_address,
        )
        db.session.add(new_chat)

        if i > 0 and i % CHUNK_SIZE == 0:
            # commit by chunk size so you don't have to start over
            commit_messages()
            print("committed {}, {} to go".format(i, len(message_ids)-i))

    # commit any extras
    commit_messages()
    print("finished query. {} new chats.".format(len(message_ids)))


def add_new_chats(queries):
    for q in queries:
        add(q)
