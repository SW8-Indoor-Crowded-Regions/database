import pytest
from mongoengine import connect, disconnect
import mongomock
from db.models.sensor import Sensor
from db.models.room import Room
from mongoengine.errors import ValidationError


@pytest.fixture(autouse=True)
def setup_mock_db():
	"""Setup mock database before each test."""
	disconnect()  # Disconnect from any previous connections --> (which could be the real database)

	# Connect to a mock MongoDB instance, notice uuidRep is standard, instead of pythonlegacy, done to remove warnings from tests.
	connect(
		db='mongoenginetest',
		host='mongodb://localhost',
		mongo_client_class=mongomock.MongoClient,
		uuidRepresentation='standard',
	)

	yield  # Run the test, it's like pausing the fixture while tests are ran.

	# Cleanup
	disconnect()


@pytest.fixture
def valid_room():
	"""Setup a mock room to be used in tests."""
	room = Room(
		name='Test Room',
		type='MEETING',
		crowd_factor=0.5,
		popularity_factor=0.5,
		area=100.0,
		longitude=12.34,
		latitude=56.78,
		floor=1,
		borders=[[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
	)
	room.save()
	yield room  # Pauses the fixture to be used elsewhere in other tests.
	room.delete()


@pytest.fixture
def valid_sensor_data(valid_room):
	return {'name': 'Test Sensor', 'rooms': [valid_room], 'latitude': 12.34589358, 'longitude': 55.3712033, 'floor': 1}


def test_valid_sensor_creation(valid_sensor_data):
	sensor = Sensor(**valid_sensor_data)
	sensor.validate()  # Should not raise any exception
	sensor.save()  # Should save without errors
	assert Sensor.objects(name=valid_sensor_data['name']).first() is not None
	sensor.delete()


def test_empty_rooms(valid_sensor_data):
	valid_sensor_data['rooms'] = []
	sensor = Sensor(**valid_sensor_data)
	with pytest.raises(ValidationError):
		sensor.validate()

	# sensor.validate()  # Empty rooms list should be valid
	# sensor.save()  # Should save without errors
	# assert Sensor.objects(id=sensor.id).first() is not None
	# sensor.delete()


def test_missing_required_fields():
	# Test creating sensor with no fields, again here making sure exception is called properly
	with pytest.raises(ValidationError):
		sensor = Sensor()
		sensor.validate()


def test_empty_name(valid_sensor_data):
	valid_sensor_data['name'] = ''
	sensor = Sensor(**valid_sensor_data)
	with pytest.raises(ValidationError):
		sensor.validate()

def test_invalid_rooms(valid_sensor_data):
	# Create a Sensor using valid data first.
	sensor = Sensor(**valid_sensor_data)
	# Introduce an invalid room (not an instance of Room)
	sensor.rooms = ['not_a_room_instance'] # type: ignore
	with pytest.raises(ValidationError):
		sensor.validate()

def test_invalid_coordinates_no_latitude(valid_sensor_data):
	sensor = Sensor(**valid_sensor_data)
	with pytest.raises(ValidationError):
		sensor.latitude = None
		sensor.validate()

def test_invalid_coordinates_invalid_longitude(valid_sensor_data):
	sensor = Sensor(**valid_sensor_data)
	sensor.longitude = 'invalid_longitude'
	with pytest.raises(ValidationError):
		sensor.validate()

def test_invalid_floor(valid_sensor_data):
	sensor = Sensor(**valid_sensor_data)
	sensor.floor = 'invalid_floor'
	with pytest.raises(ValidationError):
		sensor.validate()