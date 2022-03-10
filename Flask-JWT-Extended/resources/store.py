from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    
    def get(cls, name):
        # find the store by its name if found return the store json
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404
    
    @classmethod
    def post(cls, name):
        # find the store by its name
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
        # Create the store and save it ot database
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201
    
    @classmethod
    def delete(cls, name):
        # find the store and delete it from database
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [x.json() for x in StoreModel.find_all()]}