import pulumi

# create a new stack
import infra

# exports
pulumi.export('group_id', infra.group.id)
pulumi.export('server_id', infra.server.id)
pulumi.export('public_ip', infra.server.public_ip)
pulumi.export('public_hostname', infra.server.public_dns)
