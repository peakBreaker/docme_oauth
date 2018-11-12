import os
import json

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint(scope='read:org')
app.register_blueprint(github_bp, url_prefix="/login")


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    ret = '<h2>USER DETAILS:</h2><br>'
    if resp.ok:
        ret += "You are @{login} on GitHub<br>".format(login=resp.json()["login"])
    else:
        ret += 'FAILED AT GETTING USER DATA<br>'

    # GET orgs
    resp = github.get("/user/orgs")
    ret += '<h2>ORGANIZATIONS:</h2><br>'
    if resp.ok:
        ret += "<pre>%s</pre>" % (json.dumps(resp.json(), indent=4))
    else:
        ret += 'FAILED AT GETTING USERORG DATA<br>'
    return ret


if __name__ == "__main__":
    app.run()
