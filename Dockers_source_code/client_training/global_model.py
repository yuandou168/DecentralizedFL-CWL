#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy
import numpy as np
from torchvision import datasets, transforms
import torch
import os 
import pathlib
import shutil
directory=pathlib.Path(__file__).parent.resolve()

from utils.sampling import mnist_iid, mnist_noniid, cifar_iid
from utils.options import args_parser
from models.Update import LocalUpdate
from models.Nets import MLP, CNNMnist, CNNCifar
from models.Fed import FedAvg
from models.test import test_img

def directory_delete(folder_path):
    # Loop over all the items in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if item_path != '/client/files/.ssh' and item_path != '/client/files/*.pt' and item_path != '/client/files/.*pth' :
            # Check if the item is a directory
            if os.path.isdir(item_path):
                # Remove all items from the directory
                shutil.rmtree(item_path)
                print("Removed items from directory:", item_path)

def execute(round, mode):
    args = args_parser()
    training_round_path = f'{directory}/files/{round}'
    if not os.path.exists(training_round_path):
          print(training_round_path)
          os.makedirs(training_round_path)
    args.device = torch.device('cuda:{}'.format(args.gpu) if torch.cuda.is_available() and args.gpu != -1 else 'cpu')
    if args.dataset == 'mnist':
            trans_mnist = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
            dataset_train = datasets.MNIST('../data/mnist/', train=True, download=True, transform=trans_mnist)
            dataset_test = datasets.MNIST('../data/mnist/', train=False, download=True, transform=trans_mnist)
    elif args.dataset == 'cifar':
            trans_cifar = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
            dataset_train = datasets.CIFAR10('../data/cifar', train=True, download=True, transform=trans_cifar)
            dataset_test = datasets.CIFAR10('../data/cifar', train=False, download=True, transform=trans_cifar)
            if args.iid:
                dict_users = cifar_iid(dataset_train, args.num_users)
            else:
                exit('Error: only consider IID setting in CIFAR10')
    else:
            exit('Error: unrecognized dataset')
    if mode == "initialization" : 
        directory_delete(f'{directory}/files/')
        os.makedirs(training_round_path)
        img_size = dataset_train[0][0].shape

        # build model
        if args.model == 'cnn' and args.dataset == 'cifar':
            net_glob = CNNCifar(args=args).to(args.device)
        elif args.model == 'cnn' and args.dataset == 'mnist':
            net_glob = CNNMnist(args=args).to(args.device)
        elif args.model == 'mlp':
            len_in = 1
            for x in img_size:
                len_in *= x
            net_glob = MLP(dim_in=len_in, dim_hidden=200, dim_out=args.num_classes).to(args.device)
        else:
            exit('Error: unrecognized model')
        net_glob.train()

        torch.save(net_glob,f'{training_round_path}/global_model.pth')
        print('Global model initialized!')

        next_round = int(round) + 1
        next_training_round_path = f'{directory}/files/{next_round}'

        if not os.path.exists(next_training_round_path):
            print(next_training_round_path)
            os.makedirs(next_training_round_path)
            print('new directory')
                
        torch.save(net_glob,f'{next_training_round_path}/global_model.pth')
        w_glob = net_glob.state_dict()
        return 'all good'
    
    if mode == "aggregation" : 

        loss_train = []
        cv_loss, cv_acc = [], []
        val_loss_pre, counter = 0, 0
        net_best = None
        best_loss = None
        val_acc_list, net_list = [], []
        participants = []

        net_glob=torch.load(f'{training_round_path}/global_model.pth')

        if args.all_clients: 
            print("Aggregation over all clients")
            w_locals = [w_glob for i in range(args.num_users)]

        for iter in range(args.epochs):
            loss_locals = []
            if not args.all_clients:
                w_locals = []

            for client_file in os.listdir(f'{training_round_path}/'):
                if client_file.endswith(".pt"):
                    print(client_file)
                    participants.append(client_file)
                    data = torch.load(os.path.join(f'{training_round_path}', client_file))
                    w = data['weights']
                    loss = data['loss']
                    if args.all_clients:
                        print("")
                    else:
                        w_locals.append(copy.deepcopy(w))
                    loss_locals.append(copy.deepcopy(loss))
            print(f"The length of my_array are {len(w_locals)}")
            w_glob = FedAvg(w_locals)

            net_glob.load_state_dict(w_glob)

            if not os.path.exists(training_round_path):
                print(training_round_path)
                os.makedirs(training_round_path)
                print('dir created')

            torch.save(net_glob,f'{training_round_path}/global_model.pth')

            next_round = int(round) + 1
            next_training_round_path = f'{directory}/files/{next_round}'

            if not os.path.exists(next_training_round_path):
                print(next_training_round_path)
                os.makedirs(next_training_round_path)
                
            torch.save(net_glob,f'{next_training_round_path}/global_model.pth')
            loss_avg = sum(loss_locals) / len(loss_locals)
            print('Round {:3d}, Average loss {:.3f}'.format(iter, loss_avg))
            loss_train.append(loss_avg)

        print("Train loss:",loss_train)
        print("Aggregation results")
        net_glob.eval()
        acc_train, loss_train = test_img(net_glob, dataset_train, args)
        acc_test, loss_test = test_img(net_glob, dataset_test, args)
        print("Training accuracy: {:.2f}".format(acc_train))
        print("Testing accuracy: {:.2f}".format(acc_test))
        str_return = "Training accuracy: {:.2f}".format(acc_train) + ", Testing accuracy: {:.2f}".format(acc_test)
        return str_return
    return 'completed'