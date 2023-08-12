import asyncio
from asyncio import StreamReader, StreamWriter
from contextlib import suppress

from chat.common import write, split_lines


class ChatServer:
    HOST: str = "127.0.0.1"
    PORT: str = 8888

    def __init__(self):
        self.users = {}
        self.server = None
        self.connections = set()

    async def start(self) -> None:
        self.server = await asyncio.start_server(
            self.handle_connection, self.HOST, self.PORT
        )

        addrs = ", ".join(
            str(sock.getsockname()) for sock in self.server.sockets
        )
        print(f"serving on {addrs}")

    async def run_forever(self) -> None:
        await self.start()
        async with self.server:
            await self.server.serve_forever()

    async def stop(self) -> None:
        if self.server:
            self.server.close()
            await self.server.wait_closed()

        while self.connections:
            await asyncio.gather(*self.connections)

    async def handle_connection(
        self, reader: StreamReader, writer: StreamWriter
    ) -> None:
        current_task = asyncio.current_task()
        self.connections.add(current_task)

        user_queue = asyncio.Queue()
        write_handler = asyncio.create_task(
            self.handle_writes(writer, user_queue)
        )
        addr = writer.get_extra_info("peername")
        username = None

        try:
            async for message in split_lines(reader):
                # the first message the client sends is their username
                if not username:
                    username = message
                    online = [f"<{user}>" for user in self.users.keys()]
                    online_message = "Nobody else is here." if not online else (
                        f"Online users: {', '.join(online)}"
                    )
                    await user_queue.put( f"Welcome, <{username}>! {online_message}" )
                    self.users[username] = user_queue
                    for user, their_queue in self.users.items():
                        if user == username:
                            continue
                        await their_queue.put(f"<{username}> has joined.")
                    print(f"<{username}> {addr} has joined.")
                    continue

                print(f"<{username}> {addr} {message!r}")

                if message == "quit":
                    break

                # broadcast message to all users
                for their_queue in self.users.values():
                    await their_queue.put(f"<{username}> {message}")
        finally:
            if username in self.users:
                del self.users[username]
            for their_queue in self.users.values():
                await their_queue.put(f"<{username}> has left.")
            print(f"<{username}> {addr} has left.")
            write_handler.cancel()
            await write_handler

            self.connections.remove(current_task)

    async def handle_writes(
        self, writer: StreamWriter, queue: asyncio.Queue
    ) -> None:
        try:
            while True:
                message = await queue.get()
                await write(writer, message)
        except asyncio.CancelledError:
            with suppress(BrokenPipeError):
                await write(writer, "quit")
