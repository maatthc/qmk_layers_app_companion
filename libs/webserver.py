import asyncio
import mimetypes
import socket
from pathlib import Path
from aiohttp import web, WSMsgType
from aiohttp.web import Application, AppRunner, TCPSite, FileResponse
import json
import logging
from datetime import datetime
import errno

from .consumer import ConsumerInterface
from .config import Config

imageFolder = "./assets/"


class WebSocketManager:
    def __init__(self):
        self.clients: set = set()

    async def add_client(self, websocket):
        self.clients.add(websocket)
        logging.info(f"WebSocket client connected. Total clients: {len(self.clients)}")

    async def remove_client(self, websocket):
        self.clients.discard(websocket)
        logging.info(
            f"WebSocket client disconnected. Total clients: {len(self.clients)}"
        )

    async def broadcast(self, message: str):
        if not self.clients:
            return

        for client in self.clients:
            try:
                await client.send_str(message)
            except Exception as e:
                logging.warning(f"Failed to send message to client: {e}")
                await self.remove_client(client)


class WebServer(ConsumerInterface):
    def __init__(self, keyboard_listener, args):
        self.host = "0.0.0.0"
        self.port = args.server_port
        self.current_layer = 0
        self.keyboard_listener = keyboard_listener
        self.args = args
        self.config = Config()

        self.websocket_manager = WebSocketManager()
        self.app: Application = None
        self.runner: AppRunner = None
        self.site: TCPSite = None
        self.keyboard_task = None

        logging.basicConfig(level=logging.INFO)

    def initial_msg(self):
        message = {
            "all_layers": self.config.layers,
        }
        return json.dumps(message)

    def build_msg(self):
        message = {
            "layer": self.current_layer,
            "image": self.config.layers[self.current_layer],
        }
        return json.dumps(message)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await self.websocket_manager.add_client(ws)

        try:
            await ws.send_str(self.initial_msg())
            async for msg in ws:
                if msg.type == WSMsgType.ERROR:
                    logging.error(f"WebSocket error: {ws.exception()}")
                    break
                elif msg.type == WSMsgType.CLOSE:
                    break
        except Exception as e:
            logging.error(f"WebSocket handler error: {e}")
        finally:
            await self.websocket_manager.remove_client(ws)

        return ws

    async def serve_static_file(
        self, file_path: str, content_type: str = None, status: int = 200
    ):
        try:
            full_path = Path(file_path).resolve()
            if not full_path.exists() or not full_path.is_file():
                return await self.serve_404()

            if content_type is None:
                content_type, _ = mimetypes.guess_type(str(full_path))
                if content_type is None:
                    content_type = "application/octet-stream"

            response = FileResponse(
                path=full_path,
                headers={
                    "Cache-Control": "public, max-age=31536000",  # Cache for 1 year
                    "Content-Type": content_type,
                },
            )

            return response

        except Exception as e:
            logging.error(f"Error serving static file {file_path}: {e}")
            return await self.serve_500()

    async def serve_index(self, req):
        return await self.serve_static_file("web/index.html", "text/html")

    async def serve_css(self, req):
        return await self.serve_static_file("web/styles.css", "text/css")

    async def serve_js(self, req):
        return await self.serve_static_file("web/app.js", "application/javascript")

    async def serve_assets(self, request):
        filename = request.match_info.get("filename", "")
        asset_path = f"{imageFolder}/{filename}"

        return await self.serve_static_file(asset_path)

    async def serve_error_page(self, file_path: str, status_code: int):
        return await self.serve_static_file(
            file_path, content_type="text/html", status=status_code
        )

    async def serve_404(self, request):
        return await self.serve_error_page("web/404.html", 404)

    async def serve_500(self):
        return await self.serve_error_page("web/500.html", 500)

    def get_network_ip(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                return local_ip
        except Exception as e:
            logging.warning(f"Could not determine network IP address: {e}")
            return None

    def display_startup_urls(self):
        print("\n" + "=" * 60)
        print("🚀 Keyboard Layers Web Interface Started")
        print("=" * 60)

        print("📱 Local Access:")
        print(f"   Web Interface: http://localhost:{self.port}")
        print(f"   WebSocket:     ws://localhost:{self.port}/ws")

        network_ip = self.get_network_ip()
        if network_ip:
            print("\n🌐 Network Access:")
            print(f"   Web Interface: http://{network_ip}:{self.port}")
            print(f"   WebSocket:     ws://{network_ip}:{self.port}/ws")
            print(
                "\n💡 Access from other devices on your network using the network URL"
            )
        else:
            print(
                "\n⚠️  Network IP detection failed - use localhost for local access only"
            )

        print("\n📋 Usage:")
        print("   • Open the web interface in any browser")
        print("   • Press Ctrl+C to stop the server")
        print("=" * 60 + "\n")

    def setup_routes(self):
        self.app.router.add_get("/", self.serve_index)
        self.app.router.add_get("/styles.css", self.serve_css)
        self.app.router.add_get("/app.js", self.serve_js)
        self.app.router.add_get("/assets/{filename}", self.serve_assets)
        self.app.router.add_get("/ws", self.websocket_handler)
        self.app.router.add_route("*", "/{path:.*}", self.serve_404)

    async def start(self):
        try:
            self.app = web.Application()
            self.setup_routes()
            self.runner = web.AppRunner(self.app)
            await self.runner.setup()

            try:
                self.site = web.TCPSite(self.runner, self.host, self.port)
                await self.site.start()
            except OSError as e:
                if e.errno == errno.EADDRINUSE:
                    print(f"\n❌ Error: Port {self.port} is already in use!")
                    await self.runner.cleanup()
                    raise SystemExit(1)
                else:
                    print(f"\n❌ Network Error: {e}")
                    print(f"   Failed to bind to {self.host}:{self.port}")
                    await self.runner.cleanup()
                    raise SystemExit(1)

            self.display_startup_urls()

            self.keyboard_task = asyncio.create_task(self.monitor_keyboard())
            logging.info("Keyboard monitoring started")

            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logging.info("Received shutdown signal")
                raise

        except KeyboardInterrupt:
            logging.info("Server shutdown requested")
            raise
        except SystemExit:
            raise
        except Exception as e:
            logging.error(f"Failed to start web server: {e}")
            await self.cleanup()
            raise

    async def monitor_keyboard(self):
        while True:
            try:
                await asyncio.sleep(0.1)
                layer_change = self.keyboard_listener.notify_changes()
                if layer_change is not None:
                    await self.handle_layer_change(layer_change)

            except KeyboardInterrupt:
                logging.info("Keyboard monitoring task cancelled")
                break
            except Exception as e:
                logging.error(f"Error in keyboard monitoring: {e}")
                disconnect_message = {
                    "type": "keyboard_disconnected",
                    "message": "Keyboard disconnected - layer updates unavailable",
                    "timestamp": datetime.now().isoformat(),
                }
                await self.websocket_manager.broadcast(json.dumps(disconnect_message))
                break
        logging.info("Keyboard monitoring task ended")

    async def handle_layer_change(self, layer: int):
        try:
            if layer < 0 or layer >= len(self.config.layers):
                logging.warning(f"Invalid layer number received: {layer}")
                return

            if layer == self.current_layer:
                return

            self.current_layer = layer
            await self.websocket_manager.broadcast(self.build_msg())
            logging.info(
                f"Layer changed to {layer}, broadcasted to {len(self.websocket_manager.clients)} clients"
            )

        except Exception as e:
            logging.error(f"Error handling layer change: {e}")

    async def cleanup(self):
        logging.info("Starting web server cleanup...")
        try:
            if self.keyboard_task and not self.keyboard_task.done():
                logging.info("Cancelling keyboard monitoring task...")
                self.keyboard_task.cancel()
                try:
                    await self.keyboard_task
                except asyncio.CancelledError:
                    logging.info("Keyboard monitoring task cancelled")

            if self.websocket_manager.clients:
                logging.info(
                    f"Closing {len(self.websocket_manager.clients)} WebSocket connections..."
                )

                shutdown_message = {
                    "type": "server_shutdown",
                    "message": "Server is shutting down",
                    "timestamp": datetime.now().isoformat(),
                }
                try:
                    await asyncio.wait_for(
                        self.websocket_manager.broadcast(json.dumps(shutdown_message)),
                        timeout=2.0,
                    )
                except asyncio.TimeoutError:
                    logging.warning("Timeout while notifying clients of shutdown")

                clients_copy = self.websocket_manager.clients.copy()
                for client in clients_copy:
                    try:
                        await client.close()
                    except Exception as e:
                        logging.warning(f"Error closing WebSocket client: {e}")

                self.websocket_manager.clients.clear()

            if self.site:
                logging.info("Stopping HTTP site...")
                await self.site.stop()
                self.site = None

            if self.runner:
                logging.info("Cleaning up app runner...")
                await self.runner.cleanup()
                self.runner = None

            logging.info("Web server cleanup completed")

        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

    def stop(self):
        """Stop the web server and clean up resources (sync wrapper)"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.cleanup())
            else:
                asyncio.run(self.cleanup())

            logging.info("Web server stop initiated")

        except Exception as e:
            logging.error(f"Error stopping web server: {e}")
            try:
                if self.site:
                    self.site = None
                if self.runner:
                    self.runner = None
                logging.info("Basic cleanup completed")
            except Exception as cleanup_error:
                logging.error(f"Error in fallback cleanup: {cleanup_error}")
