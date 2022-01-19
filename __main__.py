import pulumi
import pulumi_aws as aws

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
    {'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['202.27.76.248/32']}
  ]
)

server = aws.ec2.Instance(
  'webserver',
  instance_type='t2.micro',
  vpc_security_group_ids=[group.id],
  ami=ami.id
)

# exports
pulumi.export('public_ip', server.public_ip)
pulumi.export('public_hostname', server.public_dns)
