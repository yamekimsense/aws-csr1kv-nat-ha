# aws-csr1kv-nat-ha

Deploy CSR1kv on AWS NAT HA using AWS python SDK (BOTO3).



## Prerequisites

Two CSR1000v

IOS-XE 17.3 or higher



## Use Case Description

CSR1kv doesn't support the stateful NAT high availability because AWS doesn't support broadcast and multicast.

Using AWS API, CSR1kv NAT HA is deployed:

    1) Private routing table is changed when failover.
    
    2) NAT IP pool is transferred when failover.



## Re-produce

1. Use BFD and EEM to detect and activate the python code.
2. Copy on the guestshell of CSR1kv on both CSR1kv.
3. Modify the NAT IP pool, route and NIC of AWS.
4. Install AWS CLI and BOTO3 - AWS python SDK.


## Result

When the active CSR1000v is down and BFD down was detected, the standby becomes active.

When becomes active, the python code is executed by EEM.

The python code changes the NAT IP from active to standby and modifies the route of private.


## Reference

AWS BOTO3 API: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html


## Youtube Video

[![AWS-CSR1kv-HA-NAT](https://i9.ytimg.com/vi_webp/ZT4mD4NAQfU/mqdefault.webp?time=1603884000000&sqp=COCn5fwF&rs=AOn4CLDL0XQfNwy3c8NW5OzVr_6YXnS_Kg)](https://youtu.be/ZT4mD4NAQfU "AWS-CSR1kv-HA-NAT")


## CSR1000v Configuration


CSR1kv cli command:



!

interface Tunnel1

  ip address 192.168.1.1 255.255.255.0 

  bfd interval 500 min_rx 500 multiplier 3

  tunnel source GigabitEthernet1

  tunnel destination <peer public IP>

!

interface GigabitEthernet1

  ip address <public IP>

  ip nat outside

  redundancy rii 100

  redundancy group 1 decrement 100

!

interface GigabitEthernet2

  ip address <private IP>

  ip nat inside

  redundancy rii 200

  redundancy group 1 ip <virtual IP> exclusive decrement 100

!

!

router eigrp 1

  bfd interface Tunnel1

  network 192.168.1.0

  passive-interface GigabitEthernet1





ip nat pool test <NAT IP POOL> <NAT IP POOL>  prefix-length mask-length

ip nat inside source list 10 pool test redundancy 1 mapping-id 1 overload



ip access-list standard 10

  10 <Access for NAT>



event manager applet ha

  event syslog pattern "RG id 1 role change from Standby to Active"

  action 220 cli command "enable"

  action 330 cli command "guestshell run sudo python3 /home/guestshell/a010-csr1kv-nat-ha.py.py"

