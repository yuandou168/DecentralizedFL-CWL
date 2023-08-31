import io
import find_clients_native
import requests
import pathlib
import os
import sys
import random

#parallel execution library: 
from joblib import Parallel, delayed

directory = pathlib.Path(__file__).parent.resolve()

communication_server_ip = sys.argv[1]


# aggregator_hostname = 'ec2-52-87-203-241.compute-1.amazonaws.com'

rounds = ['0','1','2','3','4','5','6','7','8','9','10','11']
# rounds = ['0','1']
# rounds = ['0']

def client_local_training(local_training_args):
      round, client, round_aggregator = local_training_args
      print('client',client)
      split_url = client.split('/')
      aggregator_split_url = round_aggregator.split('/')
      #create the path for the client weights file to get based on the training round 
      client_round_file = split_url[0] + '//' + split_url[2] + f'/{round}/' + split_url[3]
      round_aggregator_url = aggregator_split_url[0] + '//' + aggregator_split_url[2] + f'/{round}/upload_weights'
      # print(client_round_file)
      client_weights = requests.get(client_round_file)
      if not os.path.exists(f'{directory}/{round}'):
          os.makedirs(f'{directory}/{round}')
      with open(f'{directory}/{round}/{split_url[3]}', "wb") as f:
          f.write(client_weights.content)
      files = {'file': (split_url[3], open(f'{directory}/{round}/{split_url[3]}', 'rb'))}
      #create the path for the aggregator link to upload the file based on the training round 

      r = requests.post(round_aggregator_url, files=files)
      # print("request post",r.status_code)

def aggregation(aggregation_args):
      client, current_round = aggregation_args
      print(client, current_round)
      client = client.split('/')
      round_aggregator_url = client[0] + '//' + client[2] + f'/{current_round}/aggregation'
      print(round_aggregator_url)
      results = requests.get(round_aggregator_url)
      return results.text

def broadcast_new_model(client_args):
      client, current_round = client_args
      split_url = client.split('/')
      client_url = split_url[0] + '//' + split_url[2] + f'/{current_round}/upload_global_model'
      # print('post client',client_url)
      files = {'file': ('global_model.pth', open(f'{directory}/{round}/global_model.pth', 'rb'))}
      #create the path for the aggregator link to upload the file based on the training round 
      r = requests.post(client_url, files=files)
      return f'send new global model to client {client}, {r.text}'


def get_global_model(aggregator_args):
    client, current_round = aggregator_args
    # print(client, current_round)
    client = client.split('/')
    round_aggregator_url = client[0] + '//' + client[2] + f'/{current_round}/global_model.pth'
    # print(round_aggregator_url)
    global_model = requests.get(round_aggregator_url)
    if not os.path.exists(f'{directory}/{round}'):
          os.makedirs(f'{directory}/{round}')
    with open(f'{directory}/{round}/global_model.pth', "wb") as f:
          f.write(global_model.content)
    return f'Got new updated global model from {round_aggregator_url}'


#get clients
clients = find_clients_native.find_clients(communication_server_ip)
#prepare the initial model
initalization_results = Parallel(n_jobs=-1, backend="threading", prefer="threads", require='sharedmem')(delayed(aggregation)((client, '0')) for client in clients)

#begin federated learning
for round in rounds:
  
  print("round",round)
  clients = find_clients_native.find_clients(communication_server_ip)
  current_aggregator = random.choice(clients)
  clients.remove(current_aggregator)

  # execute local training in parallel for al the clients 
  results = Parallel(n_jobs=-1, backend="threading",prefer="threads", require='sharedmem')(delayed(client_local_training)((round, client, current_aggregator)) for client in clients)
  #stop_aggregator_endpoint(aggregator_hostname)
  print(aggregation((current_aggregator, round)))
  print(get_global_model((current_aggregator, round)))
  broadcasts = Parallel(n_jobs=-1, backend="threading", prefer="threads", require='sharedmem')(delayed(broadcast_new_model)((client, round)) for client in clients)
