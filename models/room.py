from mongoengine import Document, StringField, FloatField

class Room(Document):
    # This field is required and must be a non-empty string.
    name = StringField(required=True)
    
    # This field is required, and must match one of the given choices.
    type = StringField(required=True, choices=["MEETING", "LOBBY", "OFFICE"])
    
    # This field is required, must be a float, and can't be negative.
    crowd_factor = FloatField(required=True, min_value=0)
    
    # Also required, must be a float, and can't be negative.
    area = FloatField(required=True, min_value=0)

    longitude = FloatField(required=True, min_value=0)
    latitude = FloatField(required=True, min_value=0)


