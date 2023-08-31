import requests
import yaml
import sys 
# Get the JSON response from the link
information_server_ip = sys.argv[1]

response = requests.get(f'{information_server_ip}:8088/discover')
json_data = response.json()

# Extract the client IP and weights from the JSON data
clients = ['http://{}/{}'.format(item['client_ip'], item['weights']) for item in json_data]
#output the clients to the stdout
for client in clients: 
    print(client)

