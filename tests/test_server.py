import asyncio

import pytest

from chat.server import ChatServer


@pytest.mark.asyncio()
async def test_server():
    server = ChatServer()
    asyncio.create_task(server.start())
    await asyncio.sleep(0.01)

    _, writer = await asyncio.open_connection("127.0.0.1", 8888)
    writer.write("username\n".encode())  # send username
    await asyncio.sleep(0.01)

    assert len(server.users) == 1

    writer.close()
    await server.stop()
