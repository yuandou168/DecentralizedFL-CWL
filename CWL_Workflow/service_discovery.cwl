cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python"]
inputs:
  discover_clients_script:
    type: File
    inputBinding:
      position: 1
  communication_server_ip:
    type: string
    inputBinding:
      position: 2

outputs:
  service_discovery_output: stdout

stdout: service_discovery_state.txt