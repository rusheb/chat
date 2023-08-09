import asyncio
from asyncio import StreamReader, StreamWriter

from common import write, split_lines

users = {}

async def chat_server(reader: StreamReader, writer: StreamWriter):
    addr = writer.get_extra_info("peername")
    print(f"{addr} has joined")
    async for message in split_lines(reader):
        print(f"Received {message!r} from {addr}")

        await write(writer, message)

        if message == "quit":
            print(f"{addr} has quit.")
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
