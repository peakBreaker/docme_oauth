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
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    ret = '<h2>USER DETAILS:</h2><br>'
    ret += "You are @{login} on GitHub<br>".format(login=resp.json()["login"])

    # GET orgs
    resp = github.get("/user/orgs")
    assert resp.ok
    ret += '<h2>ORGANIZATIONS:</h2><br>'
    ret += "<pre>%s</pre>" % (json.dumps(resp.json(), indent=4))
    return ret


if __name__ == "__main__":
    app.run()
