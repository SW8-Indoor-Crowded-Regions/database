import pytest
from mongoengine import connect, disconnect
import mongomock
from db.models import Room, Sensor

@pytest.fixture(autouse=True)
def setup_mock_db():
    """Setup mock database before each test."""
    disconnect()  # Disconnect from any previous connections
    
    # Connect to a mock MongoDB instance
    connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient, uuidRepresentation='standard')
    
    yield  # Run the test
    
    # Cleanup after test
    disconnect()

@pytest.fixture
def sample_room():
    """Create a sample room for testing."""
    room = Room(
        name="Mock Room",
        type="OFFICE",
        crowd_factor=0.7,
        area=120.0,
        longitude=10.0,
        latitude=20.0
    ).save()
    yield room
    room.delete()

@pytest.fixture
def sample_sensor(sample_room):
    """Create a sample sensor for testing."""
    sensor = Sensor(
        name="Mock Sensor",
        movements=[[1, 1], [2, 2]],
        rooms=[sample_room]
    ).save()
    yield sensor
    sensor.delete()

def test_mock_room_creation():
    """Demonstrate creating and querying a room with mock database."""
    # Create a room
    Room(
        name="Test Room",
        type="MEETING",
        crowd_factor=0.5,
        area=100.0,
        longitude=15.0,
        latitude=25.0
    ).save()

    # Query the room
    found_room = Room.objects(name="Test Room").first()
    assert found_room is not None
    assert found_room.type == "MEETING"
    assert found_room.area == 100.0

    # Update the room
    found_room.update(crowd_factor=0.8)
    updated_room = Room.objects(id=found_room.id).first()
    assert updated_room.crowd_factor == 0.8

    # Delete the room
    found_room.delete()
    assert Room.objects(name="Test Room").first() is None

def test_mock_sensor_with_room(sample_room):
    """Demonstrate sensor operations with referenced room using mock database."""
    # Create a sensor referencing the room
    Sensor(
        name="Test Sensor",
        movements=[[1, 2], [3, 4]],
        rooms=[sample_room]
    ).save()

    # Query and verify sensor with room reference
    found_sensor = Sensor.objects(name="Test Sensor").first()
    assert found_sensor is not None
    assert len(found_sensor.rooms) == 1
    assert found_sensor.rooms[0].name == sample_room.name

    # Test updating sensor movements
    new_movements = [[5, 6], [7, 8]]
    found_sensor.update(movements=new_movements)
    updated_sensor = Sensor.objects(id=found_sensor.id).first()
    assert updated_sensor.movements == new_movements

def test_mock_querying_multiple_rooms():
    """Demonstrate querying capabilities with mock database."""
    # Create multiple rooms
    rooms = [
        Room(name="Room 1", type="OFFICE", crowd_factor=0.5, area=100.0, longitude=10.0, latitude=20.0),
        Room(name="Room 2", type="MEETING", crowd_factor=0.7, area=150.0, longitude=11.0, latitude=21.0),
        Room(name="Room 3", type="LOBBY", crowd_factor=0.3, area=200.0, longitude=12.0, latitude=22.0)
    ]
    for room in rooms:
        room.save()

    # Demonstrate different query operations
    # Query by type
    office_rooms = Room.objects(type="OFFICE")
    assert len(office_rooms) == 1
    assert office_rooms[0].name == "Room 1"

    # Query by area range
    large_rooms = Room.objects(area__gte=150.0)
    assert len(large_rooms) == 2

    # Query by multiple conditions
    specific_rooms = Room.objects(type="MEETING", crowd_factor__gte=0.6)
    assert len(specific_rooms) == 1
    assert specific_rooms[0].name == "Room 2"

    # Cleanup
    for room in rooms:
        room.delete()

def test_mock_bulk_operations():
    """Demonstrate bulk operations with mock database."""
    # Bulk create rooms
    rooms_data = [
        {"name": f"Room {i}", "type": "OFFICE", "crowd_factor": 0.5, 
         "area": 100.0, "longitude": 10.0, "latitude": 20.0}
        for i in range(5)
    ]
    [Room(**data).save() for data in rooms_data]

    # Bulk update
    Room.objects(type="OFFICE").update(crowd_factor=0.8)
    updated_rooms = Room.objects(type="OFFICE")
    assert all(room.crowd_factor == 0.8 for room in updated_rooms)

    # Bulk delete
    Room.objects(type="OFFICE").delete()
    assert Room.objects(type="OFFICE").count() == 0
