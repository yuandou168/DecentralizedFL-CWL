cwlVersion: v1.0
class: CommandLineTool
baseCommand: curl
requirements:
  InlineJavascriptRequirement: {}
inputs:
  client_url:
    type: string

  round :
    type: string
  # upload_state:
  #   type: File[]


arguments: 
  - valueFrom: |
  
      ${
        var lastSlashIndex = inputs.client_url.lastIndexOf("/");
        var newUrl = '';
        if (lastSlashIndex >= 0) {
          newUrl = inputs.client_url.slice(0, lastSlashIndex) + '/' + inputs.round  + '/aggregation';
          console.log(newUrl); 
        } else {
          console.log("Invalid URL");
        }
        return newUrl;
      }

outputs:
  decentralized_aggregation:
    type: stdout
  
stdout: $(('aggregation_decentralized'+inputs.round + '.txt'))