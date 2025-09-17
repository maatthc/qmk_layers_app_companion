import socket
import asyncio
from zeroconf import (
    ServiceStateChange,
    ServiceInfo,
    Zeroconf,
)
from zeroconf.asyncio import (
    AsyncServiceBrowser,
    AsyncServiceInfo,
    AsyncZeroconf,
)

service_type = "_keyboard._tcp.local."
service_name = f"Companion.{service_type}"


class Advertiser:
    def __init__(self, service_port=1977):
        self.running_task = None
        self.zeroconf = Zeroconf()
        service_properties = {"path": "/", "version": "1.0"}

        host_name = socket.gethostname() + ".local."
        host_ip = socket.gethostbyname(host_name)
        addresses = [socket.inet_aton(host_ip)]

        self.info = ServiceInfo(
            service_type,
            service_name,
            addresses=addresses,
            port=service_port,
            properties=service_properties,
            server=host_name,
        )

    async def registered_task(self):
        while True:
            try:
                await self.zeroconf.async_register_service(self.info)
            except KeyboardInterrupt:
                break
            except Exception:
                pass
            await asyncio.sleep(1)
        print("Exiting Zeroconf background task")

    async def register(self):
        print(f"Registering service: {self.info.name}")
        self.running_task = asyncio.create_task(self.registered_task())

    def __end__(self):
        print("Unregistering service...")
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()
        if self.running_task is not None:
            self.running_task.cancel()


class ServiceDiscover:
    def __init__(self):
        self.service_info = None
        print("Searching for Companion App server..")
        self.zc = AsyncZeroconf()

    async def find(self):
        AsyncServiceBrowser(self.zc.zeroconf, service_type, handlers=[self.add_service])
        while self.service_info is None:
            await asyncio.sleep(1)
            print(".", end="", flush=True)
        return socket.inet_ntoa(self.service_info.addresses[0]), self.service_info.port

    def add_service(
        self,
        zeroconf: Zeroconf,
        service_type: str,
        name: str,
        state_change: ServiceStateChange,
    ) -> None:
        try:
            asyncio.ensure_future(
                self.async_display_service_info(zeroconf, service_type, name)
            )
        except Exception as e:
            print(f"Error retrieving service info: {e}")

    async def async_display_service_info(
        self, zeroconf: Zeroconf, service_type: str, name: str
    ):
        info = AsyncServiceInfo(service_type, name)
        await info.async_request(zeroconf, 3000)
        self.service_info = info
        print(
            f"Added service {name} - address: {socket.inet_ntoa(info.addresses[0])}, port: {info.port}"
        )

    def __end__(self):
        self.zc.close()
