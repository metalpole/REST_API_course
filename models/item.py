from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Many to one relationship
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # Define new column for store (and attribute for ItemModel) using store_id as foreign key 
    # to lookup store name in store table
    store = db.relationship('StoreModel') # Each item can only be found in one store

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'name': self.name,
            'price': self.price
        }
        
    @classmethod
    def find_by_name(cls, name):
        # filter(ItemModel.name == name)
        # Can have multiple parameters in one filter
        # Converts result into ItemModel object with name, price attributes as defined in __init__
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # Insert, or update if it already exists
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()