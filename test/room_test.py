from db.models import Room


def test_room_creation():
    """Test creating a Room instance."""
    room = Room(
        name="Test Room",
        type="MEETING",
        crowd_factor=1.2,
        area=40.5,
        longitude=12.34,
        latitude=56.78,
    )

    assert room.name == "Test Room"
    assert room.type == "MEETING"
    assert room.crowd_factor == 1.2
    assert room.area == 40.5
    assert room.longitude == 12.34
    assert room.latitude == 56.78
