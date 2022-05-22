import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
api = Api(app)


from apis.PhotoAlbums import PhotoAlbums
from apis.HelloWorld import HelloWorld
from apis.AuthorizeWithGoogle import AuthorizeWithGoogle

api.add_resource(AuthorizeWithGoogle, '/auth')
api.add_resource(PhotoAlbums, '/albums')
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    # app.run('localhost', 8080, debug=True, ssl_context="adhoc")
    app.run()
