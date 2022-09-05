# System Design Interviews

## What to Evaluate

From the interviewers point-of-view, the goal is to assess a person's:

1. technical design skills
2. ability to collaborate
3. work under pressure
4. resolve ambiguity

Red flags in interview:

- over-engineering: delight in design purity, ignore trade-off
- narow mindedness, stubbornness
- giving out answer without thinking & talking through the problem

---

## 4-Step Framework

### 1. Understand the Problem and Scope (3-10 mins)

Ask the right questions:

- what specific features
- how many users, traffic
- scaling plan
- tech stack (mobile/web): language, cache service

### 2. Propose High-level Design (10-15 mins)

Make a initial design and ask for feedback

- draw box diagrams
- back-of-the-envelope estimation on storage
- look for edge cases

### 3. Design Deep Dive (10-25 mins)

Depending on job level, the interview may focus on high-level design, or performance characteristics (bottleneck)

- do not try to explain technical details (e.g. how an algorithm works)
- careful with time management. Don't get carried away by trivia

### 4. Wrap-up (3-5 mins)

Answer follow-up questions, including:

- identify system bottleneck and potential improvement
- recap of design (especially if more than one solutions are suggested)
- failure cases
- operation and monitoring (metrics, error logs)
- scale to next level

---

## Example Problems

- Design [Rate Limiter](./examples/design_rate_limiter.md)
- Design [Consistent Hashing](./examples/design_consistent_hashing.md)
- Design [Key-Value Store](./examples/design_key_value_store.md)
- Design [Unique ID Generator](./examples/design_unique_id_generator.md)
- Design [URL Shortener](./examples/design_url_shortener.md)
- Design [Web Crawler](./examples/design_web_crawler.md)
- Design [News Feed](./examples/design_news_feed.md)
- Design [Chat Systen](./examples/design_chat_system.md)
- Design [Auto-complete](./examples/design_auto_complete.md)
- Design [YouTube](./examples/design_youtube.md)
