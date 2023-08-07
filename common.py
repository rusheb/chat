import asyncio
from asyncio import StreamWriter


async def send_message(writer: StreamWriter, message: str):
    for char in message:
        writer.write(char.encode())
        await writer.drain()
        # Simulate network latency
        await asyncio.sleep(0.1)
