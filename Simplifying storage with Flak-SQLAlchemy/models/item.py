from db import db

# db.Model tells the things that we are saving to and retrieve from database(Mapping)
class ItemModel(db.Model):

    # The model to be stored
    __tablename__ = 'items'

    # Columns the table contain
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80)) #80 is a limit of characters 
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    
    def __init__(self,name,price, store_id):
        self.name = name
        self.price  = price
        self.store_id = store_id

    # Create a json file 
    def json(self):
        return {'name': self.name, 'price': self.price}    

    @classmethod  
    def find_by_name(cls,name):
        # Building a query on database and filtering by name
        # SELECT * FROM item WHERE name=name and limit=1
        return cls.query.filter_by(name=name).first()
                  
    # Saving to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Deleting from database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()