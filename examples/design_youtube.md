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

- 5 \* 10 ^ 6 DAU

Upload:

- 10% of users upload 1 video per day: 5 \* 10 ^ 5 videos
- each video is 300MB on average: 5 _ 10 ^ 5 _ 0.3 _ 10 ^ 9 = 1.5 _ 10 ^ 14 = 150 \* 10 ^12 = 150 TB

Read:

- 5 million DAU, watching 5 videos per day, each 0.3 GB
- CDN is expensive, with $0.02 / GB:
  - 5 _ 10 ^ 6 _ 5 _ 0.3 _ 0.02 = 150,000 USD / day

### 2. Propose High-level Design

Three major components

- clients: can by any device
- CDN: streams videos to client
- API servers:
  - has its load baalancers
  - handles authentication
  - metadata CRUD
  - user account management
  - has metadata cache and DB

Uploading:

- raw video is uplaoded to "original storage"
- transcoding servers pull video from original storage

  - transform into different format, bitrate
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

- preprocessor: split videos into group of pictures (GOP), store in memory in case retry is needed
- scheduler: split the workflow into stages and put in task queue of resoruce manager
- resouce manager: can access three queues:
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

### 4. Wrap-up

- easy to scale API servers horizontally (stateless)
- scale data: replica, sharding
- live streaming: higher latency requirement, lower parallelism requirement
- videos removal: copyright, porn, illegal acts
