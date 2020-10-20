#run on python3

import boto3

print ("---- IP movement ---------------")
print (response)

ec2 = boto3.resource('ec2')
route = ec2.Route('rtb-id','0.0.0.0/0')
response = route.replace(NetworkInterfaceId='target-nic-id')

print ("---- route change     ---------------")
print (response)


ec2 = boto3.resource('ec2')

network_interface = ec2.NetworkInterface('target-nic-id')
response = network_interface.assign_private_ip_addresses(
    AllowReassignment=True,
    PrivateIpAddresses=[
        'NAT pool ID',
    ]
)

print ("---- IP movement ---------------")
print (response)

