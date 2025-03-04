# sensor.py

sensors_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "movements", "roomId"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "Name or identifier for the sensor"
            },
            "movements": {
                "bsonType": "array",
                "description": "An array of tuples of two integers representing movements (e.g., counts in two directions)",
                "items": {
                    "bsonType": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "bsonType": "int",
                        "description": "Each tuple element should be an integer"
                    }
                }
            },
            "roomId": {
                "bsonType": "objectId",
                "description": "Reference to the room this sensor is installed in"
            }
        }
    }
}
