import requests
import yaml



def find_clients(information_server_ip):

    response = requests.get(f'http://{information_server_ip}:8088/discover')
    json_data = response.json()
    # Extract the client IP and weights from the JSON data
    clients = ['http://{}/{}'.format(item['client_ip'], item['weights']) for item in json_data]
    return clients
