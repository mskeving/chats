import re

from flask import render_template

from app import app
from models import Text

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/get_links/<user>', methods=['GET'])
def get_links(user):
    if user == "missy":
        email = "mskeving@gmail.com"
    elif user == "phil":
        email = "philrha@gmail.com"
    else:
        return "User {} not known".format(user)

    text_obj = Text.query.filter_by(sender=email).first()

    if not text_obj:
        return None

    # links = set(re.findall("(http:\/\/.*?)[\"' <]", text_obj.text))  # http
    # links.update(set(re.findall("(https:\/\/.*?)[\"' <]", text_obj.text)))  # https
    links = set(re.findall("(https:\/\/www\.youtube\.com.*?)[\"' <]", text_obj.text))  # http

    html = ""
    for link in links:
        html += u'<div style="margin-bottom:5px;"><a target=_blank href={}>{}</a></div>'.format(link, link)

    return html
