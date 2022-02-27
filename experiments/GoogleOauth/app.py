import os 

from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
 
app = Flask(__name__)
 
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<\
!\xd5\xa2\xa0\x9fR"\xa1\xa8'
 
'''
    Set SERVER_NAME to localhost as twitter callback
    url does not accept 127.0.0.1
    Tip : set callback origin(site) for facebook and twitter
    as http://domain.com (or use your domain name) as this provider
    don't accept 127.0.0.1 / localhost
'''
 
app.config['SERVER_NAME'] = 'localhost:8080'
oauth = OAuth(app)
 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/google/')
def google():
   
    # Google Oauth Config
    # Get client_id and client_secret from environment variables
    # For developement purpose you can directly put it
    # here inside double quotes
    GOOGLE_CLIENT_ID = "192945714387-unahrc9sdl4mjdag2naghk3fpq1hs15v.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "uZElQTC0v9-jqhZY6fGJs8Cp"
     
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
     
    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
 
@app.route('/oauth2callback')
def google_auth():
    token = oauth.google.authorize_access_token()

    user = oauth.google.parse_id_token(token)
    print(" Google User ", user)
    print(" \n\n\ntoken ", token)
    return redirect('/')
 
if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc")