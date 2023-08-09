import asyncio
from asyncio import StreamWriter

import aiofiles

from common import write, split_lines


async def handle_stdin(writer: StreamWriter):
    async with aiofiles.open("/dev/stdin", mode="rb") as f:
        async for line in f:
            text: str = line.decode()
            await write(writer, text)


async def chat_client():
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    stdin_handler = asyncio.create_task(handle_stdin(writer))

    async for message in split_lines(reader):
        if message == "quit":
            print("Quitting")
            break

        print(f"Received {message!r}")

    stdin_handler.cancel()


if __name__ == '__main__':
    asyncio.run(chat_client())
