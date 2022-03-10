from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)

"""
JWT related configuration includes:
1) add claims to each jwt
2) customize the token expired error message 
"""
app.config['JWT_SECRET_KEY'] = 'jose'  # we can also use app.secret like before, Flask-JWT-Extended can recognize both
app.config['JWT_BLOCKLIST_ENABLED'] = True  # enable blocklist feature
app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blocklisting for access and refresh tokens
jwt = JWTManager(app)

"""
claims are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via get_jwt_claims()
"""
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


# This method will check if a token is blocklisted, and will be called automatically when blocklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(decrypted_token):
    return decrypted_token['jti'] in BLOCKLIST


# The following callbacks are used for customizing jwt response/error messages 

# when token has expired if no activity for long time
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401

# We want to access the user info but we don't have required token(invalid token)
@jwt.invalid_token_loader
def invalid_token_callback(error):  
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401

# returning a custom response when a valid and non-fresh token is used 
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401

#  returning a custom response when a revoked token is encountered
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

# Create the table
@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)