# DESIGN A RATE LIMITER

Objective:

- prevent DoS attack
- reduce cost if calling third-party API

### 1. Understand the Problem and Scope

- client-side rate limiter or server-side
- based on IP, user ID or other property
- what's the throttle rules
- scale of system (start-up or tech giant)
- distirbuted rate limiting

Implicit requirement:

- light weight, should not increase latency
- exception handling: show users they are throttled (status code 429)
- fault tolerance

### 2. Propose High-level Design

- client side throttle is unreliable
- common to have a rate limiter middleware between client and API server
  - API gateway is a fully managed service that supports rate limiting

Five algorithms for rate limiting:

1. token bucket algo

- a bucket has fixed _capacity_ and is getting _refilled_ token at constnat rate
- every time a request is served, a token is consumed
- pros: easy, memory efficient, allow bust of traffic

2. leaking bucket algo

- maintain a FIFO queue of request with fixed _capacity_
- process requests at a fixed rate (measured in seconds)
- pros: memory efficient, stable outflow rate
- cons: burst traffic will fill with old requests

3. fixed window counter

- windows don't overlap; quota resets at the start of each window
- cons: spike at end of previous window and next window can cause overshoot of rate

4. sliding window log

- keep timestamps of requests in a sorted set (Redis)
- when a request arrives, old timestamp (older than window start) are dropped
- pros: very accurate rate limiting in any window starting at any time
- cons: very memory intensive. Rejected requests are counted in quota too

5. sliding window counter

- an estimation algo
- number of requests in current window = requests in current + overlapping time (%) with previous window \* request in previous window
- pros: smooths traffic spikes, memory efficient
- cons: not as strict and accurate

### 3. Design Deep Dive

- store rules in config files and save on disk. Worker nodes load rules and cache them
- return 429 if exceeding rate limit with response header:
  - `X-Ratelimit-Remaining`
  - `X-Ratelimit-Limit`
  - `X-Ratelimit-Retry-After`
- race condition: use Lua script or sorted set data structure (Redis)
- sync issue: use centralized data score (Redis)
- multi-data center to minimize latency
- monitoring with metrics

### 4. Wrap-up

- hard vs soft rate limiting
- different levels of rate limiting
  1. physical layer
  2. data link layer
  3. network layer
  4. transport layer
  5. session layer
  6. presentation layer
  7. application layer (most discussed)
- client should handle 429 exception and retry
- design client to avoid overwhelming server
