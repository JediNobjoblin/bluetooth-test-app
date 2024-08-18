import bluetooth
import time

class BluetoothDevice:
    def __init__(self, address, name=None, config=None):
        self.address = address
        self.name = name
        self.socket = None
        self.connection_timeout = config.get('bluetooth', {}).get('connection_timeout', 10)
        self.auto_reconnect = config.get('bluetooth', {}).get('auto_reconnect', False)
        self.max_reconnect_attempts = config.get('bluetooth', {}).get('max_reconnect_attempts', 3)
        self.reconnect_attempts = 0
        self.allowed_devices = config.get('security', {}).get('allowed_devices', [])

        if self.address not in self.allowed_devices:
            raise ValueError(f"Device {self.address} not allowed to connect.")

    def connect(self):
        try:
            print(f"Connecting to {self.address}...")
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.connect((self.address, 1))
            print(f"Connected to {self.address}")
            self.reconnect_attempts = 0  # Reset reconnect attempts on successful connection
        except Exception as e:
            print(f"Failed to connect to {self.address}: {e}")
            if self.auto_reconnect:
                self.reconnect()

    def reconnect(self):
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            print(f"Attempting to reconnect to {self.address} (Attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})...")
            time.sleep(2)  # Delay before trying to reconnect
            self.connect()
        else:
            print(f"Max reconnect attempts reached for {self.address}. Giving up.")

    def send_and_receive(self, message):
        try:
            print(f"Sending message: {message}")
            self.socket.send(message)
            data = self.socket.recv(1024)
            print(f"Received: {data}")
        except Exception as e:
            print(f"Failed to send or receive data: {e}")
        finally:
            self.socket.close()

    def disconnect(self):
        if self.socket:
            self.socket.close()
            print(f"Disconnected from {self.address}")

