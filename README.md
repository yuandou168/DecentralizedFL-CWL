# This repository contains our Proof Of Concept of CWL-FLOps for Decentralized Federated Learning

> **_Please note:_** In this project we have used Federated Learning source code based on the repository mentioned in the Acknowledgments section
>
## Description:
- This project provides Decentralized Federated Learning scenario implementation based on CWL workflows.
- Our CWL workflows include 12 training rounds of federated learning based on MNIST dataset.
- Since we focus on Decentralized Federated learning scenario, our CWL workflow randomly select one of the clients to act as the aggregator for each training round to update the global model from the received client weights.
## Federation Structure :

- Federation structure in this demo
  - Clients:
      
      In this project, we assume all clients that participate in the Federated Learning experiments/training are running the necessary Docker compose files from `docker_compose_files/decentralized_compose.yml`.
      In our demo we used AWS EC2 instances to represent FL client nodes.



  - Communication server:

      This is a simple server used by the client docker containers to send their availability and participate in the FL experiments.
      
      The server is created with the following terraform template : `communication_server/main.tf`

## Architecture 
![architecture_final](https://github.com/ResearchDemo23/DecentralizedFL-CWL/assets/143496839/25be4f15-ed96-4f64-9d00-9723e294ee5f)


## Video demonstration 



https://github.com/ResearchDemo23/DecentralizedFL-CWL/assets/143496839/2b4879cf-353d-44fb-b644-e4d4df1dba17



## Using this demo: 
> **_Please note:_** We are not responsible for any use or misuse of the code or its consequences. For example we are not responsible for any expenses if you are using your own AWS account while using this demo nor for any security concerns.
>
- Changes needed:
  - Creating docker images for client training based on `Dockers_source_code/client_training`, `Dockers_source_code/client_registration` and `Dockers_source_code/communication_server` and pushing them to your own docker hub to be used in the experiments.
  - Change the docker compose file `docker_compose_files/decentralized_compose.yml` with the name of your docker images
  - Change the terraform template of the communication server based on your own aws configuration and your own name for the `Dockers_source_code/communication_server` docker image created.
- FL clients state before running the experiment: 
  - Clients that want to participate in the FL experiments should be running the docker compose file `docker_compose_files/decentralized_compose.yml` and also have created an empty weight file in their directory with `.pt` extension.

- Experiment Setup:
    1. Assuming you have already forked/cloned the repo
    2. Create the following github actions secrets based on your AWS account:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - DOCKER_PASSWORD
        - DOCKER_USERNAME
    3. Replace tags for building and pushing images based on your dockerhub name in the following github actions workflows: `.github/workflows/decentralized_training.yml` , `.github/workflows/client_register.yml` and `.github/workflows/communication_server.yml`.
- If you want to provision an AWS EC2 instance based on the terraform template, as the communication server and run experiment do the following:
    - Run manually the workflow from terminal with: `gh workflow run`
    - Select the FL experiment (CWL_workflow_experiment_infrastructure_provision.yml) option
    - run `gh run watch` to watch the jobs status
    - go to actions and check the progress of the `CWL_workflow_experiment_infrastructure_provision` workflow
- If you want to run experiments based on source code changes if you have already provisioned a server for the communication server
     - Make the required changes in the source code
     - Push changes 
     - Assuming that changes are pushed from client_training, then go to actions and watch the progress of the `decentralized_training` workflow
     - Watch the progress of the `CWL_workflow_experiment` that should run as soon as the decentralized_training workflow is finished
   
## Citation:
The initial idea of this project has been published in the proceedings of the 19th  IEEE International Conference on e-Science (Link to the conference: https://www.escience-conference.org/2023/).

- Chronis Kontomaris, Yuandou Wang, and Zhiming Zhao. "CWL-FLOps: A Novel Method for Federated Learning Operations at Scale." 2023 IEEE 19th International Conference on e-Science (e-Science). IEEE Computer Society, 2023. Doi: 10.1109/e-Science58273.2023.10254788
  
- Bibtex  
@inproceedings{kontomaris2023cwl,
  title={CWL-FLOps: A Novel Method for Federated Learning Operations at Scale},
  author={Kontomaris, Chronis and Wang, Yuandou and Zhao, Zhiming},
  booktitle={2023 IEEE 19th International Conference on e-Science (e-Science)},
  pages={1--2},
  year={2023},
  organization={IEEE Computer Society}
}


## Acknowledgements
This project uses code from the following source:

- Shaoxiong Ji. (2018, March 30). A PyTorch Implementation of Federated Learning. Zenodo. [http://doi.org/10.5281/zenodo.4321561](http://doi.org/10.5281/zenodo.4321561)
