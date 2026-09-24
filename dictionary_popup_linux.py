import logging
import os
import socket
import threading
import tkinter as tk

from lookup import lookup_word
from popup_ui import create_popup_window
from primary_selection import get_primary_selection

SOCKET_PATH = "/tmp/wordpop.sock"

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordpop.log")
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def handle_trigger(root):
    """Runs when a trigger signal comes in. Does the lookup on a background
    thread (so it doesn't block the socket listener), then safely hands the
    result back to the main thread to actually build the popup."""
    def do_lookup():
        selected_text = get_primary_selection()
        if not selected_text or not selected_text.strip():
            root.after(0, lambda: create_popup_window(root, None))
            return
        data = lookup_word(selected_text)
        root.after(0, lambda: create_popup_window(root, data))

    threading.Thread(target=do_lookup, daemon=True).start()


def socket_listener(root):
    """Runs on its own thread. Listens for trigger signals from trigger.py
    and hands each one off to handle_trigger."""
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(1)
    logging.info(f"Listening on {SOCKET_PATH}")

    while True:
        conn, _ = server.accept()
        conn.close()
        handle_trigger(root)


def main():
    root = tk.Tk()
    root.withdraw()  # persistent hidden controller window, same pattern as Windows

    listener_thread = threading.Thread(target=socket_listener, args=(root,), daemon=True)
    listener_thread.start()

    logging.info("WordPop (Linux) started")
    root.mainloop()


if __name__ == "__main__":
    main()