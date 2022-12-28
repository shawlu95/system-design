### DB Services

- fully managed
- MySQL (Amazon Aurora), Maria, PostgreSQL
- Microsoft, Oracle
- **AWS DynamoDB** is serverless
- **AWS Redshift** big data storage, based on PostgreSQL
- **AWS ElastiCache** in-memory data score (cache)
- **AWS Database Migration Services**: move DB to AWS; or from one type of engine to another
- **AWS Neptunes** millisec latency on billions of edges

#### Example of migrating on-site databse

- on-premise onsite Oracle database is slow and outgrown capacity, license expensive
- launch AWS Aurora (built on open-sourced MySQL, PostgreSQL), no license fee
- some fields may not be compatible with AWS Aurora. **AWS Database Migration Services**, define workflow, including source db, target db, operations on data
- launch a webserver to receive requests from the outside world, and retrieve data from Aurora
- setup ElastiCache to cache popular requests
  - invalidate cache if underlying data change (update / delete)
  - when first requested, write data into cache, with time-to-live (TTL)
- security groups are created in VPC
  - place RDS inside security group to allow connection from my IP
  - outbound is allowed to inbound subjects (requests) by default

### Amazon RDS

- managed relational database
- PostgreSQL, MySQL, MariaDB, Oracle, Microsoft SQL, Amazon Aurora
- PaaS, handle routing database tasks such as provisioning, patching, backup, recovery, failure detection, repair
- backup is a snapshot, can be user-initiated or auto-backed up
  - user initiated backup is not deleted when db terminates
  - auto-backup is terminated when db terminate
- Multi AZ is recommended for production app (so is the application app)
- a standby instance in another AZ can take over the domain if DB is down (switched by route 53)
- read-replicas not supported for Microsoft or Oracle
- how to use one endpoint for replicas
  - use Aurora replica (only one endpoint)
  - software uses different endpoints
  - use Route53 to create "internal domain names"
  - custom load balancer on EC2 (advanced)
- Aurora is AWS RDS flagship
  - 1/10 of the commercial database cost
  - 5 times faster than MySQL
  - clusters share single read endpoint
  - up to 15 read replicas
  - Aurora Serverless is suitable for infrequent, intermittent, unperdictable tasks. Pay by seconds

### Amazon DynamoDB

- NoSQL
  - tables: e.g. Persons
  - attributes: columns
  - items: e.g. rows in a table
  - parittion key
  - sort key
- provisioned capacity:
  - specify read & writes per second
  - for predictable traffic, consistent or gradual ramping
- on-demand capacity
  - auto scale up & down based on demands
  - no capacity planning
  - per per request

### Amazon DocumentDB

- MongoDB is most popular. Migrate MongoDB to Dynamo is hard!
- DocumentDB is compatible with MongoDB
- 1 primary, 15 replicas
- replicate 6 copies across 3 AZ
- continuous backup to S3

### Amazon Keyspaces

- compatible with Cassandra, CQL
- provisioned and on-demand modes available

### Amazon Neptune

- store and navigate relationship
- nodes, edges, properties on nodes, edges
- language support: **Gremlin**, **SPARQL**

### Amazon Redshift

- based on PostgreSQL
- big data wharehouse, complex query, petabyte scale

### Amazon ElastiCache

- fully managed, in-memory store
- low latency access for popular content
- **Redis** or **Memcached** engine

### Amazon Quantum Ledger Database (QLDB)

- append only, ledger, immutable, transparent journal
- built-in cryptographic verification
- useful for sensitive data, e.g. financial transaction
