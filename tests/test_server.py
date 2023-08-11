import asyncio
import pytest

from chat.server import hello_world, start_chat_server


def test_dummy_server():
    assert hello_world() == "Hello, world!"

@pytest.mark.asyncio()
async def test_server_can_accept_client():
    users = {}
    server_task = asyncio.create_task(start_chat_server())
    await asyncio.open_connection("127.0.0.1", 8888)

    # assert len(users) == 1
    # server_task.cancel()
