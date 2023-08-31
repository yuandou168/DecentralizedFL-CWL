from flask import Flask, send_file, request, send_from_directory 
import client
import client_details
import yaml
import pathlib
import glob
from utils.options import args_parser
import global_model
import argparse
import shutil

import json
import os
import sys

app = Flask(__name__)
#keep directory here to map for every client's directory 
directory=pathlib.Path(__file__).parent.resolve()
args = args_parser()


@app.route(f'/<round>/{client_details.weights_file}')
def download_file(round):
    print("test flask", round)
    client.central_single(round)
    training_round_path_file = f'{directory}/files/{round}/{client_details.weights_file}'
    #for each training round check if the folder exists, then the training round already exists and we send the file
    
    file_path = training_round_path_file
    print(f'Sending {file_path} for the aggregator to download')
    return send_file(file_path, as_attachment=True)


@app.route('/')
def test():
    return f'Hello, World from {client_details.weights_file} and watchover!'

@app.route('/<round>/global_model.pth')
def download_global_model(round):

    training_round_path = f'{directory}/files/{round}'
    file_path = f'{training_round_path}/global_model.pth'
    return send_file(file_path, as_attachment=True)

@app.route('/<round>/aggregation')
def execute_aggregation(round):
    if round == '0' :
        mode = 'initialization'
        result = global_model.execute(round, mode)
    else :
        mode = 'aggregation'
        result = global_model.execute(round, mode) 
    return result


@app.route('/<round>/upload_global_model', methods=['POST'])
def received_peer_global_model(round):

    if 'file' not in request.files:
        return 'No file part in the request'

    file = request.files['file']

    current_directory = f'{directory}/files/{round}'
    current_file_path = f'{current_directory}/{file.filename}'
    if not os.path.exists(current_directory):
            os.makedirs(current_directory)
            print('made new directory for current round ')
    if os.path.exists(current_file_path):
            os.remove(current_file_path)
            print(f"File {current_file_path} deleted successfully.")
    file.save(current_file_path)
    next_round = int(round)+1
    dir_new = f'{directory}/files/{next_round}'
    file_path = f'{dir_new}/{file.filename}'
    if not os.path.exists(dir_new):
        os.makedirs(dir_new)
        print('made new directory for next round with',file_path)
    shutil.copyfile(current_file_path,file_path)
    return 'File uploaded successfully'


@app.route('/<round>/upload_weights', methods=['POST'])
def received_peer_weights(round):

    if 'file' not in request.files:
        return 'No file part in the request'

    file = request.files['file']    
    directory_new = f'{directory}/files/{round}'
    if not os.path.exists(directory_new):
                os.makedirs(directory_new)
    file_path = f'{directory_new}/{file.filename}'
    # if file exists then we have to delete it and replace it 
    if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        
    file.save(file_path)
    print("test",file_path)
    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
