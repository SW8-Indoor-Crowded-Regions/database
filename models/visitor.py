
from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
    DateTimeField
)

from room import Room

class Visitor(Document):
    name = StringField(required=True)
    
    # "visitedRooms" as an array of ObjectId
    visited_rooms = ListField(ReferenceField(Room), required=True)
    
    visit_date = DateTimeField()
