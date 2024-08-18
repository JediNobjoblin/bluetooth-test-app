import yaml
import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bluetooth_scanner import BluetoothScanner
from src.bluetooth_device import BluetoothDevice

def load_config():
    with open("config/settings.yaml", 'r') as config_file:
        return yaml.safe_load(config_file)

def main():
    config = load_config()
    scanner = BluetoothScanner(config=config)
    print("Starting Bluetooth scan...")
    devices = scanner.scan_for_devices()

    if devices:
        address, name = devices[0]  # Select the first device found
        device = BluetoothDevice(address=address, name=name, config=config)
        device.connect()
        device.send_and_receive(config['bluetooth'].get('test_message', 'Hello from Docker!'))
    else:
        print("No devices found during the scan.")

if __name__ == "__main__":
    main()

