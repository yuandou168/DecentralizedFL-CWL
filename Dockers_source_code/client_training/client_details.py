import json 
import pathlib
import os

from utils.options import args_parser

directory=pathlib.Path(__file__).parent.resolve()
args = args_parser()

# Find the dataset and weights file in the current directory
dataset = ''
weights_file = ''
print("details args",args)
communication_ip = f'{args.communication_ip}:8088'
for file_name in os.listdir(f'{directory}/files/'):
    if file_name.endswith(".pth"):
        dataset = file_name
    elif file_name.endswith(".pt"):
        weights_file = file_name

    # Create the JSON dictionary
    json_dict = {
        "dataset": dataset,
        "weights": weights_file,
        "communication_server_ip": communication_ip
    }

# Write the JSON dictionary to a file
with open(f'{directory}/files/information.json', "w") as f:
    json.dump(json_dict, f)
    print("JSON file created successfully!")
    
