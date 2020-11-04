from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # Many (items) to one (store) relationship; returns list of ItemModels 
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
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