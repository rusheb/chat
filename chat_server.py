import asyncio

from chat.server import ChatServer

if __name__ == '__main__':
    try:
        server = ChatServer()
        asyncio.run(server.start_chat_server())
    except KeyboardInterrupt:
        print("Exiting.")
