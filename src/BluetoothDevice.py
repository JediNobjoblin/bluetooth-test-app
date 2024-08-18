import bluetooth

class BluetoothDevice:
    def __init__(self, address, name=None, config=None):
        self.address = address
        self.name = name
        self.socket = None
        self.connection_timeout = config.get('bluetooth', {}).get('connection_timeout', 10)
        self.auto_reconnect = config.get('bluetooth', {}).get('auto_reconnect', False)
        self.max_reconnect_attempts = config.get('bluetooth', {}).get('max_reconnect_attempts', 3)
        self.allowed_devices = config.get('security', {}).get('allowed_devices', [])

        # Check if the device is allowed
        if self.address not in self.allowed_devices:
            raise ValueError(f"Device {self.address} not allowed to connect.")

    def connect(self):
        print(f"Connecting to {self.name or 'Unknown device'} ({self.address})...")
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.settimeout(self.connection_timeout)
        try:
            self.socket.connect((self.address, 1))
            print("Connected successfully.")
        except bluetooth.BluetoothError as e:
            print(f"Failed to connect: {e}")
            if self.auto_reconnect:
                self.reconnect()
        return self.socket

    def reconnect(self):
        attempt = 0
        while attempt < self.max_reconnect_attempts:
            attempt += 1
            print(f"Reconnection attempt {attempt}/{self.max_reconnect_attempts}")
            try:
                self.connect()
                break
            except bluetooth.BluetoothError as e:
                print(f"Reconnection attempt failed: {e}")
                if attempt >= self.max_reconnect_attempts:
                    raise

    def send_and_receive(self, message="Hello, Bluetooth device!"):
        if self.socket is None:
            raise ValueError("Device is not connected.")
        try:
            print(f"Sending message: {message}")
            self.socket.send(message)
            response = self.socket.recv(1024)
            print(f"Received response: {response.decode('utf-8')}")
        finally:
            self.disconnect()

    def disconnect(self):
        if self.socket:
            print(f"Disconnecting from {self.name or 'Unknown device'} ({self.address})...")
            self.socket.close()
            self.socket = None
            print("Disconnected successfully.")
