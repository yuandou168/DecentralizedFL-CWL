import matplotlib.pyplot as plt
import copy
import os
import numpy as np
from torchvision import datasets, transforms
import torch
import time 

import sys
import argparse
import pathlib

from utils.sampling import mnist_iid, mnist_noniid, cifar_iid
from utils.options import args_parser
from models.Update import LocalUpdate
from models.Nets import MLP, CNNMnist, CNNCifar
from models.Fed import FedAvg
from models.test import test_img
import client_remote
import client_details
import json

directory=pathlib.Path(__file__).parent.resolve()

def client_local(round,args_original,client_id,global_model_name,client_indexes,mnist):

    file_to_download = [ client_remote.File(name='global_model', type='.pth')]
      
    training_round_path = f'{directory}/files/{round}'
    global_model_path = f'{training_round_path}/global_model.pth'

    global_model=torch.load(global_model_path)
    local = LocalUpdate(client_id, args=args_original, dataset=mnist, idxs=client_indexes)
    weights, loss = local.train(global_model,client_id)
    print("test",weights,"loss",loss)

    state_dict = {
      'weights': weights,
      'loss': loss
    }

    weights_to_save = f'{training_round_path}/{client_details.weights_file}'

    if os.path.isfile(weights_to_save):
        print("replacing file")
        os.remove(weights_to_save)

    if not os.path.exists(training_round_path):
      os.makedirs(training_round_path)

    #Save the state_dict as a .pt file
    torch.save(state_dict, weights_to_save)
    print(f'Sending {client_details.weights_file} to the server')
    return "client weights saved!"


def central_single(round):
  args = args_parser()

  args.device = torch.device('cuda:{}'.format(args.gpu) if torch.cuda.is_available() and args.gpu != -1 else 'cpu')
  global_model=args.global_model
  print("test",args)
  args.client_id = 0
  print("argstest",args)
  if args.client_id is not None : 
      trans_mnist = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
      dataset_train = datasets.MNIST('../data/mnist/', train=True, download=True, transform=trans_mnist)
      dataset_test = datasets.MNIST('../data/mnist/', train=False, download=True, transform=trans_mnist)
      dict_users = mnist_iid(dataset_train, args.num_users)
      client_local(round,args,args.client_id,global_model,dict_users[args.client_id],dataset_train)



