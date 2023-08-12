import asyncio
from asyncio import StreamReader, StreamWriter
from contextlib import suppress

from chat.common import write, split_lines


class ChatServer:
    def __init__(self):
        self.users = {}
        self.server = None
        self.connections = set()

    async def start(self) -> asyncio.Server:
        self.server = await asyncio.start_server(
            self.handle_connection, "127.0.0.1", 8888
        )

        addrs = ", ".join(str(sock.getsockname()) for sock in self.server.sockets)
        print(f"serving on {addrs}")

        return self.server

    async def run_forever(self) -> None:
        await self.start()
        async with self.server:
            await self.server.serve_forever()

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()

        while self.connections:
            await asyncio.gather(*self.connections)

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        current_task = asyncio.current_task()
        self.connections.add(current_task)

        user_queue = asyncio.Queue()
        write_handler = asyncio.create_task(self.handle_writes(writer, user_queue))
        addr = writer.get_extra_info("peername")
        username = None

        try:
            async for message in split_lines(reader):
                # the first message the client sends is their username
                if not username:
                    username = message
                    self.users[username] = user_queue
                    print(f"{username} ({addr}) has joined.")
                    continue

                print(f"Received {message!r} from {username} ({addr})")

                if message == "quit":
                    break

                # broadcast message to all users
                for their_queue in self.users.values():
                    await their_queue.put(f"<{username}> {message}")
        finally:
            del self.users[username]
            print(f"{username} ({addr}) has left.")
            write_handler.cancel()
            await write_handler

            self.connections.remove(current_task)

    async def handle_writes(self, writer: StreamWriter, queue: asyncio.Queue):
        try:
            while True:
                message = await queue.get()
                await write(writer, message)
        except asyncio.CancelledError:
            with suppress(BrokenPipeError):
                await write(writer, "quit")


