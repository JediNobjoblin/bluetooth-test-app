import bluetooth
import yaml

class BluetoothScanner:
    def __init__(self, config):
        self.scan_duration = config.get('bluetooth', {}).get('scan_timeout', 8)
        self.flush_cache = config.get('bluetooth', {}).get('flush_cache', True)
        self.lookup_class = config.get('bluetooth', {}).get('lookup_class', False)

    def scan_for_devices(self):
        print("Scanning for nearby Bluetooth devices...")
        nearby_devices = bluetooth.discover_devices(
            duration=self.scan_duration,
            lookup_names=False,  # We will manually lookup names
            flush_cache=self.flush_cache,
            lookup_class=self.lookup_class
        )

        devices = []
        if not nearby_devices:
            print("No devices found.")
        else:
            print(f"Found {len(nearby_devices)} devices.")
            for idx, address in enumerate(nearby_devices):
                print(f"Debug: Found device with address {address}")
                try:
                    name = bluetooth.lookup_name(address)
                    print(f"{idx + 1}: {name} ({address})")
                    devices.append((address, name))
                except bluetooth.BluetoothError as e:
                    print(f"Error looking up name for {address}: {e}")
                    devices.append((address, "Unknown"))

        return devices

