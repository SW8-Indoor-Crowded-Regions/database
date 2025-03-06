
from mongoengine import (
    Document,
    StringField,
    ListField,
    ObjectIdField,
    DateTimeField
)

class Visitor(Document):
    name = StringField(required=True)
    
    # "visitedRooms" as an array of ObjectId
    visited_rooms = ListField(ObjectIdField(), required=True)
    
    visit_date = DateTimeField()
