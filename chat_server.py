import asyncio

from chat.server import start_chat_server

if __name__ == '__main__':
    try:
        asyncio.run(start_chat_server())
    except KeyboardInterrupt:
        print("Exiting.")
