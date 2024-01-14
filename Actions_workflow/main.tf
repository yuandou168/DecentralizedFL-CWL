


data "aws_security_group" "existing" {
  id = "sg-055359512c5897242" # Replace with the actual security group ID
}


resource "aws_instance" "communication_server" {
  ami           = "ami-0c7217cdde317cfec"  # Replace with your desired AMI ID
  instance_type = "t2.micro"
  key_name      = "YuandouAWS"
  
  tags = {
    "Name" = "Communication_server_terraform"
  }

  vpc_security_group_ids = [data.aws_security_group.existing.id]

  

  credit_specification {
    cpu_credits = "unlimited"
  }
  
  user_data = <<-EOF
      #!/bin/bash
      yum update -y
      yum install -y docker
      service docker start
      docker pull zhujiangheart/federation_server_endpoint_test:latest
      sudo docker run -p 8088:8088 -d zhujiangheart/federation_server_endpoint_test:latest 
  EOF

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 10  # Replace with your desired volume size in GB
    delete_on_termination = true
    iops                  = 3000  # Replace with your desired IOPS (optional)
  }
 
}
 output "CommunicationServerIpDecentralized" {
  description = "CommunicationServer Public IP"
  value       = aws_instance.communication_server.public_ip
 }


