from mongoengine import Document, StringField, ListField, IntField, ReferenceField, ValidationError
from .room import Room

class Sensor(Document):
    name = StringField(required=True)
    movements = ListField(
        ListField(IntField(), min_length=2, max_length=2), required=False
    )
    rooms = ListField(ReferenceField(Room), required=False)

    def clean(self):
        """Custom validation rules."""
        # Validate movement coordinates
        if self.movements:
            for movement in self.movements:
                if not isinstance(movement, (list, tuple)):
                    raise ValidationError("Each movement must be a list or tuple of coordinates")
                if len(movement) != 2:
                    raise ValidationError("Each movement must have exactly 2 coordinates")
                if not all(isinstance(coord, int) for coord in movement):
                    raise ValidationError("Movement coordinates must be integers")
        
        # Validate that name is not empty
        if not self.name or not self.name.strip():
            raise ValidationError("Name cannot be empty")
        
        # Validate rooms: ensure each room is a valid Room instance
        if self.rooms:
            for room in self.rooms:
                if not isinstance(room, Room):
                    raise ValidationError("Each room must be a valid Room instance")
        
        super().clean()
