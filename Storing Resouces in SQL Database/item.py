from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,
                        help="This field can't be left blank"
                        )

    @jwt_required()
    def get(self,name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message':'Item not found'}, 404    

    @classmethod  
    def find_by_name(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name':row[0], 'price':row[1]}}
                  
    # Add the item to the list
    def post(self,name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' is already exists!".format(name)}, 404

        data = Item.parser.parse_args()
        item = {'name':name, 'price':data['price']}

        try:
            self.insert(item)
        except:
            return{'message':'An error occurred while inserting the item'}
        return item    


    @classmethod
    # Inserting an item
    def insert(self,item):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Insert name and value
        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    # Delete the item
    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Insert name and value
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    # putting data to the list
    def put(self, name):
        data = Item.parser.parse_args()
        # print something not in the args to verify that it works
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            self.insert(updated_item)
        else:
            item.update(updated_item)

        return updated_item

    @classmethod
    # update the item
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Update where the name=?
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'],item['name']))

        connection.commit()
        connection.close()



class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Select everything from items
        query = "SELECT * FROM items"
        result  = cursor.execute(query)
        items =[]
        # Iterate over each row
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
       
        connection.close()
        return {'items':items}
