from db import db

# db.Model tells the things that we are saving to and retrieve from database
class UserModel(db.Model):
    
    __tablename__ = 'users'

    # Columns the table contain
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        # Create a query and filter by username and taking first
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        # Create a query and filter it by id
        return cls.query.filter_by(id=_id).first()        