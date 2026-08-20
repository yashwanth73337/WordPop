import logging
import os
import queue
import socket
import threading
import time
import tkinter as tk

import keyboard
import pyperclip
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

from lookup import lookup_word
from popup_ui import create_popup_window, _make_dpi_aware

HOTKEY = "ctrl+m"
POLL_INTERVAL_MS = 100
LOCK_PORT = 51837  # arbitrary local port, used only to detect a second instance

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordpop.log")
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

result_queue = queue.Queue()
stop_event = threading.Event()


def _acquire_single_instance_lock():
    """Prevents a second copy of WordPop from ever running at the same time —
    this is what caused the clipboard/hotkey conflicts earlier."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", LOCK_PORT))
    except OSError:
        return None
    return sock  # kept alive for the program's lifetime; the port stays held until it exits


def handle_lookup():
    """Runs on a background thread. Never touches Tkinter directly."""
    try:
        old_clipboard = None
        try:
            old_clipboard = pyperclip.paste()
        except Exception:
            pass

        pyperclip.copy("")

        # Release the physical hotkey combo before simulating Ctrl+C,
        # so the keyboard library doesn't get confused about which keys are still down.
        keyboard.release("m")
        keyboard.release("ctrl")
        time.sleep(0.05)

        keyboard.send("ctrl+c")
        time.sleep(0.15)

        selected_text = pyperclip.paste()

        try:
            if old_clipboard is not None:
                pyperclip.copy(old_clipboard)
        except Exception:
            pass

        if not selected_text or not selected_text.strip():
            result_queue.put(None)
            return

        data = lookup_word(selected_text)
        result_queue.put(data)
        logging.info(f"Lookup succeeded for: {selected_text.strip()[:50]}")

    except Exception:
        logging.exception("Error in handle_lookup")
        result_queue.put(None)


def on_hotkey():
    threading.Thread(target=handle_lookup, daemon=True).start()


def create_tray_icon():
    image = Image.new("RGB", (64, 64), color="#1e1e1e")
    draw = ImageDraw.Draw(image)
    draw.rectangle([4, 4, 60, 60], outline="#8ab4f8", width=3)
    draw.text((22, 18), "W", fill="#8ab4f8")

    def on_quit(icon, item):
        icon.stop()
        stop_event.set()

    menu = Menu(MenuItem("Quit WordPop", on_quit))
    return Icon("WordPop", image, "WordPop", menu)


def poll_queue(root):
    try:
        while True:
            data = result_queue.get_nowait()
            try:
                create_popup_window(root, data)
            except Exception:
                logging.exception("Error creating popup window")
    except queue.Empty:
        pass

    if stop_event.is_set():
        root.quit()
        return

    root.after(POLL_INTERVAL_MS, poll_queue, root)


def main():
    lock = _acquire_single_instance_lock()
    if lock is None:
        logging.info("Another instance of WordPop is already running. Exiting.")
        return

    _make_dpi_aware()  # MUST happen before any Tk window is created

    root = tk.Tk()
    root.withdraw()

    keyboard.add_hotkey(HOTKEY, on_hotkey)

    icon = create_tray_icon()
    threading.Thread(target=icon.run, daemon=True).start()

    logging.info("WordPop started")
    root.after(POLL_INTERVAL_MS, poll_queue, root)
    root.mainloop()


if __name__ == "__main__":
    main()