# Design Google Drive

### 1. Understand the Problem and Scope

- core function: upload and download files
- platform: mobile, web
- support any file format
- need to be encrypted
- limit 10GB per file
- 10 million DAU

Features:

- upload, download file
- sync files across devices
- see version history
- share files with friends
- notification on file edit, deletion, sharing

Not include:

- collaborative editing

Non-functional requirement

- reliability: no data loss
- fast sync speed
- band-width: do not use up mobile data plan
- scale to high volume of traffic

Estimation

- 50 million users
- 10 million DAU
- 10 GB free space per user
- user upload 2 files per day, each 500kb
- total storage space: 50e6 * 10e9 = 5e17 = 500 PB
- QPS for upload: 10e6 * 2 / 86400 = 231 qps
  - peak QPS 462

### 2. Propose High-level Design

- a load balancers route traffic to API servers
- server query metadata database or cache
- explain how to decouple web servers from metadata and file storage
- Block servers divide big files into chunks. e.g. Dropbox has block size of 4MB
- blocks are stored in S3 or equivalent
- inactive files are stored in cold storage for cheaper price
- notification service

Conflict resolution

- if two users try to modify the same file, the first one is accepted
- the conflict is returned to second user to override or merge

### 3. Design Deep Dive

Block server details

- delta sync: only modified blocks are synced and transferred across network
- compression: reduce network transfer throughput (e.g. gzip, bzip2 for text file)
- encrypt each block before sending to cloud storage

Strong consistency

- different devices must not see different versions of file
- data in all cache replicas must be consistent
- invalidate cache on database write
- MySQL is good candidate for maintaining ACID property on metadata
- a notification service is required to update client to rebuild files after update
  - use long polling, not web socket
  - when change is detected, client will close the long poll
  - then must reconnect to metadata server to downlaod latest changes
  - open a new long-poll connection

Upload

1. client send requests to API server which creates a record with upload status = pending
2. notify user that new file is being added
3. client uploads file to block servers
4. block servers divides file into block, compress, encrypt each block and uplaod to cloud storage
5. cloud storage triggers callback which update status to 'uploaded'
6. notify client that upload is successful

Download

1. when file is updated, notify all online client immediately of the change

- if client if offline, save data to cache and inform client when online

2. client requests metadata by API
3. API servers fetch changes from DB or updated cache
4. chuncks are downloaded from cloud to block servers
5. client download the new blocks to reconstruct the files

Cost-saving

- dedup data blocks by hash
- limit versions to save
- only keep valuable version, don't save every edit on a word documents
- move inactive files in cold storage

Failure handling:

- load balancer failure: monitor using heartbeat
- block server fail: other servers pick up unfinished tasks
- cloud storage: use multiple region
- API server fail: route traffic to other servers (stateless)
- meta cache fail: replicate cache, bring up new cache to replace failed ones
- notification service fail: reconnect all long-poll clients (could be slow)
- offline backup queue fail: multiple backup queues needed. Consumers should resubscribe

### 4. Wrap-up

- strong consistency, low network bandwidth, fast sync
- could upload files firectly to cloud storage instead of block servers
- may have a "presence server" to handle online/offline status tracking
