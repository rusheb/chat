import asyncio
from asyncio import StreamReader, StreamWriter

from common import write, split_lines

users = {}

async def chat_server(reader: StreamReader, writer: StreamWriter):
    username = None
    lines = split_lines(reader)

    async for message in lines:
        if not username:
            username = message
            users[username] = writer
            print(f"{username} has joined.")
            continue

        print(f"Received {message!r} from {username}")

        for username, user_writer in users.items():
            await write(user_writer, message)

        if message == "quit":
            print(f"{username} has quit.")
            break

    writer.close()
    await writer.wait_closed()


async def async_main():
    server = await asyncio.start_server(
        chat_server, "127.0.0.1", 8888
    )

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"serving on {addrs}")

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("Exiting.")
