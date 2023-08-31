cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python"]
inputs:
  random_client_generator_script: 
    type: File
    inputBinding:
      position: 1
  client_list:
    type: string[]
    inputBinding:
      position: 2


outputs:
  random_output: stdout

stdout: random_output.txt