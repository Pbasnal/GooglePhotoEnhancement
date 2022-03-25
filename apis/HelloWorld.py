from flask_restful import Resource, reqparse
from flask import session, jsonify
from cacheservice import DictCache
from UserAuth import UserOauth
from apis.messagebus import USER_QUEUE
from apis.messagebus import MessageBus
Bus = MessageBus()
        
class HelloWorld(Resource):
    def get(self):
        if 'user_id' not in session:
            return f"User {userId} not found", 400

        userId = session['user_id']
        print(f"Loading for user: {userId}")
        user = UserOauth.query.filter(UserOauth.id == userId).one()
        userProcessStatus = self.getUserStatus(userId)
        if userProcessStatus == True:
            return jsonify(user.serialize)
        elif userProcessStatus == None:
            # Bus.publish(USER_QUEUE, userId)
            pass
        # only for testing the below code is used
        Bus.publish(USER_QUEUE, userId)

        return { "userId": userId, "processStatus": "In Progress"}, 202

    def getUserStatus(self, userId):
        with DictCache("userProcessCache.json") as userProcessCache:
            return userProcessCache.getForKey(userId)

class SimilarImages(Resource):
    def get(self):
        if 'user_id' not in session:
            return f"User {userId} not found", 400

        userId = session['user_id']
        user = UserOauth.query.filter(UserOauth.id == userId).one()
        
        if user == None:
            return {}, 300

        with DictCache("similarPhoto.json", "json") as similarPhotoCache:
            return similarPhotoCache.cache, 200