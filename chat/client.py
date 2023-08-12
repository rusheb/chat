import asyncio
from asyncio import StreamWriter

import aiofiles

from chat.server import ChatServer
from chat.common import write, split_lines


async def start_chat_client(name) -> None:
    reader, writer = await asyncio.open_connection(
        ChatServer.HOST, ChatServer.PORT
    )
    # the server is expecting a name first
    await write(writer, name)

    stdin_handler = asyncio.create_task(handle_stdin(writer))
    async for message in split_lines(reader):
        if message == "quit":
            break
        print(message)
    print("Goodbye.")
    stdin_handler.cancel()


async def handle_stdin(writer: StreamWriter) -> None:
    async with aiofiles.open("/dev/stdin", mode="rb") as f:
        async for line in f:
            text = line.decode()
            await write(writer, text)
