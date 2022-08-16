### 1. Understand the Problem and Scope

- 100 million urls per day
  - 100,000,000 / 24 / 60 / 60 = 1160 requests / second
- as short as possible
- url cannot be deleted or updated
- service run for 10 years

Estimation

- 1160 qps
- read:write ratio 10:1, read volume 11,600 qps
- 10 years requires 10 _ 365 _ 100 million = 365 billion records
- each record 100 bytes, 365b \* 100 byte = 36.5 TB

### 2. Propose High-level Design

Design two API endpoints

- `POST`: send long url, return short url
- `GET`: send short url, get long URL and 301 status code for redirect
  - 301 for permanent redirect (browser cache, no more hit on server)
  - 302 for temp redirect (better track click rate)

Clarify hash requirement:

- long URL must be **hashed** to short URL
- short URL can be **mapped** to long URL

### 3. Design Deep Dive

#### Using Hash Function

- use 0-9, a-z, A-Z (62 characters) for hash
- need 7 characters to host 62^7 = 3.5 trillion records
- use existing algo: `CRC32`, `MD5`, `SHA-1`

Prevent hash collision:

- query DB to check if hash exists. If so, append hash to long URL and hash again (loop)
- to improve performance, use bloom filter to check if hash exists in DB

#### Using base62

- map URL sequence number to a base62 string
- pros: unique, no collision
- cons: difficult to scale, require unique ID generator, length increases with number

#### Handling Write

1. receives long url
2. check if long url is in DB, if so, return short URL
3. if not in DB, get the next seq ID and convert to base 62, save in DB: `(id, short url, long url)`

#### Handling Read

1. load balancer forward read request to cache server
2. cache return long url if found
3. if not in cache, fetch from DB, return request if found, and store in cache
4. if not found in DB, return 404

### 4. Wrap-up

- rate limiter
- web server is stateless
