## Single-Node

Optimize read-write:

- compress value
- store frequently accessed in memory, the rest on disk

## CAP Theorem

- consistency: all clients see the same version of data
- availability: can always request even if some nodes are down
- partition tolerance: continue to operate despite network partitions

Real world implication:

- partition is not available: we must choose consistency or availability
  - choose consistency: if a partition is down, must block writes on all partitions
  - choose availability: some parittions will continue to write, others will be stale
- use consistent hashing to parittion data
  - imagine the hash ring, move a key clockwise and replicate to first N virtual servers (or unique servers, to be more fault-tolerant)
  - add and remove server depending on the node
  - number of virtual nodes is proportional to machine capacity

## Consistency

- N: number of replicas
- W: number of nodes required to confirm write success
- R: number of nodes required to confirm read success

- **strong consistency**: achieved when `W + R > B` which means at least one node will have most recent write and serve it to read request
- **optimize for read**: R = 1, W = N
- **optimize for write**: W = 1, R = N

### Vector Clock

- Each data record has a vector clock
- each entry of vector clock is `[server, version]`
- every time a write request is handled, version is incremented by 1
- no conflict, if all versions of a vector is smaller or equal (or >=) to another vector
- conflict, if some version is bigger, other version is smaller
- to optimize memory, can keep a fixed-size array of newest servers and versions

### Gosip Protocol

How to detect if a server is offline? We need other servers to tell us.

- each server keeps a membership lists (exhaustive), each member with its ID and heart beat counter (and timestamp)
- each server periodically increment heartbeat counter and sendout timestamp to _random_ set of servers
- recipient servers update the sender's heartbeat and last-seen timestamp
- when a server hasn't incremented for a long period, it is considered offline
- no single-point of failure

---

## Failure Handling

- sloppy quorum and hinted handoff handle temporary failure
- Merkle Tree handles permanent failure (anti-entropy protocol)
  - transfer tree of hashes to check for inconsistency
  - start by comparing root. If root is identical, the two nodes are exactly same version
  - if root is not same, tranverse down the tree to find which keys are inconsistent. Transfer those key-value only across networks
