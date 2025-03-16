from mongoengine import Document, StringField, ListField, ReferenceField, ValidationError
from .room import Room

class Sensor(Document):
    name = StringField(required=True)
    rooms = ListField(ReferenceField(Room), required=True, min_length=2, max_length=2)

    def clean(self):
        """Custom validation rules."""
        self.validate_name()
        self.validate_rooms()
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
