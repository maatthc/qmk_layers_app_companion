import configparser
import sys


class Config:
    _config_file = "config.ini"
    _config = None

    @staticmethod
    def __init__():
        if Config._config is not None:
            return
        print("Loading configuration...")
        Config._config = configparser.ConfigParser()
        try:
            Config._config.read(Config._config_file)
        except configparser.Error as e:
            print(f"Error reading configuration file: {e}")
            sys.exit(2)

        if "KEYBOARD_USB_HID" in Config._config:
            keyboard = Config._config["KEYBOARD_USB_HID"]
            Config.vendor_id = int(keyboard["vendor_id"], 16)
            Config.product_id = int(keyboard["product_id"], 16)
            Config.usage_page = int(keyboard["usage_page"], 16)
            Config.usage = int(keyboard["usage"], 16)
        else:
            print(
                f"KEYBOARD_USB_HID section not found in config file: {Config._config_file}"
            )
            sys.exit(2)

        if "LAYER_IMAGES" in Config._config:
            values = Config._config["LAYER_IMAGES"].values()
            Config.layers = [v for v in values]
        else:
            print(
                f"LAYER_IMAGES section not found in config file: {Config._config_file}"
            )
            exit(2)
