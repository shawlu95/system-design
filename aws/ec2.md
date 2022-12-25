## EC2

- on-demand instances, pay by the second
- spot-instances: highest bidder gets the instances; could be terminated when spot price goes higher
- reserved: one~three long term contract, always available
- scheduled-instance: available on recurring schedule
- dedicated instances: pay by hour, single-tenant hardware
- dedicated hosts: dedicated to running dedicated instances

### Instance Type

- general purpose: SQP, cluster compute
- compute optimized: engineering, ad serving, gaming
- memory optimized: high performance database
- GPU: 3D, ML, videos
- storage optimize: NoSQL, elastic MR

* bare metal: no virtualized environment

- T2/T3 Burstable: have baseline performance, but can burst much higher depending on CPU credits
- Graviton: Arm Neoverse cores

### EC2 Fleet

- create a group of instances
- unlimited instances types per fleet
- on-demand and spot purchasing options
- available in API/SDK, AWS CLI (not available in console)
- span multiple AZ, but in one Region
- different fleet in different regions

### Storage

- Elastic Block Store
  - most common
  - replicated in AZ
  - if attached when launching instance, deleted when instance is terminated
  - if attahced after launching, will not be deleted when EC2 terminate
  - storage options:
    - general purpose gp2
    - provisioned IOPS SSD: for database
    - cold HHD: lowest cost
    - throughput optimized: for frequently accessed workloads, low cost per GB
    - EBS snapshot: backed up in S3, incremental backup, can be coplied across region/account
    - EBS encryption
- Instance store
  - physicaly attached to host server
  - lost when drive fail or instance terminate
  - cannot detach and attach to another instance

### Connect

- SSH Shell, requires PEM file and stores remotely
- EC2 Instance Connect: a browser shell, no PEM required
