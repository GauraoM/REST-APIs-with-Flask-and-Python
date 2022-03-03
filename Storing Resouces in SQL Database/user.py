import sqlite3
from flask_restful import Resource, reqparse

class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    # find by username
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Create query to select the data based on username from table
        query = "SELECT * FROM users WHERE username=?"   
        result = cursor.execute(query,(username,))
        # Get the row from result set
        row = result.fetchone()
        if row:
            # passing a set of positional arguments
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    # find by id
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Create query to select id from table
        query = "SELECT * FROM users WHERE id=?"   
        result = cursor.execute(query,(_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

class UserRegister(Resource):
   
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,
                        help = "This field can't be blank"
                        )  
    parser.add_argument('password',type=str,required=True,
                        help = "This field can't be blank"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message":"User with username already exists!"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES(NULL,?,?)" 
        cursor.execute(query,(data['username'], data['password']))

        # To save the changes made into the data
        connection.commit()
        # Close the connection so that it can't receive more data
        connection.close()

        return {"message":"User created successfully!"}, 201                      
            
