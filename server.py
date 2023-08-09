import asyncio
from asyncio import StreamReader, StreamWriter

from common import write, split_lines

users = {}

async def handle_writes(writer: StreamWriter, queue: asyncio.Queue):
    while True:
        message = await queue.get()
        await write(writer, message)

async def handle_connection(reader: StreamReader, writer: StreamWriter):
    username = None
    queue = asyncio.Queue()
    addr = writer.get_extra_info("peername")

    write_handler = asyncio.create_task(handle_writes(writer, queue))

    async for message in split_lines(reader):
        if not username:
            print("Setting username")
            username = message
            users[username] = queue
            print(f"{username} ({addr}) has joined.")
            continue

        print(f"Received {message!r} from {username} ({addr})")

        if message == "quit":
            print(f"{username} left.")
            del users[username]
            await queue.put(message)
            break

        for username, queue in users.items():
            await queue.put(message)

    write_handler.cancel()
    await write_handler

    writer.close()
    await writer.wait_closed()


async def async_main():
    server = await asyncio.start_server(
        handle_connection, "127.0.0.1", 8888
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
