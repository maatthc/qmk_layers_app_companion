import hid
from config import Config

BYTES_TO_READ = 1


class Keyboard:
    def __init__(self, listener):
        self.gui = None
        self.hid = None

        self.updateLayer = listener.updateLayer
        self.config = Config()

        self.hid = self.get_raw_hid_interface()
        if self.hid is None:
            self.print_instructions()
            exit(1)

        self.listen_to_layer_changes()

    def get_raw_hid_interface(self):
        device_interfaces = hid.enumerate(self.config.vendor_id, self.config.product_id)
        raw_hid_interfaces = [
            i
            for i in device_interfaces
            if i["usage_page"] == self.config.usage_page
            and i["usage"] == self.config.usage
        ]

        if len(raw_hid_interfaces) == 0:
            return None

        interface = hid.Device(path=raw_hid_interfaces[0]["path"])
        interface.nonblocking = True
        print(f"Keyboard Manufacturer: {interface.manufacturer}")
        print(f"Keyboard Product: {interface.product}")
        return interface

    def listen_to_layer_changes(self):
        while True:
            data = self.hid.read(BYTES_TO_READ)
            if len(data) == 0:
                continue
            response = int.from_bytes(data)
            self.updateLayer(response)

    def print_instructions(self):
        print("No keyboard found.")
        print(
            f"Please ensure your keyboard is connected and configured correctly on the file {self.config.config_file}"
        )

    def __del__(self):
        if self.hid is not None:
            self.hid.close()
