import asyncio
from asyncio import StreamReader, StreamWriter

from common import read_line, write

users = {}

async def handle_echo(reader: StreamReader, writer: StreamWriter):
    first_message = await reader.read(100)
    username = first_message.decode()
    print(f"New client: {username}")
    users[username] = writer

    while True:
        message = await read_line(reader)

        print(f"Received {message!r} from {username!r}")

        if message == "quit\n":
            break

        print(f"Sending {message!r}")
        for user, user_writer in users.items():
            print(f"sending to {user}")
            await write(user_writer, message)

    print(f"{username} has left")
    writer.close()
    await writer.wait_closed()

async def async_main():
    server = await asyncio.start_server(
        handle_echo, "127.0.0.1", 8888
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
