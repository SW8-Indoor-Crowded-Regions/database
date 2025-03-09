from mongoengine import Document, StringField, FloatField, ValidationError

class Room(Document):
    name = StringField(required=True)
    type = StringField(required=True, choices=["MEETING", "LOBBY", "OFFICE"])
    crowd_factor = FloatField(required=True, min_value=0)
    area = FloatField(required=True, min_value=0)
    longitude = FloatField(required=True, min_value=0)
    latitude = FloatField(required=True, min_value=0)

    def clean(self):
        """Custom validation rules."""
        super().clean()
        
        # Validate that name is not empty or just whitespace
        if not self.name or not self.name.strip():
            raise ValidationError("Name cannot be empty")
        
        # Validate type is one of the allowed choices
        if self.type not in ["MEETING", "LOBBY", "OFFICE"]:
            raise ValidationError("Type must be one of: MEETING, LOBBY, OFFICE")
        
        # Validate crowd_factor is a number and non-negative
        if self.crowd_factor is None or not isinstance(self.crowd_factor, (int, float)):
            raise ValidationError("Crowd factor must be a number")
        if self.crowd_factor < 0:
            raise ValidationError("Crowd factor cannot be negative")
        
        # Validate area is a number and non-negative
        if self.area is None or not isinstance(self.area, (int, float)):
            raise ValidationError("Area must be a number")
        if self.area < 0:
            raise ValidationError("Area cannot be negative")
        
        # Validate longitude is a number and non-negative
        if self.longitude is None or not isinstance(self.longitude, (int, float)):
            raise ValidationError("Longitude must be a number")
        if self.longitude < 0:
            raise ValidationError("Longitude cannot be negative")
        
        # Validate latitude is a number and non-negative
        if self.latitude is None or not isinstance(self.latitude, (int, float)):
            raise ValidationError("Latitude must be a number")
        if self.latitude < 0:
            raise ValidationError("Latitude cannot be negative")
