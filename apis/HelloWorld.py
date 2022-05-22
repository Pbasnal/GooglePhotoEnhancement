from flask_restful import Resource
from flask import session, jsonify, redirect, url_for
from cacheservice import DictCache
from UserAuth import UserOauth
from apis.messagebus import USER_QUEUE
from apis.messagebus import MessageBus
from apis.AuthorizeWithGoogle import AuthorizeWithGoogle
Bus = MessageBus()
        
class HelloWorld(Resource):
    def get(self):
        if 'user_id' not in session:
            return f"User {userId} not found", 400

        userId = session['user_id']
        print(f"Loading for user: {userId}")
        user = UserOauth.getUser(userId)
        
        if user is None:
            return redirect("/auth")

        userProcessStatus = self.getUserStatus(userId)
        if userProcessStatus == True:
            return jsonify(user.serialize)
        elif userProcessStatus == None:
            Bus.publish(USER_QUEUE, userId)
            pass

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
