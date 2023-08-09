import asyncio
from asyncio import StreamWriter, StreamReader


async def write(writer: StreamWriter, message: str):
    if not message.endswith("\n"):
        message += "\n"
    for char in message:
        writer.write(char.encode())
        # Simulate network latency
        await asyncio.sleep(0.1)
    await writer.drain()


async def split_lines(reader: StreamReader):
    buffer = b""
    while True:
        buffer = buffer + await reader.read(100)
        if b"\n" in buffer:
            data, buffer = buffer.split(b"\n", 1)
            yield data.decode()
