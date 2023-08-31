from flask import Flask, jsonify, request
import json
import time

from waitress import serve
from numpy import size
app = Flask(__name__)

services = []
aggregator_ip = []

# Register a service with the central server
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    data['last_seen'] = int(time.time()) 
    services.append(data)
    return 'OK'

# Discover available services
@app.route('/discover', methods=['GET'])
def discover():
    if size(services) > 0:
        return list({item['client_ip']: item for item in services if (time.time() - item['last_seen']) <= 10 }.values())
    else:
        return services
    
@app.route('/register_aggregator', methods=['POST'])
def aggregator_register():
    aggregator_ip.append(request.data)
    return 'Aggregator registered successfully'


@app.route('/discover_aggregator', methods=['GET'])
def aggregator_discover():
    return aggregator_ip[0]

if __name__ == '__main__':
    serve(app,host="0.0.0.0", port=8088)
