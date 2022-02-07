import unittest
import pulumi

pulumi.runtime.set_all_config({
  'project:ip_address': pulumi.Output.secret('121.249.192.15/32'), # arbitrary ip addr.
  'project:key_pair': pulumi.Output.secret('test_key_pair')
})

class MyMocks(pulumi.runtime.Mocks):
  def new_resource(self, args: pulumi.runtime.MockResourceArgs):
    outputs = args.inputs
    if args.typ == 'aws:ec2/instance:Instance':
      outputs = {
        **args.inputs,
        'publicIp': '203.0.113.12',
        'publicDns': 'ec2-203-0-113-12.ap-northeast-1.compute.amazonaws.com',
      }
    return [args.name + '_id', outputs]
  def call(self, args: pulumi.runtime.MockCallArgs):
    if args.token == 'aws:ec2/getAmi:getAmi':
      return {
        'architecture': 'x86_64',
        'id': 'ami-0c635ee4f691a2310'
      }
    return {}

pulumi.runtime.set_mocks(MyMocks())

import infra

class TestingWithMocks(unittest.TestCase):
  # check 1: instances have a Name tag
  @pulumi.runtime.test
  def test_server_tags(self):
    def check_tags(args):
      urn, tags = args
      self.assertIsNotNone(tags, f'server {urn} must have tags')
      self.assertIn('Name', tags, f'server {urn} must have a name tag')

    return pulumi.Output.all(infra.server.urn, infra.server.tags).apply(check_tags)

  # check 2: instances must not use an inline user data script
  @pulumi.runtime.test
  def test_server_user_data(self):
    def check_user_data(args):
      urn, user_data = args
      self.assertFalse(user_data, f'server {urn} must not use inline user data')

    return pulumi.Output.all(infra.server.urn, infra.server.user_data).apply(check_user_data)

  # check 3: instances must not have port 22 for ssh exposed
  @pulumi.runtime.test
  def test_security_group_rules(self):
    def check_security_group_rules(args):
      urn, ingress = args
      ssh_open = any([rule['from_port'] == 22 and any([block == '0.0.0.0/0' for block in rule['cidr_blocks']]) for rule in ingress])
      self.assertFalse(ssh_open, f'server {urn} must not have port 22 exposed to the Internet')

    return pulumi.Output.all(infra.server.urn, infra.group.ingress).apply(check_security_group_rules)
