from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token, create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required)
from blocklist import BLOCKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field can not be empty') 

_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field can not be empty') 
    
# Create user
class UserRegister(Resource):
    
    def post(self):
        data = _user_parser.parse_args()
        # find user by its username otherwise add it and save to database
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'],data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

# Retrieve user and delete user
class User(Resource):
    @classmethod
    def get(cls, user_id):
        # find user by user_id and return the json if found
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'}, 404
        return user.json() 

    @classmethod
    def delete(cls, user_id):
        # find user by id if found then delete it
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'}, 404
        user.delete_from_db() 
        return {'message':'User deleted'}, 200  

class UserLogin(Resource):
    @classmethod
    def post(self):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in datbase
        user = UserModel.find_by_username(data['username'])
        # check password, create access token, crete refresh token
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity = user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                'access_token': access_token,
                'refresh_token': refresh_token
            },200
        return {'message':'invalid credentials'},401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_jwt()['jti'] #'jti' is JWT ID and unique identifier for jwt
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        # Create new token based on refresh token if user not logged in for long time
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200    
        