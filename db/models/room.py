from mongoengine import Document, StringField, FloatField, ValidationError

# Define allowed room types as a constant variable
ROOM_TYPES = ("MEETING", "LOBBY", "OFFICE", "EXHIBITION", "RESTROOM", "SHOP", "RESTAURANT")

class Room(Document):
	name = StringField(required=True)
	type = StringField(required=True, choices=ROOM_TYPES)
	crowd_factor = FloatField(required=True, min_value=0.1, max_value=2.0)
	popularity_factor = FloatField(required=True, min_value=0.1, max_value=2.0)
	occupants = FloatField(min_value=0, default=0)
	area = FloatField(required=True, min_value=0)
	longitude = FloatField(required=True, min_value=0)
	latitude = FloatField(required=True, min_value=0)

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
			(self.latitude, self.validate_non_negative_number, "Latitude must be a non-negative number")
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
