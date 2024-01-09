import os

import flask
import flask.json
import flask_httpauth
from werkzeug.security import generate_password_hash, check_password_hash

import scraper.scrape as scrape

app = flask.Flask(__name__)
auth = flask_httpauth.HTTPBasicAuth()

username = os.environ["HUNT_USERNAME"]
password = os.environ["HUNT_PASSWORD"]

users = {
    username: generate_password_hash(password)
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/puzzles')
@auth.login_required
def scrape_it():
    return flask.json.jsonify(
        scrape.scrape_hunt_state(
            os.environ['HUNT_LOGIN_URL'],
            os.environ['PUZZLES_URL'],
            username,
            password))


application = app
