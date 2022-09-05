# Design an Anto-complete System

Also known as

- type-ahead
- search-as-you-type
- incremental search

### 1. Understand the Problem and Scope

- only match the beginning of query (not middle)
- return 5 results (most frequently searched)
- only English
- no spell-check
- no capitalization or special letters
- 10 million DAU
- fast resposne time (100ms)

Estimation

- 10 x 10^6 DAU \* 10 searches per day = 10 ^ 8 query per day
- 4 words \* 5 chars / word = 20 chars / query (1 char per byte)
- as user types one query string (5 words, 20 chars), a total of 20 queries are issued
- QPS 10 ^ 8 \* 20 / 86400 = 24,000
- peak traffic 48,000 QPS
- storage: 10 ^ 8 query per day \* (20 bytes / query) = 2 ^ 9 byte = 2 GB
  - if 20% requests are new, only adds 0.4 GB

### 2. Propose High-level Design

- Data gathering service: count query frequency per day
- query service:

```sql
select * from frequency
where query like "prefix%"
order by frequency desc
limit 5
```

### 3. Design Deep Dive

Prefix tree (trie, pronounced "try")

- root node is an empty string
- each level has 26 branches (26 letters, case insensitive)
- each leaf not means a complete query, traversed from root
- each non-leaf node is a partial query

Time complexity

- find prefix: O(p) where p is length of prefix
- find all children of prefix: O(c) where c is number of children
- sort all children leaf nodes by frequency O(clogc)

Optimize the data structure

- set a maximum depth, e.g. store nore more than 10 level
- store top N leaf nodes in each of the non-leaf nodes (trade storage for speed)

#### Data Gathering

1. analytic logs are retrieved
2. data aggregators run on regular interval, count frequency of queries
3. workers receive aggregated data and build tries
4. cache weekly snapshot of built trie
5. store trie in key-value store for fast lookup

- key: prefix
- value: top N leaf nodes

#### Query Service

1. search query is sent to load balancer
2. load balancer forwards request to API servers
3. API retrieves leaf node from cache, or the DB

Optimize:

- AJAX request: does not refresh whole web page
- browser cache (Google search engine uses)
- data sampling, only count 1 out of N query (if throughput is not manageable)

#### Maintaining Trie

- create: by workers using aggregated data
- update:
  1. replace the entire trie weekly, because the data are usually stable
  2. dynamic update nodes: if a leaf node frequency is updated, all intermediate nodes along the path needs to update

Storage Scaling

- small data, store a-i in one, j-z in second server
- largre data, partition using first two letters of prefix
  - do not assign alphabetically
  - instead, based on total search frequency (rare combinations can be grouped into single server)

### 4. Wrap-up

- may store unicode in trie nodes
- for multi-country, store local language in DNS server based on geolocation
- support trending search (twitter): beyond the scope, read in free time
