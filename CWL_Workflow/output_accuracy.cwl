cwlVersion: v1.2
class: CommandLineTool
baseCommand: cat
inputs:
  - id: datafile
    type: File
    inputBinding:
      position: 1
  - id: training_round
    type: string

outputs: [] 
