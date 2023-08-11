import asyncio
from asyncio import StreamReader, StreamWriter

from chat.common import write, split_lines


# users: Dict[str, asyncio.Queue] = {}

def hello_world():
    return "Hello, world!"

class ChatServer:
    def __init__(self):
        self.users = {}
        self.server = None

    async def start(self) -> None:
        self.server = await asyncio.start_server(
            self.handle_connection, "127.0.0.1", 8888
        )

        addrs = ", ".join(str(sock.getsockname()) for sock in self.server.sockets)
        print(f"serving on {addrs}")

        return self.server

    async def run_forever(self):
        await self.start()
        async with self.server:
            await self.server.serve_forever()

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        my_queue = asyncio.Queue()
        write_handler = asyncio.create_task(self.handle_writes(writer, my_queue))
        username = None
        addr = writer.get_extra_info("peername")

        async for message in split_lines(reader):
            if not username:
                username = message
                self.users[username] = my_queue
                print(f"{username} ({addr}) has joined.")
                continue

            print(f"Received {message!r} from {username} ({addr})")

            if message == "quit":
                print(f"{username} left.")
                del self.users[username]
                await my_queue.put(message)
                break

            for their_queue in self.users.values():
                await their_queue.put(f"<{username}> {message}")

        await write_handler

        writer.close()
        await writer.wait_closed()

    async def handle_writes(self, writer: StreamWriter, queue: asyncio.Queue):
        while True:
            message = await queue.get()
            await write(writer, message)

