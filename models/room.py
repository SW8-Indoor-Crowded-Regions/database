rooms_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "type", "crowdFactor", "area"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "Name of the room (string)"
            },
            "type": {
                "bsonType": "string",
                "description": "Type of the room (string or enum)",
                "enum": ["MEETING", "LOBBY", "OFFICE"]  # Add more enums if needed
            },
            "crowdFactor": {
                "bsonType": "double",
                "description": "A floating-point number representing how crowded the room is"
            },
            "area": {
                "bsonType": "double",
                "description": "Total area of the room in square units"
            }
        }
    }
}
