# Designing YouTube

### 1. Understand the Problem and Scope

- core function: upload video and watch video
- support multiple platform: iOS, Android, web, TV
- 5 million DAU
- 30 minutes average daily time
- need to support international
- need to support different resolution and format
- **can use cloud service e.g. AWS**

Estimation

- 5e6 DAU

Upload:

- 10% of users upload 1 video per day: 5e5 videos
- each video is 300MB on average: 5e5 * 0.3 * 1e9 = 1.5 * 1e14 = 150e12 = 150 TB

Read:

- 5 million DAU, watching 5 videos per day, each 0.3 GB
- CDN is expensive, with $0.02 / GB:
  - 5e6 * 5 * 0.3 * 0.02 = 150,000 USD / day

### 2. Propose High-level Design

Three major components

- clients: can by any device
- CDN: streams videos to client
- API servers:
  - has its load balancers
  - handles authentication
  - metadata CRUD
  - user account management
  - has metadata cache and DB

Uploading:

- raw video is uploaded to "original storage"
- transcoding servers pull video from original storage

  - transform into different **format**, **bitrate**
  - transcoded videos are put into CDN

- after transcoding completes, messages are queued in event bus, and dequeued and notify client of success

  - update metadata DB and cache when completed

Streaming:

- Popular streaming protocol:
  - MPEG-DASH: Moving Picture Expert Group, Dynamic Adaptive Streaming over HTTP
  - Apple HLS: HTTP Live Streaming
  - Microsoft Smooth Streaming
  - Adobe HTTP Dynamic Streaming (HDS)

### 3. Design Deep Dive

- the original video must be encoded into compatible bitrates and formats
  - higher bitrate means higher video quality
  - different devices and browsers only support certain types of formats
  - adjust video quality based on network bandwidth for better viewing experience

DAG to encode video

- preprocessor: split videos into **group of pictures** (GOP), store in memory in case retry is needed
- scheduler: split the workflow into stages and put in task queue of resource manager
- resource manager: can access three queues:
  - task queues, a priority queue; pick the highest priority ans assign to available workers
  - worker queue
  - task scheduler: pick optimal worker for optimal task
- task workers: execute the task designed by schedulers
- temp storage: save metadata in RAM for fast access by different workers
- encoded videos are stored in BLOB

Optimization

- geolocation: assign to nearest CDN centers for hosting encoded video
- parallel tasks: assign GOP into different workers, by using an event bus to be polled by workers
- security: using pre-signed URL to allow specific users to upload specific video into a path in specific time (e.g. 2 hr)

Copy right

- digital right management (DRM) systems: Apple FairPlay, Google WIdevine, Microsoft PlayReady
- AES encryption: encrypt a video and config an authorization policy; decrypted when streamed
- watermark on video

Cost-saving

- put popular videos on CDN, others on video servers, or S3 Glacier
- some popular videos are only popular in specific countries
- partnering with Internet Service Providers (ISP) for better pricing

Erorr handling:

- recoverable errors: on server side, can just retry, fallback, replace failed nodes etc
- irrecoverable errors: bad file format, incomplete upload, authentication, return error to clinet and abandone all DAG tasks

Examples of recoverable errors:

- upload errors: retry
- split video errors: client cannot split, then split on servers
- transcoding error: retry
- preprocessor error: regenerate DAG
- scheduler error: reschedule tasks
- task workers down: assign tasks to other workers, add workers nodes
- API server down: spin up new servers, reroute failed requests
- meta cache down: access other cache nodes, add new cache nodes to replace failed ones
- meta DB down:
  - master down: promote slave to master
  - slave down: use another slave, add more slaves

### 4. Wrap-up

- easy to scale API servers horizontally (stateless)
- scale data: replica, sharding
- live streaming: higher latency requirement, lower parallelism requirement
- videos removal: copyright, porn, illegal acts
