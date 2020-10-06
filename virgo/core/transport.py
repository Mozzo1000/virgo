import selectors
import json
import io


def set_selector_events_mask(self, mode):
    """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
    if mode == "r":
        events = selectors.EVENT_READ
    elif mode == "w":
        events = selectors.EVENT_WRITE
    elif mode == "rw":
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
    else:
        raise ValueError(f"Invalid events mask mode {repr(mode)}.")
    self.selector.modify(self.sock, events, data=self)


def read_socket(self):
    try:
        # Should be ready to read
        data = self.sock.recv(4096)
    except BlockingIOError:
        # Resource temporarily unavailable (errno EWOULDBLOCK)
        pass
    else:
        if data:
            self._recv_buffer += data
        else:
            raise RuntimeError("Peer closed.")


def write_socket(self, isserver=False):
    if self._send_buffer:
        print("sending", repr(self._send_buffer), "to", self.addr)
        try:
            # Should be ready to write
            sent = self.sock.send(self._send_buffer)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            self._send_buffer = self._send_buffer[sent:]
            # Close when the buffer is drained. The response has been sent.
            if isserver and sent and not self._send_buffer:
                self.close()


def json_encode(obj, encoding):
    return json.dumps(obj, ensure_ascii=False).encode(encoding)


def json_decode(json_bytes, encoding):
    tiow = io.TextIOWrapper(
        io.BytesIO(json_bytes), encoding=encoding, newline=""
    )
    obj = json.load(tiow)
    tiow.close()
    return obj

def close_socket(self):
    print("closing connection to", self.addr)
    try:
        self.selector.unregister(self.sock)
    except Exception as e:
        print(
            "error: selector.unregister() exception for",
            f"{self.addr}: {repr(e)}",
        )

    try:
        self.sock.close()
    except OSError as e:
        print(
            "error: socket.close() exception for",
            f"{self.addr}: {repr(e)}",
        )
    finally:
        # Delete reference to socket object for garbage collection
        self.sock = None