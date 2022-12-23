### Relational Database

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
