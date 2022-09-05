# Design Notification System

### 1. Understand the Problem and Scope

- push notification to phones, SMS message, email
- soft real-time
- support iOS, android, desktop
- what triggers: client apps or server
- can opt out notification
- volumes: 10 million push daily, 1 million SMS, 5 million email

### 2. Propose High-level Design

iOS Push

- providers build and send requests to **Appple Push Notification Service (APNS)**
- device token identifies the iOS device
- payload is a JSON object

Android Push

- Analog of APNS is **Firebase Cloud MEssaging (FCM)**

SMS message

- Twillio
- Nextmo

Email

- Sendgrid
- Mailchimp
- can monitor delivery rate and analytics (click rate)

Gathering contact info

- a user may have multiple devices
- a user table can map to multiple rows in the device table

Components of system

- server 1~N: trigger notification
  - micro-service that detect certain conditions (items in cart, billing)
  - cron-job to trigger regular notification (weekly news-letter)
- notification system:
  - provide API for server 1~N, build notification payload to 3rd party providers
  - validate emails, phone numbers
  - query DB and cache for info to build notification payload
  - stateless, support horizontal scaling
  - use message queues (event bus) ot decouple components (iOS queue, Android queue, SMS queue, email queue)
  - workers node pull from message queues, build payload, and send to 3-party providers and wait for response
- 3-party services: send out mobile push, SMS or email

### 3. Design Deep Dive

Reliability: Preventing data loss

- retry mechanism
- messages may be out-of-order
- at-least-once delivery
- exactly-once is impossible

Optimization

- reuse template string, json
- save notification setting. If user opted out, do not even try (reduce throughput)
- notification server perform **rate limiting** per user (don't trigger users)
- notification server authenticate incoming requests
- retry failed delivery a few times. Add failed delivery to the front of queue
- monitored queue size throughput the day (handling peak traffic)

### 4. Wrap-up

- reliability: retry
- security: client must provide app key / app secret to send notification
- tracking and monitoring
- respect user setting
- rate limiting
