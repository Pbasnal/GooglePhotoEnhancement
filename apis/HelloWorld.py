from flask_restful import Resource, Api
from flask import Flask, redirect, url_for, session, request, jsonify

class HelloWorld(Resource):
    def get(self):
        if 'user_id' not in session:
            return "User not found", 400

        userId = session['user_id']
        from UserAuth import UserOauth

        user = UserOauth.query.filter(UserOauth.id == userId).one()

        return jsonify(user.serialize)