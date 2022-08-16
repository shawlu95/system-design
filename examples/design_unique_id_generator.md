# Unique ID Generator

### 1. Understand the Problem and Scope

- id should be unique and sortable
- id does not have to increment by 1
- id only contains numeric value
- id should fit into 64 bit
- throughput 10,000 ID per second

### 2. Propose High-level Design

#### Multi-master Replication

- if a cluster has N machine, each machine increment ID by N at a time
- cons: hard to scale, remove/add server, ID does not go up with time across server (not sortable)

#### UUID

- 128 bit number
- generated independently without communication across server
- do not go up with time

#### Ticket Server

- has one server counting ID and serves get request
- pros: easy, fit small-scale app
- cons: single point of failure; synchronization issue if more than one ticket servers

### 3. Design Deep Dive: Twitter snowflake

Divide the 64 bit into different parts, from left to right:

- 1 bit: for sign
- 41 bit: milliseconds to be added to genesis timestamp, loop over in 69 years
- 5 bit: data center ID (2^5 = 32 centers)
- 5 bit: machine ID per data center
- 12 bit: sequence number, reset every millisecond (timestamp smallest unit)

### 4. Wrap-up

- each machine can generate 2^12 = 4096 per millisecond, or 4,096,000 per second
- with 32 data centers, 32 machine in each center, the whole system can generate 4,194,304,000 ID per seconds
- assume servers have the same clocks (use Network Time Protocol to sync server time, beyond the scope)
