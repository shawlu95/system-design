# News Feed

Common examples: Facebook news feed, Instagram, Twitter timeline

### 1. Understand the Problem and Scope

- mobile or desktop app
- feature: user can publish post and see friends' post sorted reverse chronologically
- avg number of freinds: 5000
- daily traffic: 10 million DAU
- media: text, photo, videos

### 2. Propose High-level Design

Talk about two parts separately: publishing feed, aggregating friends' feed

#### Posting Feed

- POST `api/v1/user/feed`
- send a post request to api with (1) content text and (2) auth token
- load balancer send requests to web servers
  - post service: store post in database, cache
  - fan out service: push to friends' news feed
  - notification service

#### Retrieve Feed

- GET `api/v1/user/feed`
- include auth token
- load balancer forwards request to web servers which query news feed services
- news feed cache: store news feed IDs to render the feed

### 3. Design Deep Dive

#### Write Feed

- web servers authenticate requests and perform rate limiting
- post services query a cache and DB
- fan out servie
  - get friend IDs from Graph DB
  - get friends data from user cache and user DB
  - push new message to a queue as `<post_id, user_id>` mapping
  - media are stored in CDN

fan out on write (push): news feed is pre-computed when a post is written

- pros: news feed is generated real-time and pushed immediately to friends, fast to retrive
- cons: hotkey problem for user with many friends; waste resource for users who don't log in

fan out on read: generated on-demand when a read request is seen

- pros: no hotkey, no inactive user problem
- cons: slow to fetch

solution:

- fan-out on read for normal users
- fan-out on write for celebrity users

#### Read Feed

- user submits a GET requests, and looks up a list of `post_id` from news feed service
- from post_id it retrieves post content, which includes poster's id and media link
  - retrieve poster's info from cache/db
  - retrieves post content from cache, db or CDN

### 4. Wrap-up

What to cache:

- news feed IDs
- content (hot cache)
- social graph
- action: like, reply
- counter: like counter, reply count
