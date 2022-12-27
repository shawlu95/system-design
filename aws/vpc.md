## Virtual Private Cloud

- span multiple AZ, cannot span multiple region
- create subnet in each AZ
- for multiple region: create one VPC in each, and connect vie **VPC peering**
- default VPC uses `172.31.0.0/16`

### VPC Route Tables

- contain routing rules to determine where network traffic is directed

### Subnet

- a private subnect only allows access from within the VPC
- subnets are private by default
- **internet gateway** is required to direct public traffic to **public subnet**
  - must have a route in a route table that define internet gateway and private subnet
  - if route table is not defined, the Main Route Table will be applied

## Public Subnet

- receive traffic from an **Internet Gateway**
- must have a route defined to an internet gateway
- public IP associated with the instance
- security groups (instance) and NACL (subnet) rules allow traffic

### VPC Peering

- conenct VPC across regions
- can comminucate as if they are in the same VPC

### AWS Direct Connect

- connect on-premise data center to VPC, high-speed data transfer
- on-premise -> customer gateway (CGW) -> VPN Connection -> Virtual Private Gateway (VPG) -> VPC

# Security Groups

- virtual firewalls to an instances
- only allow rules, otherwise denied
- stateful, response to requests are allowed
- default is block inbound traffic not using the same security group, allow all outbound

### Network Access Control Lists (NACL)

- associated to a subnet (not EC2 instances)
- allow and deny rules, evaluated in number order
- default allows all inbound, outbound rules
- custom NACL denies all traffic until rules are added
- \*_stateless_: response to inbound traffic are subject to rules for outbound traffic (unlike security groups)

### Web Application Firewall (WAF)

- protect web appp & API against common web exploits
- AWS managed rules for specific applications
- IP Sets to blacklist or whitelist IP addresses
- applicable to CloudFront, Application Load Balancer, API Gateways, AWS AppSyn
