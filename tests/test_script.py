import yaml
from src.bluetooth_scanner import BluetoothScanner
from src.bluetooth_device import BluetoothDevice

def load_config():
    with open("config/settings.yaml", 'r') as config_file:
        return yaml.safe_load(config_file)

def run_test_scan(config):
    scanner = BluetoothScanner(config=config)
    devices = scanner.scan_for_devices()

    if devices:
        address, name = devices[0]  # Select the first device found for testing
        return BluetoothDevice(address=address, name=name, config=config)
    return None

def run_test_connection(device):
    if device:
        device.connect()
        device.send_and_receive("Test message for connection")
    else:
        print("No devices found to test connection.")

if __name__ == "__main__":
    # Load configuration
    config = load_config()

    print("Running Bluetooth scan test...")
    device = run_test_scan(config)

    if device:
        print("\nRunning Bluetooth connection test...")
        run_test_connection(device)
    else:
        print("No device found to run connection test.")

