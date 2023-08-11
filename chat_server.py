import asyncio

from chat.server import ChatServer

if __name__ == '__main__':
    try:
        asyncio.run(ChatServer().run_forever())
    except KeyboardInterrupt:
        print("Exiting.")
