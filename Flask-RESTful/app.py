from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity

app = Flask(__name__)
# Allow flask propogating exceptions even debug is set to false on app
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose' # Secret key for encryption
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = [] # Contains a dictionary for each item

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,
                        help="This field can't be left blank"
                        )

    @jwt_required()
    def get(self,name):
        # Returns an item matches with the name
        return {'item': next(filter(lambda x: x['name']==name, items),None)}

    # Add the item to the list
    def post(self,name):
        if next(filter(lambda x: x['name']==name,items),None) is not None:
            return {"message: An item with name {} is already exists!".format(name)}, 404

        data = Item.parser.parse_args()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item

    # Delete the item
    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] !=name, items))# Looking for the item except those get deleted
        return {'message': 'Item deleted'}

    @jwt_required()
    # putting data to the list
    def put(self, name):
        data = Item.parser.parse_args()
        # print something not in the args to verify that it works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items':items} # Returns a list of items

api.add_resource(Item, '/item/<string:name>') # https://127.0.0.1:5000/item/item name
api.add_resource(ItemList, '/items') # https://127.0.0.1:5000/items

if __name__ == '__main__':
    app.run(debug=True) # Important to mention debug=True            

