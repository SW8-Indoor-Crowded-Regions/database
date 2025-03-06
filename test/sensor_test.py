import pytest
from db.models.sensor import Sensor
from db.models.room import Room
from mongoengine.errors import ValidationError

@pytest.fixture
def valid_room():
    room = Room(
        name="Test Room",
        type="MEETING",
        crowd_factor=0.5,
        area=100.0,
        longitude=12.34,
        latitude=56.78
    )
    room.save()
    yield room
    room.delete()

@pytest.fixture
def valid_sensor_data(valid_room):
    return {
        "name": "Test Sensor",
        "movements": [[1, 2], [3, 4]],  # List of [x, y] coordinates
        "rooms": [valid_room]
    }

def test_valid_sensor_creation(valid_sensor_data):
    sensor = Sensor(**valid_sensor_data)
    sensor.validate()  # Should not raise any exception

def test_invalid_movement_length(valid_sensor_data):
    # Test with invalid movement coordinates (too few values)
    valid_sensor_data["movements"] = [[1]]
    sensor = Sensor(**valid_sensor_data)
    with pytest.raises(ValidationError):
        sensor.validate()

    # Test with invalid movement coordinates (too many values)
    valid_sensor_data["movements"] = [[1, 2, 3]]
    sensor = Sensor(**valid_sensor_data)
    with pytest.raises(ValidationError):
        sensor.validate()

def test_empty_movements(valid_sensor_data):
    valid_sensor_data["movements"] = []
    sensor = Sensor(**valid_sensor_data)
    sensor.validate()  # Empty movements list should be valid

def test_empty_rooms(valid_sensor_data):
    valid_sensor_data["rooms"] = []
    sensor = Sensor(**valid_sensor_data)
    sensor.validate()  # Empty rooms list should be valid

def test_missing_required_fields():
    # Test creating sensor with no fields
    with pytest.raises(ValidationError):
        sensor = Sensor()
        sensor.validate()

def test_invalid_movement_values(valid_sensor_data):
    # Test with non-integer movement values
    valid_sensor_data["movements"] = [[1.5, 2.5]]
    sensor = Sensor(**valid_sensor_data)
    with pytest.raises(ValidationError):
        sensor.validate()

def test_empty_name(valid_sensor_data):
    valid_sensor_data["name"] = ""
    sensor = Sensor(**valid_sensor_data)
    with pytest.raises(ValidationError):
        sensor.validate()

def test_multiple_rooms(valid_sensor_data, valid_room):
    # Create another room
    another_room = Room(
        name="Another Room",
        type="OFFICE",
        crowd_factor=0.3,
        area=80.0,
        longitude=12.34,
        latitude=56.78
    ).save()
    
    # Test with multiple rooms
    valid_sensor_data["rooms"] = [valid_room, another_room]
    sensor = Sensor(**valid_sensor_data)
    sensor.validate()  # Should not raise any exception
    
    another_room.delete()

def test_large_movement_list(valid_sensor_data):
    # Test with a large number of movements
    valid_sensor_data["movements"] = [[i, i+1] for i in range(1000)]
    sensor = Sensor(**valid_sensor_data)
    sensor.validate()  # Should not raise any exception

def test_negative_movement_values(valid_sensor_data):
    # Test with negative movement values (should be valid as IntField allows negative values)
    valid_sensor_data["movements"] = [[-1, -2], [-3, -4]]
    sensor = Sensor(**valid_sensor_data)
    sensor.validate()  # Should not raise any exception
