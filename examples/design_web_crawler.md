## Background

Web crawler (aka web spider, robot) is used to discover new or updated content on web

- used for search engine indexing
- web archiving
- web mining (e.g. financial firms)
- web monitoring (trademark, copyright)

### 1. Understand the Problem and Scope

Web crawlers are extremely complex, but the iterations are:

1. for a set or URLs, download all web pages
2. extract URLs found in those pages
3. repeat

Questions to ask interviewer:

1. purpose of web crawler
2. number of pages to download per month
3. what content type (HTML only)
4. only new or updated pages
5. how long to store (5 years)
6. duplicate policy (ignore duplicate)

implicit requirement

1. scalable
2. robust: handle unresponsive servers, crashes
3. courtesy
4. extensibility: for new content type

Estimation:

- 1 billion a month => 1e9 / 30 / 24 / 3600 = 400 qps
- peak traffic 800 qps
- avg html 500kb
- 1 b pages * 0.5mb = 1e9 * 0.5e6 = 0.5e15 = 500e12 or 500 TB a month
- store 5 years needs: 5 * 12 * 0.5 PB = 30 PB

### 2. Propose High-level Design

- seed urls: starting set of urls (by geographic, by topics, manually picked)
- url frontier: a FIFO queue storing urls to be downloaded
- html downloader
- dns resolver: translate url to IP address
- content parser: parse and validate html
- content seen: dedup pages
- content storage: most store in disk, popular content in memory
- url extractors: extract links from html and push into filters
- url filters: remove 404, error links
- url seen: dedup url (use bloom filter or hash table)
  - if not seen, save into frontier
- url storage: save already visited url

### 3. Design Deep Dive

#### Courtesy

- BFS is more popular than DFS because a path can be very deep and obscure
  - using a FIFO queue
  - prioritize by page ranks, traffic, update recency
- DFS is not polite because it keeps asking for URL from the same host
- first assign priority
  - assign url to different queue
  - a queue selector randomly dequeue url from queues, with higher probability on high-priority queue
- next, assign worker
  - keeping a table, maps url to queue (same domain's sub-url should be on same queue)
  - a queue selector dequeue url and assign to worker threads
- check for `robot.txt` (Robots Exclusion Protocol) and follow crawler policy

#### Efficiency

- URL frontier store most url on disk, and maintain a buffer for enqueue/dequeue
- cache DNS resolver (often takes time due to synchronous nature)

#### Freshness

- recrawl based on update history
- recrawl important pages first

#### Robustness

- consistent hashing: distirbute loads among downlaoders
- handle exception
- validate data
- save crawl state
- avoid duplicate using hash/checksum
- avoid spider traps by setting max URL depth

### 4. Wrap-up

- server-sode rendering: not addressed
- filter unwanted: spam, ads
- replicate and sharding (fault tolerant)
- analytics, metrics, monitoring
