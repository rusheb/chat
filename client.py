import asyncio
import sys

from common import write, read_line


async def chat_client(name: str):
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 8888
    )

    writer.write(name.encode())
    await writer.drain()

    for line in sys.stdin:
        print(f"Sending: {line!r}")
        await write(writer, line)

        if line == "quit\n":
            break

        data = await read_line(reader)
        print(f"Received {data!r}")

    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: client.py <NAME>")
        sys.exit(1)

    name = sys.argv[1]
    asyncio.run(chat_client(name))
