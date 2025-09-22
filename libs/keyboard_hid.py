import sys
import hid

from libs.config import Config

BYTES_TO_READ = 1


class Keyboard:
    def __init__(self):
        self.hid = None

        self.config = Config()

        self.hid = self.get_raw_hid_interface()
        if self.hid is None:
            self.print_instructions()
            sys.exit(1)

    def get_raw_hid_interface(self):
        device_interfaces = hid.enumerate()
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

    def notify_changes(self):
        try:
            data = self.hid.read(BYTES_TO_READ)
            if len(data) == 0:
                return
            response = int.from_bytes(data, sys.byteorder)
            print(f"Layer change detected: {response}")
            return response
        except KeyboardInterrupt:
            print("KeyboardInterrupt received. Exiting...")
        except Exception as e:
            print(f"An error occurred while reading from HID: {e}")

    def print_instructions(self):
        print("No keyboard found.")
        print(
            f"Please ensure your keyboard is connected and configured correctly on the file {self.config._config_file}"
        )

    def __del__(self):
        print("Cleaning up Keyboard resources...")
        if self.hid is not None:
            self.hid.close()
