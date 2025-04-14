from mongoengine import Document, StringField, ListField, ReferenceField, ValidationError, FloatField, ObjectIdField
from .room import Room
from bson import ObjectId

class Sensor(Document):
    _id = ObjectIdField(required=False, primary_key=True, default=ObjectId)
    name = StringField(required=True)
    rooms = ListField(ReferenceField(Room, dbref=False), required=True, min_length=2, max_length=2)
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)

    def clean(self):
        """Custom validation rules."""
        self.validate_name()
        self.validate_rooms()
        self.validate_coordinates(self.latitude, "Latitude")
        self.validate_coordinates(self.longitude, "Longitude")
        super().clean()

    def validate_name(self):
        """Validate that name is not empty."""
        if not self.name or not self.name.strip(): # type: ignore
            raise ValidationError("Name cannot be empty")

    def validate_rooms(self):
        """Validate rooms: ensure each room is a valid Room instance."""
        if self.rooms:
            for room in self.rooms: # type: ignore
                if not isinstance(room, Room):
                    raise ValidationError("Each room must be a valid Room instance")

    def validate_coordinates(self, value, field_name: str):
        """Validate latitude: ensure lat is valid"""
        if value is None or not isinstance(value, float):
            raise ValidationError(f"{field_name} must be a non-empty float")