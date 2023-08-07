import asyncio


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 8888
    )

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
    asyncio.run(tcp_echo_client())
