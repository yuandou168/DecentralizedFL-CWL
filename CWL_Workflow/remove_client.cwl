#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: ExpressionTool

requirements:
  - class: InlineJavascriptRequirement

inputs:
  client_list:
    type: string[]
    inputBinding:
      loadContents: true
  aggregator:
    type: string

outputs:
  clients_updated:
    type: string[]

expression: "${var new_clients = inputs.client_list.filter(e => e !== inputs.aggregator);
                return {'clients_updated' : new_clients } ;
              }"