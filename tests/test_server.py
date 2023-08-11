import asyncio

import pytest

from chat.server import hello_world, ChatServer


def test_dummy_server():
    assert hello_world() == "Hello, world!"

@pytest.mark.asyncio()
async def test_server_can_accept_client():
    # users = {}
    server = ChatServer()
    server_task = asyncio.create_task(server.start())
    await asyncio.sleep(0.1)

    _, writer = await asyncio.open_connection("127.0.0.1", 8888)
    writer.write("test\n".encode())
    await asyncio.sleep(0.1)

    assert len(server.users) == 1
    server_task.cancel()