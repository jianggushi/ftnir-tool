from abc import ABC, abstractmethod
import queue
import time
import threading


class ITransport(ABC):
    def __init__(self):
        self._connected = False
        self._receive_thread = None
        self.receive_queue = queue.Queue()

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def send_data(self, data: bytes) -> bool:
        pass

    @abstractmethod
    def receive_data(self) -> bytes | None:
        pass

    def is_connected(self) -> bool:
        return self._connected

    def start_receiving(self):
        if not self._receive_thread or not self._receive_thread.is_alive():
            self._receive_thread = threading.Thread(
                target=self._receive_loop, daemon=True
            )
            self._receive_thread.start()

    def _receive_loop(self):
        while self._connected:
            try:
                data = self.receive_data()
                if data:
                    self.receive_queue.put(data)
            except Exception as e:
                print(f"Error in receive loop: {e}")
                self._connected = False
            time.sleep(0.01)  # 避免 CPU 占用过高

    def _emit_data(self, data: bytes):
        print(data)
