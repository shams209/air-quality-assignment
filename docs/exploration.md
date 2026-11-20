# Part C: Exploration Homework

## C1: Optimized Query System of a Social Media Algorithm

### Why a naive JOIN is slow
In a social media feed, if a user follows 1,000 people, a naive query at read time has to look at the `posts` table, find all posts by those 1,000 authors, sort them by time, and then return them. If the table has 100 million rows, the database has to scan the entire table (or a massive portion of it) every single time a user opens their app. This is an O(N) operation and will crash the server under heavy load.

### What an index does
An index on `(author_id, created_at)` acts like the index at the back of a textbook. Instead of scanning every page (row) to find the author, the database uses a B-Tree structure to jump directly to the specific `author_id`. This reduces the lookup time from O(N) to O(log N).

### C1 Experiment Results (from `src/feed_experiment.py`)
**Without Index:**
Query Plan: `SCAN posts`
Time taken: 3.0708 ms

**With Index:**
Query Plan: `SEARCH posts USING INDEX idx_author_time (author_id=?)`
Time taken: 1.1614 ms

### Conclusion
The index changed the query plan from a full table `SCAN` to a `SEARCH` using the index. While the `TEMP B-TREE FOR ORDER BY` still appears (because we are sorting multiple authors), the initial filtering time dropped significantly. For massive scale, this prevents the database from locking up.

---

## C2: GitHub Actions, Rules, and Code Reviews

### Which events should trigger the workflow?
The workflow should trigger on `push` to the `main` branch, and on `pull_request` targeting the `main` branch. This ensures that every new change is tested before it is merged.

### What should block a merge?
A merge should be blocked if the CI pipeline fails (e.g., if `pytest` fails, or if the linter finds syntax errors). 

### Who should review which files?
- **Core logic (`src/`):** Requires at least 1 senior developer review.
- **Database migrations (`sql/`):** Requires a DBA (Database Administrator) review.
- **CI/CD config (`.github/`):** Requires a DevOps engineer review to prevent someone from accidentally turning off the tests.

**Artifact:** I created `.github/workflows/ci.yml` to automatically run `pytest` on every push.

---

## C3: Theory of System Design

### Glossary (10 Terms)
1. **Load Balancer:** Distributes incoming traffic across multiple servers (e.g., AWS ALB routing traffic to 3 EC2 instances).
2. **Caching:** Storing data in fast memory to reduce database load (e.g., Redis storing user session tokens).
3. **SQL Database:** Relational database for structured data (e.g., PostgreSQL storing financial transactions).
4. **NoSQL Database:** Non-relational database for unstructured data (e.g., MongoDB storing JSON documents).
5. **Message Queue:** Asynchronous communication between services (e.g., RabbitMQ queuing email notifications).
6. **Replication:** Copying data to multiple servers (e.g., a Primary DB for writes and a Read Replica for heavy read queries).
7. **Sharding:** Splitting a large database horizontally (e.g., Users A-M on Server 1, Users N-Z on Server 2).
8. **CDN (Content Delivery Network):** Caching static assets geographically close to users (e.g., Cloudflare serving images).
9. **API Gateway:** A single entry point for all API requests (e.g., Kong routing `/users` and `/billing`).
10. **CAP Theorem:** You can only guarantee 2 of 3: Consistency, Availability, or Partition Tolerance.

### Trade-off Explanation: SQL vs NoSQL
If I am building a banking application, I will choose a **SQL database** to prioritize **Consistency**. I must ensure that two people cannot withdraw the same $100 at the exact same time. If the system experiences a network partition, the database will temporarily go offline rather than risk corrupting the balance.
If I am building a Twitter feed, I will choose a **NoSQL database** to prioritize **Availability**. If the system partitions, it is better for the user to see a slightly stale feed (eventual consistency) than to see an error message and not be able to use the app at all.

---

## C4: A Workflow for System Design

### Workflow Steps
1. **Clarify Requirements:** Ask about scale (e.g., 1,000 users or 1 million?), features, and constraints.
2. **Capacity Estimation:** Calculate expected read/write QPS (Queries Per Second) and storage needs.
3. **High-Level Design:** Draw the main boxes (Client, API Gateway, Load Balancer, Database).
4. **Detailed Design:** Deep dive into caching, database schema, and queues.
5. **Review & Iterate:** Walk through bottlenecks and edge cases.

### Design Document: URL Shortener (e.g., bit.ly)
- **Requirements:** User submits a long URL, gets a short URL. Clicking the short URL redirects to the long one. Fast read speed is critical.
- **Capacity:** 100M new URLs/month (Write: ~40 QPS). 10B redirects/month (Read: ~4,000 QPS).
- **API Design:** `POST /url` (create), `GET /{code}` (redirect).
- **Database:** SQL table with `id`, `long_url`, `short_code`. We need a fast index on `short_code`.
- **Detailed Design:** Since reads are 100x more frequent than writes, we put **Redis** in front of the database. When a user clicks a link, we check Redis first. If it's there, we redirect instantly. If not, we query the DB, save to Redis, and redirect.