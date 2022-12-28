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

Common strategy is to 'invalidate' cache (removing it

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

### Basic Command

-

### Reference

- official site: https://redis.com/
- rbook notebook: https://rbook.cloud/
- run notebook locally: `npx rbook` then `http://localhost:3050`
