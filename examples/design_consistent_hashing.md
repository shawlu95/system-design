# DESIGN CONSISTENT HASHING

## Naive Hashing

The most naive hashing is to take modulo of request's hash, and use the remainder as server index

- cons: only works when server count is fixed. When server is added or removed, lots of hash keys need to be reshuffled

## Consistent Hashing

Visualize hash space as a ring. Hash the servers and assign them to the ring (each occupies a slot). When a request is hashed, it falls somewhere on the ring. To assign a request to a server, move clockwise and see which server it hits first.

Pros:

- minimize keys distributed when server is added or removed
- when a server is removed, its key will be distributed to the next server
- when a server is added, only some of the previous server's keys will be distributed to the new servers

Cons:

- partitions are not evenly distributed, can cause hotspot

To resolve: each server gets multiple virtual nodes. The more virtual nodes, the smaller the standard deviation of traffic on each virtual nodes.

- easy to scale horizontally
- mitigate hotspot (hotkey) problem

## Real-world

- Amazon Dynamo, Apache Cassandra
- CDN Akamai
- Google load balancer
