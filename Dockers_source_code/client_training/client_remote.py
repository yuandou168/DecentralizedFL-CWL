import logging
import os
import sys
from protos import hello_pb2, hello_pb2_grpc
import requests
import pathlib
import time
import client_details

#keep directory to map for every client's directory 
directory = pathlib.Path(__file__).parent.resolve()
initial_directory = pathlib.Path(__file__).resolve()

class File:
    def __init__(self, name, type):
        self.name = name
        self.type = type

def get_filepath(filename, extension):
    return f'{filename}{extension}'

def run(round,files,mode):
    logging.basicConfig()

    if mode == 'download':

        for file in files:
                filename = file.name
                extension = file.type
                filepath = get_filepath(filename, extension)
                print("test",round)
                #get aggregator ip from communication server first 
                aggregator_ip_url = f'http://{client_details.communication_ip}/discover_aggregator'
                aggregator_ip = requests.get(aggregator_ip_url).text
                #request from the current's round aggregator the global model
                global_model_url = f'http://{aggregator_ip}/{round}/{filepath}'
                print("url for the global model of this round is :",global_model_url)
                r = requests.get(global_model_url, allow_redirects=True)
                save_path = f'{directory}/files/{round}/'
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                if (r.content != None):
                    if os.path.isfile(save_path+filepath):
                        print("Saving new global model")
                        os.remove(f'{save_path}'+filepath)
                    with open(f'{save_path}'+filepath, mode="ab") as f:
                            if r.content is not None: 
                                f.write((r.content))
    else : 
         app.run()
         