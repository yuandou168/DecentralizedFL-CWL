#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import torch
from torch import nn, autograd
from torch.utils.data import DataLoader, Dataset
import numpy as np
import random
import pickle
import os 
from sklearn import metrics

import pathlib
import client_details
#keep directory here to map for every client's directory 
directory=pathlib.Path(__file__).parent.resolve()
#get the directory one level up
directory_one_up=directory.parent
print("directory test2",directory,',',directory_one_up)

class DatasetSplit(Dataset):
    def __init__(self, dataset, idxs):
        self.dataset = dataset
        self.idxs = list(idxs)

    def __len__(self):
        return len(self.idxs)

    def __getitem__(self, item):
        image, label = self.dataset[self.idxs[item]]
        return image, label


class LocalUpdate(object):
    def __init__(self, client_id, args, dataset=None, idxs=None):
        self.args = args
        self.loss_func = nn.CrossEntropyLoss()
        self.selected_clients = []
        # print("test"+idxs)

        # dataset_object=DatasetSplit(dataset, idxs)
        # for i in range(len(dataset_object)):
        #     image, label = dataset_object[i]
        #     print(f"Image: {image}, Label: {label}")

        #-----The following lines of code are used to created partioned data for clients ----------
        # if os.path.exists(f'split_dataset{client_id}.pkl'):
        #     os.remove(f'split_dataset{client_id}.pkl')
        # with open(f'/Users/chroniskontomaris/Documents/Thesis/Toy_Federated_Horizontal/githubExamples/federated-learning/split_dataset{client_id}.pkl', 'wb') as f:
        #     print("bikame")
        #     pickle.dump(DatasetSplit(dataset, idxs), f)
        #-----End ----------


        #self.ldr_train = DataLoader(DatasetSplit(dataset, idxs), batch_size=self.args.local_bs, shuffle=True)
        
        #create train pytorch train dataset from local client dataset 
        #with open(f'{directory_one_up}/split_dataset{client_id}.pkl', 'rb') as f:
        #changed line
        dataset_path = f'{directory_one_up}/files/{client_details.dataset}'
        print("directory test",f'{directory_one_up}/files/{client_details.dataset}')
        print('lets test')
        #with open(f'{directory_one_up}/files/{client_details.dataset}', 'rb') as f:
            #loaded_split_dataset = pickle.load(f)
        #self.ldr_train = DataLoader(loaded_split_dataset, batch_size=self.args.local_bs, shuffle=True)
        #test for tomorrow (works with the new datasets created)
        loaded_split_dataset = torch.load(dataset_path)
        self.ldr_train = loaded_split_dataset

    def train(self, net, client):
        net.train()
        # train and update
        optimizer = torch.optim.SGD(net.parameters(), lr=self.args.lr, momentum=self.args.momentum)

        epoch_loss = []
        for iter in range(self.args.local_ep):
            print('I am at epoch',iter)
            batch_loss = []
            for batch_idx, (images, labels) in enumerate(self.ldr_train):
                images, labels = images.to(self.args.device), labels.to(self.args.device)
                net.zero_grad()
                log_probs = net(images)
                loss = self.loss_func(log_probs, labels)
                loss.backward()
                optimizer.step()
                if self.args.verbose and batch_idx % 10 == 0:
                    print('Update Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                        iter, batch_idx * len(images), len(self.ldr_train.dataset),
                               100. * batch_idx / len(self.ldr_train), loss.item()))
                batch_loss.append(loss.item())
            epoch_loss.append(sum(batch_loss)/len(batch_loss))
        return net.state_dict(), sum(epoch_loss) / len(epoch_loss)

