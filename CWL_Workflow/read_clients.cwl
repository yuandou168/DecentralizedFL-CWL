#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: ExpressionTool

requirements:
  - class: InlineJavascriptRequirement

inputs:
  datafile:
    type: File
    inputBinding:
      loadContents: true

outputs:
  client_list:
    type: string[]

expression: "${var lines2 = inputs.datafile.contents.split('\\n');
                 lines2.pop();
                  return {'client_list' : lines2 } ;
              }"