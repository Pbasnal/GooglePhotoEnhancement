from flask import Flask
import os
import threading

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['LC_ALL'] = 'en_US.utf-8'
os.environ['LANG'] = 'en_US.utf-8'
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'development'   

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_restful import Api

api = Api(app)
def addApis():
    from apis.HelloWorld import HelloWorld, SimilarImages
    api.add_resource(HelloWorld, '/')
    api.add_resource(SimilarImages, '/similarimages')
    
    from apis.AuthorizeWithGoogle import AuthorizeWithGoogle
    api.add_resource(AuthorizeWithGoogle, '/auth')

    from apis.PhotoAlbums import PhotoAlbums
    api.add_resource(PhotoAlbums(api), '/albums')

addApis()

def startWorkers():
    print("Starting workers")
    from apis.messagebus import MessageBus
    Bus = MessageBus()
    import apis.userBackgroundProcess as userListener
    import apis.photoBackgroundProcess as photoListener

    Bus.addListener(photoListener)
    Bus.addListener(userListener)

    Bus.startListeners("localhost")

def startServer(debug=False):

    print(f"API routes \n{app.url_map}")
    app.run(
        # host='localhost',
        port=8080,
        debug=debug,
        ssl_context="adhoc")
    # app.run(debug=debug, ssl_context="adhoc")
    # app.run()

workerThread = threading.Thread(target=startWorkers)
workerThread.start()

if __name__ == '__main__':

    startServer()
