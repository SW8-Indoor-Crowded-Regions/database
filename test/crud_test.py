import pytest
from mongoengine import connect, disconnect
import mongomock
from db.models import Room, Sensor

# --- Fixtures ---

@pytest.fixture(autouse=True)
def setup_mock_db():
	"""Setup and teardown the mock database for each test."""
	disconnect()  # Disconnect from any previous connections
	connect(
		db='mongoenginetest',
		host='mongodb://localhost',
		mongo_client_class=mongomock.MongoClient,
		uuidRepresentation='standard',
	)
	yield
	disconnect()


@pytest.fixture
def sample_room():
	"""Create and yield a sample room for testing, then clean up."""
	room = Room(
		name='Mock Room',
		type='OFFICE',
		crowd_factor=0.7,
		popularity_factor=0.7,
		area=120.0,
		longitude=10.0,
		latitude=20.0,
		floor=1,
		borders=[[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
	)
	room.save()
	yield room
	room.delete()


@pytest.fixture
def sample_sensor(sample_room):
	"""Create and yield a sample sensor referencing a room, then clean up."""
	sensor = Sensor(name='Mock Sensor', rooms=[sample_room])
	sensor.save()
	yield sensor
	sensor.delete()


@pytest.fixture
def sample_rooms():
	"""
	Create and yield multiple Room documents for querying tests.
	Clean up the rooms after the test.
	"""
	rooms = [
		Room(
			name='Room 1',
			type='OFFICE',
			crowd_factor=0.5,
			popularity_factor=0.5,
			area=100.0,
			longitude=10.0,
			latitude=20.0,
			floor=1,
			borders=[[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
		),
		Room(
			name='Room 2',
			type='MEETING',
			crowd_factor=0.7,
			popularity_factor=0.7,
			area=150.0,
			longitude=11.0,
			latitude=21.0,
			floor=1,
			borders=[[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
		),
		Room(
			name='Room 3',
			type='LOBBY',
			crowd_factor=0.3,
			popularity_factor=0.3,
			area=200.0,
			longitude=12.0,
			latitude=22.0,	
			floor=1,
			borders=[[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
		),
	]
	for room in rooms:
		room.save()
	yield rooms
	for room in rooms:
		room.delete()


# --- Room Tests ---
def create_room(name: str) -> Room:
	"""Create a room with the given name.
	Args:
		name (str): The name of the room.
	Returns:
		room (Room): The created room.
	"""
	room = Room(
		name=name,
		type='OFFICE',
		crowd_factor=0.5,
		popularity_factor=0.5,
		area=100.0,
		longitude=10.0,
		latitude=20.0,
		floor=1,
		borders=[[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
	)
	return room


def test_room_creation():
	"""Test that a room can be created and exists in the database."""
	room = create_room('Test Room')
	room.save()
	found_room = Room.objects(name='Test Room').first()
	assert found_room is not None
	assert found_room.type == 'OFFICE'
	assert found_room.area == 100.0
	room.delete()


def test_room_query():
	"""Test that a created room can be queried and has correct attributes."""
	room = create_room('Test Room')
	room.save()
	found_room = Room.objects(name='Test Room').first()
	assert found_room is not None
	assert found_room.type == 'OFFICE'
	assert found_room.area == 100.0
	room.delete()


def test_room_update():
	"""Test that a room's attributes can be updated."""
	room = Room(
		name='Test Room',
		type='MEETING',
		crowd_factor=0.5,
		popularity_factor=0.5,
		area=100.0,
		longitude=15.0,
		latitude=25.0,
		floor=1,
		borders=[[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
	)
	room.save()
	room.update(crowd_factor=0.8)
	updated_room = Room.objects(_id=room.id).first()
	assert updated_room is not None
	assert updated_room.crowd_factor == 0.8
	room.delete()


def test_room_deletion():
	"""Test that a room can be deleted from the database."""
	room = Room(
		name='Test Room',
		type='MEETING',
		crowd_factor=0.5,
		popularity_factor=0.5,
		area=100.0,
		longitude=15.0,
		latitude=25.0,
		floor=1,
		borders=[[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
	)
	room.save()
	room.delete()
	assert Room.objects(name='Test Room').first() is None


# --- Sensor Tests ---


def test_sensor_creation_with_room(sample_room):
	"""Test that a sensor referencing a room is created correctly."""
	sensor = Sensor(name='Test Sensor', rooms=[sample_room], latitude=72.1280321, longitude=32.180212)
	sensor.save()
	found_sensor = Sensor.objects(name='Test Sensor').first()
	assert found_sensor is not None
	assert len(found_sensor.rooms) == 1
	assert isinstance(found_sensor.rooms[0], Room)
	assert found_sensor.rooms[0].name == 'Mock Room'
	sensor.delete()


# --- Query Tests on Multiple Rooms ---


def test_query_by_type(sample_rooms):
	"""Test querying rooms by their type."""
	office_rooms = Room.objects(type='OFFICE')
	assert len(office_rooms) == 1
	assert office_rooms[0].name == 'Room 1'


def test_query_by_area_range(sample_rooms):
	"""Test querying rooms by an area range."""
	large_rooms = Room.objects(area__gte=150.0)
	assert len(large_rooms) == 2


def test_query_by_multiple_conditions(sample_rooms):
	"""Test querying rooms with multiple conditions."""
	specific_rooms = Room.objects(type='MEETING', crowd_factor__gte=0.6)
	assert len(specific_rooms) == 1
	assert specific_rooms[0].name == 'Room 2'


# --- Bulk Operation Tests ---


def generate_rooms(num: int) -> list[Room]:
	return [
		Room(
			name=f'Room {i}',
			type='OFFICE',
			crowd_factor=0.5,
			popularity_factor=0.5,
			area=100.0,
			longitude=10.0,
			latitude=20.0,
			floor=1,
			borders=[[1.1, 1.0], [1.2, 1.0], [1.2, 1.0]],
		)
		for i in range(num)
	]


def test_bulk_create_rooms():
	"""Test bulk creation of rooms."""
	rooms = generate_rooms(5)
	for room in rooms:
		room.save()
	count = Room.objects(type='OFFICE').count()
	assert count == 5
	for room in rooms:
		room.delete()


def test_bulk_update_rooms():
	"""Test bulk updating of rooms."""
	rooms = generate_rooms(5)
	for room in rooms:
		room.save()
	Room.objects(type='OFFICE').update(crowd_factor=0.8)
	updated_rooms = Room.objects(type='OFFICE')
	for room in updated_rooms:
		assert room.crowd_factor == 0.8
	for room in rooms:
		room.delete()


def test_bulk_delete_rooms():
	"""Test bulk deletion of rooms."""
	rooms = generate_rooms(5)
	for room in rooms:
		room.save()
	Room.objects(type='OFFICE').delete()
	assert Room.objects(type='OFFICE').count() == 0
