## Cassandra

> The data model you use is the most important factor in your success with Cassandra.

It is more important than any config tuning. Check chapter 5.

### Elevator Pitch

> Apache Cassandra is an open source, distributed, decentralized, elastically scalable, highly available, fault-tolerant, tuneably consistent, row-oriented database. Cassandra bases its distribution design on Amazon’s Dynamo and its data model on Google’s Bigtable, with a query language similar to SQL. Created at Facebook, it now powers cloud-scale applications across many industries.

- row oriented, sparse multidimensional hash table (aka wide column store)
- Cassandra is **not** column oriented (HBase stores data by column)
- tunable consistency: `replication factor` and `consistency level`

### When to use Cassandra

- large deployment
- lots of writes throughput
- built-in support geographical distribution
- can build across multiple cloud provider, at network layer (not db layer)

```bash
docker pull cassandra
docker run --name my-cassandra cassandra
docker stop my-cassandra

docker exec -it my-cassandra cqlsh
docker start cassandra -p 9042:9042
```

### CQL & Data Model

- case in-sensitive
- text, varchar are synonymous
- `count` enforce full-table scan, expensive
- can drop column if not part of primary key

### Data Model

- **no-join**: either join from client side (bad) or denormalize the data (preferred)
- **no referential integrity** e.g. cascading delete
- query-centric design (RDBMS is data-centric)
  - minimize the number of partitions scanned in order to satisfy a query
- optimize for storage: each table is stored as separate file on disk; keep related columns in the same table
- sorting is a design choice: query cannot define how to sort, order is defiend with `create table` clustering columns
- **wide-column store** sparse multi-dimensional hashmap. each value has a key
- empty key doesn't consume space as `null` does in RDBMS
- primary key consists of partition key and clustering key
  - partition key unique determines partition
  - clustering key determines rows' order in a partition
  - primary key cannot contain null when inserting value
  - support **upsert**: insert and update is treated the same way
- column (key:val pair) -> row -> partition -> table -> keyspace -> cluster (aka ring)
- key space is similar to database in RDBMS
  - container for tables
  - define keyspace wide attributes such as replication factor
- table is a container for an ordered collection of rows
- row is a ordered collection of columns
- enum is stored as string

### Special data types

- counter: race-free increments across data center. Not idempotent
- `inet`: IPv4 or IPv6
- `timeuuid`: a nice substitute for `uuid`
- `UDT` user-defined type, considered as collection, cannot store as map value unless `frozen`

## Time

- primary key cannot have `write_time` or `ttl`
- update associates a write time to each updated column
- update can assign a `ttl` to the updated column
- insert can assign a `ttl` to the entire new row

## Architecture

gossip protocol:

- detect failure using **Phi Accrural Failure Detector** algorithm
- assess with continuous level of suspicion on whether a node has failed

snitches:

- provide information about network topology
- determine relative host proximity, and decide which nodes to read and write from

rings and token

- consistent hashing
- each node is assigned a token (an 64 bit int) and range of partition hash key
- virtual nodes are used to evenly distribute the keys
- **practitioner** convert partition column into token

replication strategy

- number of copy for your data
- defined per **keyspace**

consistency level

- number of read nodes before returning the data
- `R+W>RF` means strong consistency
- any node can accept read or write, becomes the "coordinator node"

hinted handoff

- a node will "hand off" to node B about the write
- allow Canssandra to always be available for writes

anti-entropy, repair

- use Merkle tree to reconcile conflict between replicas
- each table has its own Merkle tree

light weight transaction

- linearizable consistency
- Paxos is a consensus algo that allows distributed peer nodes to agree on a proposal
- 4-round trips required, use with caution

write process

- write is appended to commit log first, to survive crash
- then written to a memory resisdent data structure called "memtable"
- flushed from "memtable" to disk called "SSTable"
  - immutable, append only, all writes are sequential

bloom filter

- a special kind of key hash
- false negative possible, if not in filter, it does not exist
