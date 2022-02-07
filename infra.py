import pulumi
import pulumi_aws as aws

# config
config = pulumi.Config()

ip_address = config.require_secret('ip_address')
key_pair = config.require_secret('key_pair')

# create resources
group = aws.ec2.SecurityGroup(
  'webserver-sg',
  description='enable http & ssh access',
  ingress=[
    {'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': [ip_address]},
    {'protocol': 'tcp', 'from_port': 80, 'to_port': 80, 'cidr_blocks': ['0.0.0.0/0']}
  ]
)

ami = aws.ec2.get_ami(
  most_recent=True,
  owners=['137112412989'],
  filters=[{'name': 'name', 'values': ['amzn2-ami-kernel-5.10-hvm-*']}]
)

user_data = """
#!/bin/bash
echo 'Hello, World!' > index.html
nohup python -m SimpleHTTPServer 80 &
"""

server = aws.ec2.Instance(
  'webserver',
  instance_type='t2.micro',
  vpc_security_group_ids=[group.id],
  user_data=user_data,
  ami=ami.id,
  key_name=key_pair,
  tags={
    'Name': 'webserver'
  }
)
