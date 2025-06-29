import websocket
import threading
import json
import time
import logging

class OrderBookWebSocketClient:
    def __init__(self, url, symbol, on_message_callback):
        self.url = url
        self.symbol = symbol
        self.on_message_callback = on_message_callback
        self.ws = None
        self.thread = None
        self.running = False
        self.last_latency = None

    def _on_message(self, ws, message):
        start_time = time.time()
        try:
            data = json.loads(message)
            if data.get("symbol") == self.symbol:
                self.on_message_callback(data)
        except Exception as e:
            logging.error(f"Error parsing message: {e}")
        finally:
            self.last_latency = time.time() - start_time

    def _on_error(self, ws, error):
        logging.error(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        logging.info("WebSocket closed")

    def _on_open(self, ws):
        logging.info("WebSocket connection opened")

    def start(self):
        self.running = True
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()

    def get_last_latency(self):
        return self.last_latency