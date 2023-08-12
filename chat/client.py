import asyncio
from asyncio import StreamWriter

import aiofiles

from chat.common import write, split_lines


async def start_chat_client(name):
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    stdin_handler = asyncio.create_task(handle_stdin(writer))

    await write(writer, name)

    async for message in split_lines(reader):
        if message == "quit":
            break

        print(message)

    print("Goodbye.")
    stdin_handler.cancel()


async def handle_stdin(writer: StreamWriter):
    async with aiofiles.open("/dev/stdin", mode="rb") as f:
        async for line in f:
            text: str = line.decode()
            await write(writer, text)


