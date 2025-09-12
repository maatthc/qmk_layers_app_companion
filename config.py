import configparser


class Config:
    def __init__(self):
        self.config_file = "config.ini"
        config = configparser.ConfigParser()
        try:
            config.read(self.config_file)
        except configparser.Error as e:
            print(f"Error reading configuration file: {e}")
            exit(2)

        if "KEYBOARD_USB_HID" in config:
            keyboard = config["KEYBOARD_USB_HID"]
            self.vendor_id = int(keyboard["vendor_id"], 16)
            self.product_id = int(keyboard["product_id"], 16)
            self.usage_page = int(keyboard["usage_page"], 16)
            self.usage = int(keyboard["usage"], 16)
        else:
            print(
                f"KEYBOARD_USB_HID section not found in config file: {self.config_file}"
            )
            exit(2)

        if "LAYER_IMAGES" in config:
            values = config["LAYER_IMAGES"].values()
            self.layers = [v for v in values]
        else:
            print(f"LAYER_IMAGES section not found in config file: {self.config_file}")
            exit(2)
