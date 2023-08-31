
  cwlVersion: v1.2
  class: Workflow

  requirements:
    ScatterFeatureRequirement: {}
    InlineJavascriptRequirement: {}
    StepInputExpressionRequirement: {}

  inputs: 

    training_round:
      type: string   

    communication_server_ip:
      type: string
    
    random_client_generator_script:
      type: File

    discover_clients_script:
      type: File
    
  outputs:

    upload_state:
      type: File[]
      outputSource: upload/upload_state

    random_output:
      type: File
      outputSource:
        random/random_output

    decentralized_aggregation:
      type: File
      outputSource:
        aggregation/decentralized_aggregation

    global_upload_state:
      type: File[]
      outputSource:
        upload_global_model/global_upload_state

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

    random:
      run: random.cwl
      in: 
        random_client_generator_script: random_client_generator_script
        client_list: get_clients/client_list
      out: [random_output]

    get_client:
      run: read_client.cwl
      in:
        datafile: random/random_output
      out: [client]
      
    update_clients:
      run: remove_client.cwl
      in:
        client_list: get_clients/client_list
        aggregator: get_client/client
      out: [clients_updated]

    receive_weights:
      run: get_weights_single.cwl
      scatter: client_url
      in:
        client_url: update_clients/clients_updated
        round: training_round
        clients_updated: update_clients/clients_updated
      out: [weights]
    
    upload:
      run: upload.cwl
      scatter: file_path2
      in: 
        file_path2: receive_weights/weights
        round: training_round
        aggregator_upload_url: get_client/client
      out: [upload_state]


    aggregation:
      run: aggregate_decentralized.cwl
      in:
        client_url: get_client/client
        round: training_round
        upload_state: upload/upload_state
      out: [decentralized_aggregation]

    get_global_model:
      run: get_global_model.cwl
      in: 
        aggregator_url: get_client/client
        round: training_round
        decentralized_aggregation: aggregation/decentralized_aggregation
      out: [global_model]

    upload_global_model:
      run: upload_global_model.cwl
      scatter: aggregator_upload_url
      in: 
        file_path2: get_global_model/global_model
        round: training_round
        aggregator_upload_url: update_clients/clients_updated

      out: [global_upload_state]
    
    print_accuracy:
      run: output_accuracy.cwl
      in: 
        datafile: aggregation/decentralized_aggregation
        training_round: training_round
        global_upload_state: upload_global_model/global_upload_state
      out: []
  
   

