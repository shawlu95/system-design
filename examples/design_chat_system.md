# Design Chat System

### 1. Understand the Problem and Scope

- one-on-one or group chat
  - 1:1 examples include Messenger, WeChat, WhatsApp
  - group chat includes Discord, Slack
- mobile/desktop
- scale: 50 million DAU
- group chat limit: 100 members
- features: online indicator (green dot); chat attachment
- message limit: 100k chars
- end-2-end encryption
- how long to store: forever

### 2. Propose High-level Design

Each client connects to chat service, not directly to each other. Chat service should support:

- retrieve messages from other clients
- find recipient for each message and relay messages
- hold message on server until recipient is online

Network protocol:

- HTTP: ok for sender, not good for receiver; FaceBook use this for initial message sending
  - login, logout, registration can still be handled by HTTP
- polling: client asks server for messages periodically
- long polling: ask server and keep connection alive until a message becomes available or time-out (very expensive). Also, sender and recipient may not connect to same servers (stateless)
- websocket: most common, client open a socket and keep connection alive. Good for sending and receiving

Types of Services

1. stateless services: handle login, signup, user profile
2. stateful services: support chat websocket
3. 3p integration: notification, email, message etc.

Data Stores

- SQL stores user profiles, use sharding and replication for scaling and fault-tolerant
- NoSQL key-value store to save chat history
  - Facebook uses HBase, Discord uses Cassandra
  - recent chat are most often accessed
  - need to support random read (from search, mention etc)

Data Model

- messages are identified by ID, not by timestamp because messages could be created at the same time
- ID increases with time, so sorting ID is same as sorting by time
- could use [UUID generator](./design_unique_id_generator.md) but it's overkill
- ID only needs to be locally unique within a group chat. Groups are identified by group ID

### 3. Design Deep Dive

Service discovery

- recommend best chat server for a client based on geolocation, server capacity
- Apache Zookeeper is popular option

1:1 chat message flow

- sender submits request to chat server 1, which acquires a ID and sends request to message sync queue
  - each user has a sync queue, containing messages from different senders
  - think of sync queue as mail inbox
- the sync queue persists data in KV store and:
  - forward message to recipient's server if conencted
  - or forward to notification server if offline

Sync from KV store:

- each device knows it's max message ID
- when a device queries KV store, new messages are downloaded if both conditions are true:
  1. recipient ID is the current device user
  2. the message ID is bigger than the device's max message ID

Presence server

- managing user online/offline status
- naive implementation
  - when user logs in and connects to socket, save "online" status in KV store and current timestamp as `last_active_at`
  - when user logs out or disconencts from socket, save "offline" status in KV store
  - user can quickly connects/disconnects due to internet stability, we don't want to update KV store too often
- better implementaiton: heart beat
  - user emits heart beat every 5s
  - if user misses 3 heart beat, mark it as offline
- fan out: how to get friends online/offline status change
  - a channel is maintained for every friend-pair
  - if a user has 500 friends, he subcribes to 500 channels as soon as he connects
  - if a user connects/disconencts, it publishes event to all of his friends' channel
  - very expensive for large groups (require manually refresh)

### 4. Wrap-up

Four components:

1. chat server for real-time chat
2. presence server for status tracking
3. push servers
4. key-value stores
