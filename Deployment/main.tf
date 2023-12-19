terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}


# Configure the AWS Provider
provider "aws" {
  profile = "terraform-user"
  region  = "us-east-1"
}

# EC2 instance
resource "aws_instance" "blogverse" {

  ami             = "ami-01bc990364452ab3e"
  instance_type   = "t2.micro"
  key_name        = "test-key"
  security_groups = ["launch-wizard-1"]

  user_data = file("userdata.sh")


  root_block_device {
    volume_size = 10
    volume_type = "gp3"

  }

  tags = {
    Name = "blogverse-server"
  }

}
# key pair 

# security group

