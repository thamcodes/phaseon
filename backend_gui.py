import serial
import time
from PyQt6.QtCore import QObject, pyqtSignal

class BrainWorker(QObject):
    # Signal to update the badge text in the frontend
    arduino_status = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.arduino = None

    def connect_arduino(self, port):
        """Connects to the Arduino at the given port (e.g., COM3)"""
        try:
            # Standard connection: 9600 baud
            self.arduino = serial.Serial(port, 9600, timeout=1)
            time.sleep(2) # Allow Arduino to reset
            self.arduino_status.emit("Connected")
        except Exception as e:
            self.arduino_status.emit("Connection Failed")
            print(f"Arduino Error: {e}")

    def disconnect_arduino(self):
        """Closes the connection"""
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
        self.arduino = None
        self.arduino_status.emit("Disconnected")