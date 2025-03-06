import pytest
from db.models import Room
from mongoengine.errors import ValidationError

@pytest.fixture
def valid_room_data():
    return {
        "name": "Test Room",
        "type": "MEETING",
        "crowd_factor": 0.5,
        "area": 100.0,
        "longitude": 12.34,
        "latitude": 56.78
    }

def test_valid_room_creation(valid_room_data):
    room = Room(**valid_room_data)
    room.validate()  # Should not raise any exception

def test_invalid_room_type(valid_room_data):
    valid_room_data["type"] = "INVALID_TYPE"
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_negative_values(valid_room_data):
    # Test each numeric field with negative values
    numeric_fields = ["crowd_factor", "area", "longitude", "latitude"]
    
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
    numeric_fields = ["crowd_factor", "area", "longitude", "latitude"]
    
    for field in numeric_fields:
        valid_data = valid_room_data.copy()
        valid_data[field] = 0.0
        room = Room(**valid_data)
        room.validate()  # Should not raise any exception

def test_all_room_types(valid_room_data):
    # Test all valid room types
    valid_types = ["MEETING", "LOBBY", "OFFICE"]
    
    for room_type in valid_types:
        valid_data = valid_room_data.copy()
        valid_data["type"] = room_type
        room = Room(**valid_data)
        room.validate()  # Should not raise any exception

def test_empty_name(valid_room_data):
    valid_room_data["name"] = ""
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_very_large_values(valid_room_data):
    # Test with very large values (should be valid)
    numeric_fields = ["crowd_factor", "area", "longitude", "latitude"]
    
    for field in numeric_fields:
        valid_data = valid_room_data.copy()
        valid_data[field] = 1e10  # Very large number
        room = Room(**valid_data)
        room.validate()  # Should not raise any exception
