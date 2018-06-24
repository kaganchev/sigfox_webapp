from bson.objectid import ObjectId
from datetime import datetime
import db_utils
from flask import Flask, request, render_template, url_for
from flask.views import View
from flask_restful import Resource, Api, reqparse, fields
from jsonschema import validate
import base64

app = Flask(__name__)
api = Api(app)

data_schema = {
    "type": "object",
    "properties": {
        "device": {"type": "string"},
        "time": {"type": "string"},
        "data": {"type": "string"},
    },
    "reqiured": ["device", "time", "data"],
    "additionalProperties": False
}

@app.route('/')
def devices():
    devices = db_utils.find_all_devices()
    for device in devices:
        device['url'] = url_for('device', device=device['device'])
    return render_template('devices.html', devices = devices)

@app.route('/device/<string:device>')
def device(device):
    messages = db_utils.find_messages_by_device(device)
    for message in messages:
        message['url'] = url_for('message', message_id =  str(message['_id']))
    return render_template('device.html', messages = messages, device = device)

@app.route('/device/messages/<string:message_id>')
def message(message_id):
    message = db_utils.find_message_by_id(message_id)

    return render_template('message.html', message = message)



class Messages(Resource):
    def post(self):
        message = request.get_json(force=True)

        try:
            validate(message, data_schema)
        except:
            return "Wrong JSON schema", 404

        data = message['data']
        
        if len(data) == 24:
            latitude = int(data[1:8], 16)
            latitude = ((latitude % 1000000) / 10000)/60 + int(latitude / 1000000)

            if bin(int(data[0], 16))[2:][0] == '0':
                message['latitude'] = round(latitude, 5)
            else:
                message['latitude'] = round(latitude, 5) * (-1)

            longitude = int(data[9:16], 16)
            longitude = ((longitude % 1000000) / 10000)/60 + int(longitude / 1000000)

            if bin(int(data[8], 16))[2:][0] == '0':
                message['longitude'] = round(longitude, 5)
            else:
                message['longitude'] = round(longitude, 5) * (-1)

            time = datetime.fromtimestamp(int(message['time'])).strftime('%Y-%m-%d %H:%M:%S')
            message['time'] = time

            temperature = int(data[18:20], 16)
            message['temperature'] = temperature

            voltage = (int(data[16:18], 16)*15)/1000
            message['voltage'] = voltage

        else:
            message['latitude'] = 0
            message['longitute'] = 0
            message['temperature'] = 0
            message['voltage'] = 0

            time = datetime.fromtimestamp(int(message['time'])).strftime('%Y-%m-%d %H:%M:%S')
            message['time'] = time

        try:
            db_utils.insert_message(message)
        except:
            return "Cannot insert message to the database", 404
        
        return data, 200

api.add_resource(Messages, '/messages')

if __name__ == '__main__':
    app.run(debug=True)