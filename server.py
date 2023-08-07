import asyncio
from asyncio import StreamReader, StreamWriter


async def handle_echo(reader: StreamReader, writer: StreamWriter):
    while True:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info("peername")

        print(f"Received {message!r} from {addr!r}")

        if message == "quit":
            break

        print(f"Sending {message!r}")
        writer.write(data)
        await writer.drain()

    print("Closing the connection")
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
    asyncio.run(async_main())
