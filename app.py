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

AMEDIA_ORG_ID = 582844


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))

    # Get user details
    resp = github.get("/user")
    ret = '<h2>USER DETAILS:</h2><br>'
    if resp.ok:
        ret += "You are %s on GitHub<br>" % resp.json()["login"]
    else:
        ret += 'FAILED AT GETTING USER DATA<br>'

    # Get user organizations
    ret += '<h2>ORGANIZATIONS:</h2><br>'
    resp = github.get("/user/orgs")
    if not resp.ok:
        ret += 'FAILED AT GETTING USERORG DATA<br>'
    else:
        u_orgs = resp.json()
        ret += "<pre>%s</pre><br>" % json.dumps(u_orgs, indent=4)

        # Check if user is part of Amedia
        for org in u_orgs:
            if org.get('id', None) == AMEDIA_ORG_ID:
                ret += '<h3>--- YOU ARE PART OF AMEDIA ORGANIZATION --- </h3>'
                break
        else:
            ret += '<h3>--- YOU ARE NOT MEMBER OF AMEDIA --- </h3>'

    # Finally return the retval
    return ret


if __name__ == "__main__":
    app.run()
