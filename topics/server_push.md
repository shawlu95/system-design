## HTTP Polling

- client requests data repeatedly
- if no new update, empty response is returned
- create HTTP overhead

## Long Polling

- client does not expect server to immediately return
- server holds the request until the response is available
- aka "hanging get"
- has a time out

## WebSocket

- persistent connection, full-duplex (either party can send at any time)
- lower overhead, real-time data transfer (live-chat)

## Server-Sent Event

- client establishes persistent connection to server
- server sends data to client
- client cannot send to server
- use case: location tracking
