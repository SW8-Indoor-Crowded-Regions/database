from mongoengine import Document, StringField, FloatField, IntField, ValidationError, ObjectIdField, ListField
from bson import ObjectId

# Define allowed room types as a constant variable
ROOM_TYPES = ("MEETING", "LOBBY", "OFFICE", "EXHIBITION", "RESTROOM", "SHOP", "RESTAURANT")

class Room(Document):
	_id = ObjectIdField(required=False, primary_key=True, default=ObjectId)
	name = StringField(required=True)
	type = StringField(required=True, choices=ROOM_TYPES)
	crowd_factor = FloatField(required=True, min_value=0.1, max_value=2.0)
	popularity_factor = FloatField(required=True, min_value=0.1, max_value=2.0)
	occupants = FloatField(min_value=0, default=0)
	area = FloatField(required=True, min_value=0)
	longitude = FloatField(required=True, min_value=0)
	latitude = FloatField(required=True, min_value=0)
	floor = IntField(required=True, min_value=1, max_value=3)
	borders = ListField(
		ListField(FloatField(required=True, default=[1.1, 1.0]), required=True, min_length=2, max_length=2),
		required=True, min_length=3
	)

	def clean(self):
		"""Custom validation rules."""
		super().clean()
		self.run_validations()

	def run_validations(self):
		"""Run all validation rules."""
		validations = [
			(self.name, self.validate_non_empty, "Name cannot be empty"),
			(self.type, self.validate_choice, "Type must be one of: " + ", ".join(ROOM_TYPES)),
			(self.crowd_factor, self.validate_non_negative_number, "Crowd factor must be a non-negative number between 0.1 and 2.0"),
			(self.popularity_factor, self.validate_non_negative_number, "Popularity factor must be a non-negative number between 0.1 and 2.0"),
			(self.area, self.validate_non_negative_number, "Area must be a non-negative number"),
			(self.occupants, self.validate_non_negative_number, "Occupants must be a non-negative number"),
			(self.longitude, self.validate_non_negative_number, "Longitude must be a non-negative number"),
			(self.latitude, self.validate_non_negative_number, "Latitude must be a non-negative number"),
			(self.floor, self.validate_floor, "Floor must be an integer from 1 to 3"),
			(self.borders, self.validate_borders, "Borders must be a list of lists containing two floats"),
		]
		for value, validator, error_message in validations:
			validator(value, error_message)

	def validate_non_empty(self, value, error_message):
		"""Validate that value is not empty or just whitespace."""
		if not value or not value.strip(): # type: ignore
			raise ValidationError(error_message)

	def validate_choice(self, value, error_message):
		"""Validate that value is one of the allowed choices."""
		if value not in ROOM_TYPES:
			raise ValidationError(error_message)

	def validate_non_negative_number(self, value, error_message):
		"""Validate value is a number and non-negative."""
		if value is None or not isinstance(value, (int, float)):
			raise ValidationError(error_message)
		if value < 0:
			raise ValidationError(error_message)

	def validate_floor(self, value, error_message):
		"""Validate floor: ensure floor is valid."""
		if value is None or not isinstance(value, int) or value < 1 or value > 3:
			raise ValidationError(error_message)
	
	def validate_borders(self, value, error_message):
		"""Validate borders: ensure borders are valid."""
		if value is None or not isinstance(value, list) or len(value) < 3:
			raise ValidationError(error_message)
		for border in value:
			if not isinstance(border, list) or len(border) != 2:
				raise ValidationError(error_message)
			for coord in border:
				if coord is None or not isinstance(coord, float):
					raise ValidationError(error_message)