import asyncio
from libs.zeroconfig import Advertiser
from libs.consumer import ConsumerInterface


class Server(ConsumerInterface):
    def __init__(self, keyboard, args):
        self.host = "0.0.0.0"
        self.port = args.server_port
        self.keyboard = keyboard
        self.clients: set[asyncio.StreamWriter] = set()
        self.adv = Advertiser(self.port)

    async def start(self):
        await self.adv.register()

        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"Server started on {addr[0]}:{addr[1]}")

        periodic_task = asyncio.create_task(
            self.periodic_update(), name="periodic_update"
        )

        try:
            async with server:
                await server.serve_forever()
        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            print("Server shutting down...")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            periodic_task.cancel()
            server.close()
            await server.wait_closed()

    async def handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        client_addr = writer.get_extra_info("peername")
        print(f"New client connected: {client_addr}")

        self.clients.add(writer)

    async def periodic_update(self):
        while True:
            try:
                await asyncio.sleep(0.1)

                message = self.keyboard.notify_changes()
                if message is not None:
                    await self.broadcast_update(str(message))

            except KeyboardInterrupt:
                print("Periodic update task cancelled")
            except Exception as e:
                print(f"Error in periodic update: {e}")

    async def broadcast_update(self, message: str):
        if not self.clients:
            return

        disconnected_clients = set()

        for client in self.clients.copy():
            try:
                client.write(message.encode())
                await client.drain()
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                disconnected_clients.add(client)

        self.clients -= disconnected_clients
        print(f"Broadcasted update to {len(self.clients)} clients")
