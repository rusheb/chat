import asyncio
import sys

from chat.client import start_chat_client

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print("USAGE: client.py <name>")

    client_name = sys.argv[1]
    asyncio.run(start_chat_client(client_name))
