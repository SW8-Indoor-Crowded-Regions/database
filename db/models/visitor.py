visitors_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "visitedRooms"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "Name of the visitor"
            },
            "visitedRooms": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                },
                "description": "List of room IDs the visitor has visited"
            },
            "visitDate": {
                "bsonType": "date",
                "description": "Optional date of visit"
            }
        }
    }
}
