import asyncio
from asyncio import StreamWriter, StreamReader


async def write(writer: StreamWriter, message: str):
    for char in message:
        writer.write(char.encode())
        # Simulate network latency
        await asyncio.sleep(0.1)
    await writer.drain()

async def read_line(reader: StreamReader) -> str:
    message = []
    while True:
        # assume we are just getting one char
        data = await reader.read(100)
        char = data.decode()

        message.append(char)

        if char == "\n":
            break

    return "".join(message)

