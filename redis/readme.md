## Redis

The notes are taken from "Caching at Scale with Refis" [PDF](https://secret-garden-library.s3.amazonaws.com/caching-at-scale-with-redis-updated-2021-12-04.pdf) and the
Why is Redis so fast

1. in-memory
2. simple data structure
3. limited feature & overhead

### Benefits

- reduce latency
- scale better, more concurrent users with the same computing resources
- improve throughput with higher resource optimization
- high availability (in case server goes down)

### Concurrency

Redis is synchronous and single-threaded in nature. It processes one command at a time, in the order it is received.

How to avoid inconsistent write (e.g. two voters upvote an item at the same time)

1. use `INC`, one HTTP request to Redis
2. use `LOCK`
3. use a Redis transaction with `WATCH`

---

## Types of Cache

- application cache: in server
- HTTP network cache: static web content along the route between browser and server
- web browser cache: images and other static content
- service cache: similar to application cache but operates at service level
- API cache stores service call
- database cache stores query results
- CPU cache
- memory cache (RAM)
- disk cache: repeated disk operation

## When to apply cache

- requested data is slow
- cost **considerably** less resource than reading from the original source
- data are unchanged
- server is stateless (no side effect)
- frequent access
- significant portion of frequent requests can be cached (normal distribution is ideal)

### When to avoid cache

- when cache causes **the application to not execute desired side effects** (e.g. modify some states)
- inconsistent data
- poor cache performance

### Static vs Dynamic

- static (read-only cache) store can't update cache, update goes to data store, then invalidate cache
- dynamic (read/write cache) cache is updated, then update data store

### How Cache Works

1. request comes in, check cache first
2. if in cache, return the cached resposne
3. if not in cache, process the request
4. put the resposne in cache
5. return response

### Key Design

- Use `:` to separate entity: `item:18`, `users:45`
- Use `#` before unique ID: `item#18`, `users#45:posts#16`
- use `#` before url: `pagecache#/about`, `pagecache#/contact`

---

### Caching Strategies

#### In-line Cache

- the cache sits in front of the data store
- direct connection between cache and data store
- consistency is responsibility of the cache

#### Cache-aside Pattern (Redis)

- no connection between cache and data store
- application checks the cache, and if not exists, then the data store
- consistency is responsibility of the application

---

### Consistency

Causess of inconsistency:

- whe nunderlying data change, cache is not updated
- there's delay in cahced results (write-behind async)
- inconsistency across cached nodes (read replicas)

Common strategy is to 'invalidate' cache (removing it).

#### Write-through cache

- the application updates the cache; the cache updates the data store
- cache is responsible for maintaining its consistency
- con: actual write is slow because both the cache and underlying data need update

### Write-behind/write-back cache

- value is updated directly in cache, and immediately return
- cache updates data store async.
- pro: more responsive API
- con: short period of inconsistency during the async update to the data store

---

## Eviction

The all-in policy is 'no-eviction' policy. Cache is never removed and cache gets filled over time.

When cache is full, **cache thrashing** can happen when item gets wrongly evicted and refetched repeatedly, reducing cache performance. So resolve, try a few different evict strategies:

- LRU eviction (approximate sampling algo): remove the piece of data that hasn't been accessed for the longest period of time
- LFU eviction (approximate sampling algo): remove data that have been accessed the fewest number of times
- oldest-stored eviction: aka LIFO cache, not so common
- random eviction: fast, but creates more cache misses later, not common
- TTL eviction: data are given a period of time. Redis does this at key-level, not at policy level. Commonly used for **session**
- cache persistence: larger than the underlying data store, never need to evict cache. If full, cache write will fail (evict all new data). This is Redis default.

---

## Advanced Concept

Redis can be configured as volatile cache, persistence cache

- volatile cache: erased when power is out, stored in RAM
- cache persistence: persist during power outage and system reboots, stored in hard disk, SSD
- hybrid is possible, backup RAM in disk, recover backup (**rehydration**) when reboot

### Redis persistence options

#### Append-only files

- a real-time log of updates to the cache.
- When replayed, cache state is reconstructed.
- Append can happen sync (guarantee no data loss) or async or every second, depending on latency requirement
- log can be 'cleaned' by removing old entries that no longer affect the end state

#### point-in-time backup (RDB)

- highly efficient, smallest possible backup file

### Mixed RAM/SSD Caching with Redis Enterprise

- open source can only store key in RAM
- enterprise can store in RAM or SSD Flash memory (**Redis on Flash** or RoF)
- LRU eviction policy: more active records in RAM, less active in SSD
- significantly larger cache
- AOF/RDB still required for persistence

### One-liner

- in-cache function: allow execute arbitrary function (e.g. python) within the cache database
- async communication channel: connect different microservices using **Redis List object** (FIFO)
- network-level cache: HTTP requests caching, managed by HTTP headers
- microservice cache: between service, cache interim results, reduce call load on backend services
- **RediSearch**: in Redis Enterprise, full-text search engine

---

## Data Structure

### List

- `List` data types with `LPUSH`, `RPOP`: FIFO queue for scheduling and messaging
- `Set` data type: `SADD`, `SREM`, `SISMEMBER`
- `Hashes` is a key-value property map in a key: `HSET`, `HMGET`, `HGETALL`
- `RedisJSON` uses a Redis module, store any type of data: `JSON.SET`, `JSON.GET`
- `SortedSet`
- `Streams`
- `Strings`

---

## Caching at Scale

- storage limit: amount of space available to cache data
- resource limit: capability to perform storing and retrieving cached data (e.g CPU)
- vertical scaling gets you higher resource limit

### Horitontal scaling

- read replicas:
  - copy of the cache is on **auxiliary servers** in different availability zones, regions, even cloud providers
  - write is processed at master node
  - if master fails, one of the replica takes over the master role
  - higher resource limit, same storage limit
  - does not improve write performance
- sharding/partitioning:
  - improve both storage and resource limit
  - each shard/partition holds a portion of the cache
  - a **shard selector** will route key to a deterministic shard
- active-active
  - handle higher write and read throughput
  - not increase storage limit, every node has complete copy of data
  - any node can accept write, and publish to every other nodes
  - increase availability
  - write conflict: when two nodes accept the write to same key, with different value
  - data lag: fresh write may not have been propagated to all nodes

---

## Performance

- **cache overhead** is the cost of checking cache and adding a record to cache (cache check + cache write)
- a **cache aside** setup would incur cache check on read request, and cache write in case of **cache miss**
- heavier resource call, better cache performance
- more cache hit, better cache performance
- formula for a cache to be effective (can calculate the required cache hit rate)

```
(hit_rate * latency_cache_hit) + (miss_rate * latency_cache_miss) > request_time_no_cache
```

### Reference

- official site: https://redis.com/
- rbook notebook: https://rbook.cloud/
- run notebook locally: `npx rbook` then `http://localhost:3050`
