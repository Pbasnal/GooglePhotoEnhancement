import os, pika, threading
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

from apis.PhotoAlbums import PhotoAlbums
from apis.HelloWorld import HelloWorld
from apis.AuthorizeWithGoogle import AuthorizeWithGoogle

api.add_resource(AuthorizeWithGoogle, '/auth')
api.add_resource(PhotoAlbums, '/albums')
api.add_resource(HelloWorld, '/')

def startWorkers():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    from apis.messagebus import Bus
    Bus.registerQueues(channel)

    import apis.userBackgroundProcess as userListener
    import apis.photoBackgroundProcess as photoListener
    userListener.registerMessageListener(channel)
    photoListener.registerMessageListener(channel)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

workerThread = threading.Thread(target=startWorkers)
workerThread.start()

if __name__ == '__main__':
    # app.run('localhost', 8080, debug=True, ssl_context="adhoc")
    app.run(debug=True, ssl_context="adhoc")
    #app.run()
