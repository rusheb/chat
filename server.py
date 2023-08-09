import asyncio
from asyncio import StreamReader, StreamWriter

from common import write, split_lines

users = {}

async def handle_writes(writer: StreamWriter, queue: asyncio.Queue):
    while True:
        message = await queue.get()
        await write(writer, message)

async def handle_connection(reader: StreamReader, writer: StreamWriter):
    my_queue = asyncio.Queue()
    write_handler = asyncio.create_task(handle_writes(writer, my_queue))
    ctx = {
        "addr": str(writer.get_extra_info("peername")),
        "username": "",
    }

    async for message in split_lines(reader):
        username = ctx['username']
        addr = ctx['addr']

        if not username:
            print("Setting username")
            username = message
            ctx["username"] = username
            users[username] = my_queue
            print(f"{username} ({ctx['addr']}) has joined.")
            continue

        print(f"Received {message!r} from {username} ({addr})")

        if message == "quit":
            print(f"{username} left.")
            del users[username]
            await my_queue.put(message)
            break

        for their_queue in users.values():
            await their_queue.put(message)

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
