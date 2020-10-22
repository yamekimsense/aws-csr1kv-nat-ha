# aws-csr1kv-nat-ha

Deploy CSR1kv on AWS NAT HA using AWS python SDK (BOTO3).



## Use Case Description

CSR1kv doesn't support the stateful NAT high availability because AWS doesn't support broadcast and multicast.
Using AWS API, CSR1kv NAT HA is deployed:
    1) Private routing table is changed when failover.
    2) NAT IP pool is transferred when failover.


## Installation

Use BFD and EEM to detect and activate the python code.
Install on the guestshell of CSR1kv on both CSR1kv.
Modify the NAT IP pool, route and NIC of AWS.
Install AWS CLI and BOTO3 - AWS python SDK.


## Configuration

Modify the NAT IP pool, route and NIC of AWS.

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
 action 330 cli command "guestshell run sudo python3 /home/guestshell/python-code-name.py"






## Usage

Modify the CLI config.
Copy to the guestshell with AWS CLI install and BOTO3 install.



### DevNet Sandbox

[DevNet Sandbox](https://developer.cisco.com/site/sandbox/)


## How to test the software

Config two CSR1kv.
Config BFD, NAT, and EEM with code above.
Copy and modify the python code after install CLI and BOTO3.
Make the failover using reload or tunnel down.


## Known issues

none.



## Getting help

Contact me.




## Getting involved

Works on python3.



## Credits and references

This is just experimental code and not for cisco offical support.

For the official guide visit : https://www.cisco.com/c/en/us/support/docs/cloud-systems-management/prime-access-registrar/213601-csr1000v-ha-redundancy-deployment-guide.html

----

## Licensing info

See the license file.
