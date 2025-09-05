import socket
import time
from zeroconf import (
    ServiceStateChange,
    ServiceInfo,
    ServiceBrowser,
    ServiceListener,
    Zeroconf,
)

service_type = "_keyboard._tcp.local."
service_name = f"Companion.{service_type}"


class Advertiser:
    def __init__(self, service_port=1977):
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

    def register(self):
        print(f"Registering service: {self.info.name}")
        self.zeroconf.register_service(self.info)

    def __end__(self):
        print("Unregistering service...")
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()


class ServiceDiscover:
    def __init__(self):
        self.service_info = None
        print("Searching for Companion App client..")
        self.zc = Zeroconf()
        browser = ServiceBrowser(self.zc, service_type, handlers=[self.add_service])

    def find(self):
        while self.service_info == None:
            time.sleep(1)
            print(".", end="", flush=True)
        return socket.inet_ntoa(self.service_info.addresses[0]), self.service_info.port

    def add_service(
        self,
        zeroconf: Zeroconf,
        service_type: str,
        name: str,
        state_change: ServiceStateChange,
    ) -> None:
        print(f"Service Info: {self.service_info}")
        info = zeroconf.get_service_info(service_type, name)
        self.service_info = info
        print(
            f"Service {name} added, address: {socket.inet_ntoa(info.addresses[0])}, port: {info.port}"
        )

    def __end__(self):
        self.zc.close()
