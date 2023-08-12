import asyncio

import pytest
import pytest_asyncio

from chat.server import ChatServer

@pytest_asyncio.fixture
async def server():
    chat_server = ChatServer()
    await chat_server.start()
    yield chat_server
    await chat_server.stop()

@pytest.mark.asyncio()
async def test_server(server):
    _, writer = await asyncio.open_connection("127.0.0.1", 8888)
    writer.write("username\n".encode())
    await asyncio.sleep(0.01)
    assert len(server.users) == 1
    writer.close()

@pytest.mark.asyncio()
async def test_server_multiple_users(server):
    writers = []
    for i in range(3):
        _, writer = await asyncio.open_connection("127.0.0.1", 8888)
        writer.write(f"user{i}\n".encode())
        writers.append(writer)

    await asyncio.sleep(0.01)
    assert len(server.users) == 3
    for writer in writers:
        writer.close()

@pytest.mark.asyncio()
async def test_client_quits(server):
    _, writer = await asyncio.open_connection("127.0.0.1", 8888)
    writer.write("username\n".encode())

    await asyncio.sleep(0.01)
    assert len(server.users) == 1

    writer.write("quit\n".encode())
    await asyncio.sleep(0.01)
    assert len(server.users) == 0

    writer.close()

@pytest.mark.asyncio()
async def test_client_quits_abruptly(server):
    _, writer = await asyncio.open_connection("127.0.0.1", 8888)
    writer.write("username\n".encode())

    await asyncio.sleep(0.01)
    assert len(server.users) == 1

    writer.close()
    await asyncio.sleep(0.01)
    assert len(server.users) == 0
