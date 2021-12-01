import yaml

# Load config.yml from configuration folder
data = yaml.safe_load(open("Configs/config.yml", mode='r'))

"""
Give bot's token key in config.yml
example: token: 123
"""
token = data['Token']

"""
Give bot's command prefix in config.yml
"""
prefix = data['Prefix']

"""
Give ticket channel in config.yml
"""
ticket_channel = data['ticket-channel']

"""
Give support-role in config.yml
"""
support_role = data['support-role']

message = {}

message['status_1'] = "Create a ticket with {prefix}new".replace("{prefix}", prefix)
message['status_2'] = "Type {prefix}new for help".replace("{prefix}", prefix)
message['status_3'] = "Bot by Sinless777#6702"
message['status_4'] = "watching +help | {users:,} users in {guilds:,} servers"