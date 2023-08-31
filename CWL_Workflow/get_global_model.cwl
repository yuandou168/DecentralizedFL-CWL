cwlVersion: v1.0
class: CommandLineTool
baseCommand: curl
requirements:
  InlineJavascriptRequirement: {}
inputs:
  aggregator_url:
    type: string

  round :
    type: string


arguments: 
  - valueFrom: "-O" 
  - valueFrom: |
      $(inputs.aggregator_url.split('/').slice(0, -1).concat([inputs.round, 'global_model.pth']).join('/'))
outputs:
  global_model:
    type: File
    outputBinding:
      glob:
          global_model.pth