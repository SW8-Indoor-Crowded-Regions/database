import pytest
from mongoengine import connect, disconnect
import mongomock
from db.models import Room
from mongoengine.errors import ValidationError

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
    room.save()  # Should save without errors
    assert Room.objects(name=valid_room_data["name"]).first() is not None

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
        room.save()  # Should save without errors
        assert Room.objects(id=room.id).first() is not None
        room.delete()

def test_all_room_types(valid_room_data):
    # Test all valid room types
    valid_types = ["MEETING", "LOBBY", "OFFICE"]
    
    for room_type in valid_types:
        valid_data = valid_room_data.copy()
        valid_data["type"] = room_type
        room = Room(**valid_data)
        room.validate()  # Should not raise any exception
        room.save()  # Should save without errors
        assert Room.objects(type=room_type).first() is not None
        room.delete()

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
        room.save()  # Should save without errors
        assert Room.objects(id=room.id).first() is not None
        room.delete()

def test_whitespace_name(valid_room_data):
    """Test that a name containing only whitespace is rejected."""
    valid_room_data["name"] = "   "
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_invalid_crowd_factor_type(valid_room_data):
    """Test that a non-numeric crowd_factor raises a ValidationError."""
    valid_room_data["crowd_factor"] = "high"
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_invalid_area_type(valid_room_data):
    """Test that a non-numeric area raises a ValidationError."""
    valid_room_data["area"] = "large"
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_invalid_longitude_type(valid_room_data):
    """Test that a non-numeric longitude raises a ValidationError."""
    valid_room_data["longitude"] = "east"
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_invalid_latitude_type(valid_room_data):
    """Test that a non-numeric latitude raises a ValidationError."""
    valid_room_data["latitude"] = "north"
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_invalid_room_type_non_string(valid_room_data):
    """Test that a room type provided as a non-string (e.g., int) raises a ValidationError."""
    valid_room_data["type"] = 123
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_name_none(valid_room_data):
    """Test that a None value for name raises a ValidationError."""
    valid_room_data["name"] = None
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_type_none(valid_room_data):
    """Test that a None value for type raises a ValidationError."""
    valid_room_data["type"] = None
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_crowd_factor_none(valid_room_data):
    """Test that a None value for crowd_factor raises a ValidationError."""
    valid_room_data["crowd_factor"] = None
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_area_none(valid_room_data):
    """Test that a None value for area raises a ValidationError."""
    valid_room_data["area"] = None
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_longitude_none(valid_room_data):
    """Test that a None value for longitude raises a ValidationError."""
    valid_room_data["longitude"] = None
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()

def test_latitude_none(valid_room_data):
    """Test that a None value for latitude raises a ValidationError."""
    valid_room_data["latitude"] = None
    room = Room(**valid_room_data)
    with pytest.raises(ValidationError):
        room.validate()