# chat
A very basic async chat app that I built to help me learn asynchronous programming with `asyncio`.

Clients can connect to the server, see who's online, and chat in real-time. The server handles client disconnects and errors gracefully.

This project was inspired by the really awesome [import asyncio](https://www.youtube.com/watch?v=Xbl7XjFYsN4&list=PLhNSoGM2ik6SIkVGXWBwerucXjgP1rHmB) youtube series.

# Demo
https://github.com/rusheb/chat/assets/26048292/96fcd4f5-deed-457a-84c5-228b30b8fa9e

# Usage
## Install dependencies
- Get [Poetry](https://python-poetry.org)
- Install dependencies with `poetry install`

## Run Server
```bash
poetry run python chat_server.py
```

## Run Client
Start multiple clients, each in a separate terminal:
```bash
poetry run python chat_client.py <client_name>
```

# Implementation Notes / Lessons Learned
- **Simulated latency**: I introduced artificial delays using asyncio.sleep() to mimic network latency and understand its implications on the chat flow.
- **User-specific queues**: I implemented individual message queues for each user. This ensures message order and keeps messages isolated, whilst still allowing concurrency across different users.
- **Task management**: I used a set to track active asyncio tasks. This makes it easy to clean up and avoid dangling tasks.
- **Testing**: I used `pytest-asyncio` to test the project's async functions.
