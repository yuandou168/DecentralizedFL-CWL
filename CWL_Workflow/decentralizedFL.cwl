#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

$namespaces:
  cwltool: "http://commonwl.org/cwltool#"
  s: https://schema.org/

$schemas:
 - https://schema.org/version/latest/schemaorg-current-http.rdf
 
requirements:
  InlineJavascriptRequirement: {}
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  ScatterFeatureRequirement: {}

inputs: 
  rounds:
    type: int
  round:
    type: string
  communication_server_ip:
    type: string
  discover_clients_script:
    type: File
  random_client_generator_script:
    type: File


outputs: []
    # accuracy:
    #   type: File[]
    #   outputSource: 
    #     decentralized_training_round/output_model
    
steps:
  discover:
    run: service_discovery.cwl
    in:
      communication_server_ip: communication_server_ip
      discover_clients_script: discover_clients_script
    out: [service_discovery_output]

  get_clients:
    run: read_clients.cwl
    in:
      datafile: discover/service_discovery_output
    out: [client_list]
      
  initialization:
    run: initialize_decentralized.cwl
    scatter: client_url
    in: 
      client_url: get_clients/client_list
      round: round
    out: [initialize_decentralized]
    
  decentralized_training_round:
    in:
      round:
        default: 0
      rounds: rounds
      clients: get_clients/client_list
      discover_clients_script: discover_clients_script
      random_client_generator_script: random_client_generator_script
      communication_server_ip: communication_server_ip
      initialize_decentralized: initialization/initialize_decentralized

    # out: [output_model]
    out: []
    requirements:
      cwltool:Loop:
        loopWhen: $(inputs.round < inputs.rounds)
        loop:
          round:
            valueFrom: $(inputs.round + 1)
          # input_model: output_model
        outputMethod:  all
    run:
      class: Workflow
      inputs:

        round:
          type: int

        communication_server_ip:
          type: string
        
        discover_clients_script:
          type: File

        random_client_generator_script:
          type: File

      outputs: []
        # output_model:
        #   type: File
        #   outputSource:
        #     decentralized_federated_learning_round/accuracy

      steps:

        decentralized_federated_learning_round:
          run: rest_parallel.cwl
          in: 
            round: round
            training_round: 
              valueFrom: $(String(inputs.round))
            discover_clients_script: discover_clients_script
            random_client_generator_script: random_client_generator_script
            communication_server_ip: communication_server_ip
          out: []

  
