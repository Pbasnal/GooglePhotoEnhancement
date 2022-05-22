from flask_restful import Resource
from flask import session, jsonify
from cacheservice import DictCache
from UserAuth import UserOauth
from apis.userBackgroundProcess import processUser
from apis.messagebus import Bus, USER_QUEUE

class UserProcess:
    def __init__(self, userId, allAlbumsInitialized) -> None:
        self.userId = userId
        self.allAlbumsInitialized = allAlbumsInitialized

        
class HelloWorld(Resource):
    def get(self):
        if 'user_id' not in session:
            return f"User {userId} not found", 400

        userId = session['user_id']

        user = UserOauth.query.filter(UserOauth.id == userId).one()

        userProcessStatus = self.getUserStatus(userId)
        if userProcessStatus == True:
            return jsonify(user.serialize)
        elif userProcessStatus == None:
            Bus.publish(USER_QUEUE, userId)

        return { "userId": userId, "processStatus": processUser(userId)}, 202

    def getUserStatus(self, userId):
        with DictCache("userProcessCache.json") as userProcessCache:
            return userProcessCache.getForKey(userId)