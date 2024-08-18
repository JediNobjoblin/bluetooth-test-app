import bluetooth

def scan_for_devices():
    print("Scanning for nearby Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

    if not nearby_devices:
        print("No devices found.")
    else:
        print(f"Found {len(nearby_devices)} devices.")
        for idx, device in enumerate(nearby_devices):
            address = device
            name = bluetooth.lookup_name(address)
            print(f"{idx + 1}: {name} ({address})")

    return nearby_devices


def connect_to_devices(device_address):
    print(f"Connecting to {device_address}...")
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((device_address, 1))
    return sock

def send_and_receive(sock):
    try:
        message = "Hello, Bluetooth device!"
        print(f"Sending message: {message}")
        # Here you would typically send the message and wait for a response
        sock.send(message)
        response = sock.recv(1024)
        print(f"Received response: {response}")
    finally:
        sock.close()

if __name__ == "__main__":
    devices = scan_for_devices()

    if devices:
        device_address = devices[0] # Use the first found device for testing
        sock = connect_to_devices(device_address)
        send_and_receive(sock)
