from fastapi import FastAPI, Request
import requests
import logging

# Configure the logging
logging.basicConfig(
     level=logging.INFO,
     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("response_logger")

# Create a FastAPI application instance
app = FastAPI()

# Define your endpoints and their handlers
@app.get("/")
def root():
    return {"message": "Hello, Luftdaten.at TTN Forwarder!"}

# endpoint for ttn uplink message
@app.post("/v3/uplink-message")
async def get_uplink_message(request: Request):
    data = await request.json()
    
    # Access the dev_eui and create x-sensor
    dev_eui = data["end_device_ids"]["dev_eui"]
    xsensor = "TTN-" + dev_eui
    
    # Access the decoded_payload field
    decoded_payload = data["uplink_message"]["decoded_payload"]

    # Access the payload values
    temperature = decoded_payload["temperature"]
    humidity = decoded_payload["humidity"]
    pm1 = decoded_payload["pm1"]
    pm2p5 = decoded_payload["pm2p5"]
    pm10 = decoded_payload["pm10"]
    
    # Send the values to sensor.community    
    headers = {
      "Content-Type": "application/json",
      "X-Pin": "16",
      "X-Sensor": xsensor
    }

    payload = {
      "software_version": "luftdatenat-ttn-forwarder_v1",
      "sensordatavalues": [
        {"value_type": "P0", "value": pm1},
        {"value_type": "P1", "value": pm2p5},
        {"value_type": "P2", "value": pm10},
        {"value_type": "temperature", "value": temperature},
        {"value_type": "humidity", "value": humidity},
      ]
    }   
    
    url = "https://api.sensor.community/v1/push-sensor-data/"
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Handle the response from the API
    if response.status_code == 200:
        # Request was successful
        response_data = response.json()
        # Log the response data
        logger.info(response_data)
    