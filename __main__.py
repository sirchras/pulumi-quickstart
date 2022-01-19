import pulumi
import pulumi_aws as aws

# config
config = pulumi.Config()

ip_address = config.require_secret('ip_address')
key_pair = config.require_secret('key_pair')

# create resources
ami = aws.ec2.get_ami(
  most_recent=True,
  owners=['137112412989'],
  filters=[{'name': 'name', 'values': ['amzn-ami-hvm-*']}]
)

group = aws.ec2.SecurityGroup(
  'webserver-sg',
  description='enable ssh access',
  ingress=[
    {'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': [ip_address]}
  ]
)

server = aws.ec2.Instance(
  'webserver',
  instance_type='t2.micro',
  vpc_security_group_ids=[group.id],
  ami=ami.id,
  key_name=key_pair,
  tags={
    'Name': 'webserver'
  }
)

# exports
pulumi.export('public_ip', server.public_ip)
pulumi.export('public_hostname', server.public_dns)
