import asyncio
from asyncio import StreamReader, StreamWriter

from common import read_line


async def handle_echo(reader: StreamReader, writer: StreamWriter):
    first_message = await reader.read(100)
    client_name = first_message.decode()
    print(f"New client: {client_name}")

    while True:
        message = await read_line(reader)

        print(f"Received {message!r} from {client_name!r}")

        if message == "quit":
            break

        print(f"Sending {message!r}")
        writer.write(message.encode())
        await writer.drain()

    print(f"{client_name} has left")
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
