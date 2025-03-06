# sensor.py
from mongoengine import (
    Document, 
    StringField, 
    ListField, 
    IntField, 
    ReferenceField, 
    ValidationError
)
from room import Room

class Sensor(Document):
    name = StringField(required=True)
    movements = ListField(ListField(IntField(), min_length=2, max_length=2), required=True)
    rooms = ListField(ReferenceField(Room), required=True)