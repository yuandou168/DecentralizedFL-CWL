#!/usr/bin/env cwl-runner
cwlVersion: v1.1
class: ExpressionTool

requirements:
  - class: InlineJavascriptRequirement

inputs:
  datafile:
    type: File
    inputBinding:
      loadContents: true

outputs:
  client:
    type: string

expression: "${var lines2 = inputs.datafile.contents.split('\\n');
                var firstClient = lines2[0];
                return {'client' : firstClient } ;
              }"