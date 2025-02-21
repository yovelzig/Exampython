
# Map user selections to ami
AMI_OPTIONS = {
    "1": "ami-0c2b8ca1dad447f8a",  
    "2": "ami-0fedcba9876543210"  
}

# Map user selections to instance types
INSTANCE_TYPES = {
    "1": "t3.small",
    "2": "t3.medium"
}

# Default AWS region
DEFAULT_REGION = "us-east-1"

# Terraform working directory and file path
TF_DIR = "./terraform_deployment"
TF_FILE = f"{TF_DIR}/main.tf"

# Terraform configuration template (Jinja2)
terraform_template  = """
provider "aws" {
  region = "{{ region }}"
}

resource "aws_instance" "web_server" {
  ami               = "{{ ami }}"
  instance_type     = "{{ instance_type }}"
  availability_zone = "{{ availability_zone }}"
  subnet_id = aws_subnet.public[0].id

  tags = {
    Name = "WebServer"
  }
}

resource "aws_lb" "application_lb" {
  name               = "{{ load_balancer_name }}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = aws_subnet.public[*].id
}

resource "aws_security_group" "lb_sg" {
  name        = "lb_security_group"
  description = "Allow HTTP inbound traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.application_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_target_group.arn
  }
}

resource "aws_lb_target_group" "web_target_group" {
  name     = "web-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group_attachment" "web_instance_attachment" {
  target_group_arn = aws_lb_target_group.web_target_group.arn
  target_id        = aws_instance.web_server.id
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = data.aws_vpc.default.id
  cidr_block        = element(["172.31.3.0/24", "172.31.4.0/24"], count.index)
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

data "aws_vpc" "default" {
  default = true
}

output "instance_id" {
  value = aws_instance.web_server.id
}

output "load_balancer_dns" {
  value = aws_lb.application_lb.dns_name
}
"""
