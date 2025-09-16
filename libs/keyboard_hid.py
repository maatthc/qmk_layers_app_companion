import hid
import threading
from libs.config import Config

BYTES_TO_READ = 1


class Keyboard:
    def __init__(self, send_keystroke):
        self.gui = None
        self.interface = None

        self.send_keystroke = send_keystroke
        self.config = Config()
        self.interface = self.get_raw_hid_interface()
        if self.interface is None:
            self.print_instructions()
            exit(1)

        self.event = threading.Event()
        self.thread = threading.Thread(
            target=self.listen_to_layer_changes,
        )
        self.thread.deamon = True
        self.thread.start()

    def set_gui(self, gui):
        self.gui = gui
        self.gui.set_thread_event(self.event)

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
        while not self.event.is_set():
            data = self.interface.read(BYTES_TO_READ)
            if len(data) == 0:
                continue
            response = int.from_bytes(data)
            self.send_keystroke(response)

    def print_instructions(self):
        print("No keyboard found.")
        print(
            f"Please ensure your keyboard is connected and configured correctly on the file {self.config.config_file}"
        )

    def __del__(self):
        if self.interface is not None:
            self.interface.close()
