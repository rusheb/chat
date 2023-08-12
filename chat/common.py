import asyncio
from asyncio import StreamWriter, StreamReader


async def write(writer: StreamWriter, message: str) -> None:
    if not message.endswith("\n"):
        message += "\n"
    for char in message:
        writer.write(char.encode())
        # Simulate network latency
        await asyncio.sleep(0.05)
    await writer.drain()


async def split_lines(reader: StreamReader) -> str:
    buffer = b""
    while True:
        data = await reader.read(100)
        if data == b"":
            break
        buffer = buffer + data
        if b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            yield line.decode()
