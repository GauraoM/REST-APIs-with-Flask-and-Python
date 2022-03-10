from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from models.item import ItemModel


class Item(Resource):
    # parse the arguments
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
                        )

    @jwt_required
    def get(self, name):
        # find the item by its name and return a json
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        # find a model by its name
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # parse the data and create an item
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            # Save it to db and return a json
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201
    
    @jwt_required
    def delete(self, name):
        # Extract any claims attache to JWT
        claims = get_jwt_claims()
        # if its not the first user
        if not claims['is_admin']:
            return {'message':'Admin Privilege required'}, 401

        # Find by name,if found delete    
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    # Put the data
    def put(self, name):
        # parse the data
        data = Item.parser.parse_args()
        # find the item by its name
        item = ItemModel.find_by_name(name)
        # Add the price and update it
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        # Get the user id of use stored in jwt
        user_id = get_jwt_identity()
        # get all the information stored
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200