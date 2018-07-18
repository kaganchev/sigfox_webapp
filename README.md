# sigfox_webapp
Web application for receiving messages from Sigfox IoT network and visualize them. Check https://iot.picklebit.io

## Used technologies
* Database - MongoDB
* Web app - Flask
* Python 3.5

## Endpoints
* POST /messages - recieves messages from the Sigfox network in format: 

{

  "device" : "{device}",
  
  "time" : "{time}",
  
  "data" : "{data}"
  
}

## Instructions
* Install the requirements with pip install -r requirements.txt
* Install MongoDB. This app use the default configuration of MongoDB
* Expose port 8080 to public network or use apache2.0 with mod_proxy
* Set your endpoint as Sigfox callback from the Sigfox backend with the above data format
