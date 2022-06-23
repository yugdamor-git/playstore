package_schema = {
    "type": "object",
    "properties": {
        "package_name": {
            "type": "string",
        },
        "data": {
            "type": "object"
        },
    },
    "required": [],
    "additionalProperties": True
}


app_schema = {
    "type": "object",
    "properties": {
        "app_id": {
            "type": "string",
        },
        "data": {
            "type": "object"
        },
    },
    "required": [],
    "additionalProperties": True
}