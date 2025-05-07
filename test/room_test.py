import pytest
from mongoengine import connect, disconnect
import mongomock
from db.models import Room
from mongoengine.errors import ValidationError

numeric_fields = ['crowd_factor', 'popularity_factor', 'area', 'longitude', 'latitude']
numerics_with_no_bounds = ['area', 'longitude', 'latitude']
numeric_factors = ['crowd_factor', 'popularity_factor']


@pytest.fixture(autouse=True)
def setup_mock_db():
	"""Setup mock database before each test."""
	disconnect()  # Disconnect from any previous connections

	# Connect to a mock MongoDB instance
	connect(
		db='mongoenginetest',
		host='mongodb://localhost',
		mongo_client_class=mongomock.MongoClient,
		uuidRepresentation='standard',
	)

	yield  # Run the test

	# Cleanup after test
	disconnect()


@pytest.fixture
def valid_room_data():
	return {
		'name': 'Test Room',
		'type': 'MEETING',
		'crowd_factor': 0.5,
		'popularity_factor': 0.5,
		'area': 100.0,
		'longitude': 12.34,
		'latitude': 56.78,
		'floor': 1,
		'borders': [[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
	}


def test_valid_room_creation(valid_room_data):
	room = Room(**valid_room_data)
	room.validate()  # Should not raise any exception
	room.save()  # Should save without errors
	assert Room.objects(name=valid_room_data['name']).first() is not None


def test_invalid_room_type(valid_room_data):
	valid_room_data['type'] = 'INVALID_TYPE'
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_negative_values(valid_room_data):
	# Test each numeric field with negative values

	for field in numeric_fields:
		invalid_data = valid_room_data.copy()
		invalid_data[field] = -1.0
		room = Room(**invalid_data)
		with pytest.raises(ValidationError):
			room.validate()


def test_missing_required_fields():
	# Test creating room with no fields
	with pytest.raises(ValidationError):
		room = Room()
		room.validate()


def test_zero_values(valid_room_data):
	# Test boundary case with zero values (should be valid)

	for field in numerics_with_no_bounds:
		valid_data = valid_room_data.copy()
		valid_data[field] = 0.0
		room = Room(**valid_data)
		room.validate()  # Should not raise any exception
		room.save()  # Should save without errors
		assert Room.objects(_id=room.id).first() is not None
		room.delete()


def test_zero_values_for_factors(valid_room_data):
	valid_room_data['crowd_factor'] = 0.0
	valid_room_data['popularity_factor'] = 0.0
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_all_room_types(valid_room_data):
	# Test all valid room types
	valid_types = ['MEETING', 'LOBBY', 'OFFICE']

	for room_type in valid_types:
		valid_data = valid_room_data.copy()
		valid_data['type'] = room_type
		room = Room(**valid_data)
		room.validate()  # Should not raise any exception
		room.save()  # Should save without errors
		assert Room.objects(type=room_type).first() is not None
		room.delete()


def test_negative_occupants(valid_room_data):
	valid_room_data['occupants'] = -1.0
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_empty_name(valid_room_data):
	valid_room_data['name'] = ''
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_very_large_values(valid_room_data):
	# Test with very large values (should be valid)

	for field in numerics_with_no_bounds:
		valid_data = valid_room_data.copy()
		valid_data[field] = 1e10  # Very large number
		room = Room(**valid_data)
		room.validate()  # Should not raise any exception
		room.save()  # Should save without errors
		assert Room.objects(_id=room.id).first() is not None
		room.delete()


def test_max_value_for_factors(valid_room_data):
	"""test max value for room factors"""
	valid_room_data['popularity_factor'] = 2.1
	valid_room_data['crowd_factor'] = 2.1
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_whitespace_name(valid_room_data):
	"""Test that a name containing only whitespace is rejected."""
	valid_room_data['name'] = '   '
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_invalid_crowd_factor_type(valid_room_data):
	"""Test that a non-numeric crowd_factor raises a ValidationError."""
	valid_room_data['crowd_factor'] = 'high'
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_invalid_popularity_factor_type(valid_room_data):
	"""Test that a non-numeric popularity_factor raises a ValidationError."""
	valid_room_data['popularity_factor'] = 'high'
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_invalid_area_type(valid_room_data):
	"""Test that a non-numeric area raises a ValidationError."""
	valid_room_data['area'] = 'large'
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_invalid_longitude_type(valid_room_data):
	"""Test that a non-numeric longitude raises a ValidationError."""
	valid_room_data['longitude'] = 'east'
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_invalid_latitude_type(valid_room_data):
	"""Test that a non-numeric latitude raises a ValidationError."""
	valid_room_data['latitude'] = 'north'
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_invalid_room_type_non_string(valid_room_data):
	"""Test that a room type provided as a non-string (e.g., int) raises a ValidationError."""
	valid_room_data['type'] = 123
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_name_none(valid_room_data):
	"""Test that a None value for name raises a ValidationError."""
	valid_room_data['name'] = None
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_type_none(valid_room_data):
	"""Test that a None value for type raises a ValidationError."""
	valid_room_data['type'] = None
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_crowd_factor_none(valid_room_data):
	"""Test that a None value for crowd_factor raises a ValidationError."""
	valid_room_data['crowd_factor'] = None
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_popularity_factor_none(valid_room_data):
	"""Test that a None value for popularity_factor raises a ValidationError."""
	valid_room_data['popularity_factor'] = None
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_area_none(valid_room_data):
	"""Test that a None value for area raises a ValidationError."""
	valid_room_data['area'] = None
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_longitude_none(valid_room_data):
	"""Test that a None value for longitude raises a ValidationError."""
	valid_room_data['longitude'] = None
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_latitude_none(valid_room_data):
	"""Test that a None value for latitude raises a ValidationError."""
	valid_room_data['latitude'] = None
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_invalid_floor(valid_room_data):
	"""Test that invalid floor values raise a ValidationError."""
	invalid_floors = [0, 4, -1, 'first', None]
	for floor in invalid_floors:
		valid_room_data['floor'] = floor
		room = Room(**valid_room_data)
		with pytest.raises(ValidationError):
			room.validate()


def test_valid_floor(valid_room_data):
	"""Test that valid floor values do not raise a ValidationError."""
	valid_floors = [1, 2, 3]
	for floor in valid_floors:
		valid_room_data['floor'] = floor
		room = Room(**valid_room_data)
		room.validate()  # Should not raise any exception
		room.save()  # Should save without errors
		assert Room.objects(_id=room.id).first() is not None
		room.delete()


def test_invalid_borders_not_a_list(valid_room_data):
	"""Test that non-list borders raise a ValidationError."""
	invalid_borders = [None, 'invalid', 123, {'lat': 1.1, 'long': 1.0}]
	for borders in invalid_borders:
		valid_room_data['borders'] = borders
		room = Room(**valid_room_data)
		with pytest.raises(ValidationError):
			room.validate()


def test_invalid_borders_too_few_coordinates(valid_room_data):
	"""Test that borders with fewer than 3 coordinate pairs raise a ValidationError."""
	valid_room_data['borders'] = [[1.1, 1.0], [1.2, 1.0]]
	room = Room(**valid_room_data)
	with pytest.raises(ValidationError):
		room.validate()


def test_invalid_borders_invalid_coordinate_format(valid_room_data):
	"""Test that borders with invalid coordinate formats raise a ValidationError."""
	invalid_borders = [
		[[1.1, 1.0], [1.2]],
		[[1.1, 1.0], [1.2, 'invalid']],
		[[1.1, 1.0], [1.2, 1.0], [1.3]],
	]
	for borders in invalid_borders:
		valid_room_data['borders'] = borders
		room = Room(**valid_room_data)
		with pytest.raises(ValidationError):
			room.validate()


def test_invalid_borders_non_float_coordinates(valid_room_data):
	"""Test that borders with non-float coordinates raise a ValidationError."""
	invalid_borders = [
		[[1.1, 1.0], [1.2, 'invalid']],
		[[1.1, 1.0], [1.2, 1]],
	]
	for borders in invalid_borders:
		valid_room_data['borders'] = borders
		room = Room(**valid_room_data)
		with pytest.raises(ValidationError):
			room.validate()


def test_valid_borders(valid_room_data):
	"""Test that valid borders pass validation."""
	valid_room_data['borders'] = [[1.1, 1.0], [1.2, 1.0], [1.3, 1.1]]
	room = Room(**valid_room_data)
	room.validate()
	room.save()
	assert Room.objects(_id=room.id).first() is not None
	room.delete()


def test_compute_area_from_four_borders(valid_room_data):
	"""Test that compute_area correctly calculates the polygon area."""
	valid_room_data['borders'] = [
		[12.340000, 56.780000],
		[12.340180, 56.780000],
		[12.340180, 56.780090],
		[12.340000, 56.780090],
	]

	room = Room(**valid_room_data)
	area = room.compute_area()
	assert area == 110.28


def test_compute_area_with_two_borders(valid_room_data):
	"""Test that compute_area returns 0.0 when only two border points are provided."""
	valid_room_data['borders'] = [
		[0.0, 0.0],
		[4.0, 0.0],
	]
	room = Room(**valid_room_data)
	area = room.compute_area()
	assert area == 0.0


def test_compute_area_with_five_borders(valid_room_data):
	"""Test that compute_area correctly calculates the area of a pentagon."""
	valid_room_data['borders'] = [
		[12.340000, 56.780000],
		[12.340090, 56.780000],
		[12.340130, 56.780050],
		[12.340045, 56.780120],
		[12.339990, 56.780050],
	]
	room = Room(**valid_room_data)
	area = room.compute_area()
	assert area == 72.5

