from bson.objectid import ObjectId
from pymongo import MongoClient
from jsonschema import validate, ValidationError

message_schema = {
    "type": "object",
    "properties": {
        "device": {"type": "string"},
        "time": {"type": "string"},
        "data": {"type": "string"},
        "latitude": {"type": "number"},
        "longitude": {"type": "number"},
        "temperature": {"type": "number"},
        "voltage": {"type": "number"}
    },
    "required": ["device", "time", "data", "latitude", "longitude", "temperature", "voltage"],
    "additionaProperties": False
}

def insert_message(data):

    # Validate the data
    try:
        validate(data, message_schema)
    except ValidationError as exception:
        return exception

    # Create database client and connect to the sigfox client
    client = MongoClient()
    db = client.sigfox
    messages = db.messages
    messages.insert_one(data)

    # Close the connection 
    client.close()
    return None

def find_all_devices():
    client = MongoClient()
    db = client.sigfox
    messages = db.messages

    pipeline = [{"$group": {'_id': {"device": "$device"}}}]
    devices = messages.aggregate(pipeline)
    devices_list = []
    for device in list(devices):
        devices_list.append(device['_id'])
    
    client.close()
    return devices_list

def find_messages_by_device(device):
    client = MongoClient()
    db = client.sigfox
    messages = db.messages

    messages_list = list(messages.find({"device": device}))
    client.close()
    return messages_list

def find_message_by_id(message_id):
    client = MongoClient()
    db = client.sigfox
    messages = db.messages

    message = list(messages.find_one({'_id': ObjectId(message_id)}))
    client.close()

    return message