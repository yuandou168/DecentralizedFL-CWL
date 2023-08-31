import requests
import json
import time
import sys
import pathlib
import os 

# Define the endpoint URL for the discovery server
DISCOVERY_SERVER_URL = f'{sys.argv[1]}:8088'
directory=pathlib.Path(__file__).parent.resolve()

# Get the client IP address
client_ip = requests.get('http://checkip.amazonaws.com/').text.strip()

host_directory = f'{directory}/files'
# Get the name of the .pt file in the current directory
weights_file = next((f for f in os.listdir(f'{host_directory}/') if f.endswith('.pt')), None)

# Create the JSON object
data = {
    "weights": weights_file,
    "client_ip": client_ip + ":3000",
    "last_seen": "0"
}

# Define the name of the output file
output_file = 'client_info.json'

# Check if the output file already exists
if os.path.exists(f'{host_directory}/{output_file}'):
    # If it does, load its contents into a dictionary
    with open(f'{host_directory}/{output_file}', 'r') as f:
        data = json.load(f)
else:
    # If it doesn't, create a new dictionary
    data = {}

# Update the dictionary with the new data
data['weights'] = weights_file
data['client_ip'] = client_ip + ":3000"
data['last_seen'] = "0"

# Write the updated dictionary back to the output file
with open(f'{host_directory}/{output_file}', 'w') as f:
    json.dump(data, f)

while True:
 with open(f'{host_directory}/client_info.json') as fp:
    data = json.load(fp)
 print("Success",data)
    
 # Send a POST request to register the service with the discovery server
 response = requests.post(f'{DISCOVERY_SERVER_URL}/register', json=data)

 if response.status_code == 200:
    print('Service registered successfully')
 else:
    print(f'Error registering service: {response.text}')
 time.sleep(7)
