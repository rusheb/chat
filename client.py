import asyncio
import sys


async def tcp_echo_client(name: str):
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 8888
    )

    writer.write(name.encode())
    await writer.drain()

    while True:
        message = input()
        print(f"Sending: {message!r}")
        writer.write(message.encode())
        await writer.drain()

        if message == "quit":
            break

        data = await reader.read(100)
        print(f"Received {data.decode()!r}")

    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: client.py <NAME>")
        sys.exit(1)

    name = sys.argv[1]
    asyncio.run(tcp_echo_client(name))
