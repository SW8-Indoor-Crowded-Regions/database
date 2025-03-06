from mongoengine import Document, StringField, FloatField

class Room(Document):
    name = StringField(required=True)
    type = StringField(required=True, choices=["MEETING", "LOBBY", "OFFICE"])
    crowd_factor = FloatField(required=True, min_value=0)
    area = FloatField(required=True, min_value=0)
    longitude = FloatField(required=True, min_value=0)
    latitude = FloatField(required=True, min_value=0)


