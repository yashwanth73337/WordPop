import sys
import tkinter as tk
import logging

POPUP_WIDTH = 380
BG_COLOR = "#1e1e1e"
FG_COLOR = "#f2f2f2"
ACCENT_COLOR = "#8ab4f8"
MUTED_COLOR = "#a0a0a0"
CLOSE_COLOR = "#ff6b6b"

MARGIN_TOP = 120
MARGIN_RIGHT = 40

_dpi_aware_done = False


def _make_dpi_aware():
    global _dpi_aware_done
    if _dpi_aware_done or sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass
    _dpi_aware_done = True


def create_popup_window(parent, data):
    """
    Creates and shows one popup as a child (Toplevel) of the persistent root window,
    fixed near the top-right corner of the screen.
    IMPORTANT: must only ever be called from the main thread.
    """
    _make_dpi_aware()

    win = tk.Toplevel(parent)
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.configure(bg=BG_COLOR)

    outer = tk.Frame(win, bg=BG_COLOR, padx=14, pady=12,
                      highlightthickness=1, highlightbackground="#3a3a3a")
    outer.pack(fill="both", expand=True)

    header = tk.Frame(outer, bg=BG_COLOR)
    header.pack(fill="x")

    title_text = data["word"] if data else "WordPop"
    word_label = tk.Label(header, text=title_text, bg=BG_COLOR, fg=FG_COLOR,
                           font=("Segoe UI", 16 if data else 14, "bold"),
                           cursor="fleur")
    word_label.pack(side="left")

    close_btn = tk.Label(header, text="✕", bg=BG_COLOR, fg=CLOSE_COLOR,
                          font=("Segoe UI", 12, "bold"), cursor="hand2")
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", lambda e: win.destroy())

    drag_data = {"x": 0, "y": 0}

    def start_drag(event):
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def do_drag(event):
        new_x = win.winfo_x() + (event.x - drag_data["x"])
        new_y = win.winfo_y() + (event.y - drag_data["y"])
        win.geometry(f"+{new_x}+{new_y}")

    header.bind("<ButtonPress-1>", start_drag)
    header.bind("<B1-Motion>", do_drag)
    word_label.bind("<ButtonPress-1>", start_drag)
    word_label.bind("<B1-Motion>", do_drag)

    text_widget = tk.Text(
        outer, bg=BG_COLOR, fg=FG_COLOR, bd=0, highlightthickness=0,
        wrap="word", width=44, font=("Segoe UI", 10),
        cursor="xterm", padx=0, pady=0,
        selectbackground="#3a5a8a", selectforeground="#ffffff"
    )
    text_widget.pack(fill="both", expand=True, pady=(8, 0))

    text_widget.tag_configure("pron", foreground=ACCENT_COLOR, font=("Segoe UI", 10))
    text_widget.tag_configure("pos", foreground=MUTED_COLOR, font=("Segoe UI", 10, "italic"))
    text_widget.tag_configure("def", foreground=FG_COLOR, font=("Segoe UI", 10))
    text_widget.tag_configure("example", foreground=MUTED_COLOR, font=("Segoe UI", 9, "italic"))
    text_widget.tag_configure("source", foreground=MUTED_COLOR, font=("Segoe UI", 8))
    text_widget.tag_configure("empty", foreground=FG_COLOR, font=("Segoe UI", 11))
    text_widget.tag_configure("forms", foreground=ACCENT_COLOR, font=("Segoe UI", 9, "bold"))

    if data is None:
        text_widget.insert("end", "No definition found.", "empty")
    else:
        pron = data.get("pronunciation")
        if pron:
            text_widget.insert("end", f'{pron["ipa"]}   ·   {pron["simple"]}\n\n', "pron")

        for meaning in data.get("meanings", []):
            text_widget.insert("end", f'{meaning["part_of_speech"]}\n', "pos")
            for i, d in enumerate(meaning["definitions"], start=1):
                text_widget.insert("end", f'{i}. {d["definition"]}\n', "def")
                if d.get("example"):
                    text_widget.insert("end", f'   "{d["example"]}"\n', "example")

            forms = meaning.get("forms")
            if forms:
                if "v1" in forms:
                    forms_line = f'V1: {forms["v1"]}   V2: {forms["v2"]}   V3: {forms["v3"]}   V4: {forms["v4"]}'
                    text_widget.insert("end", f'{forms_line}\n', "forms")
                elif forms.get("comparative") or forms.get("superlative"):
                    parts = []
                    if forms.get("comparative"):
                        parts.append(f'comparative: {forms["comparative"]}')
                    if forms.get("superlative"):
                        parts.append(f'superlative: {forms["superlative"]}')
                    text_widget.insert("end", f'{"   ·   ".join(parts)}\n', "forms")

            text_widget.insert("end", "\n")

        if data.get("source") == "online":
            text_widget.insert("end", "(via online fallback)", "source")

    text_widget.configure(state="disabled")

    win.update_idletasks()

    counted = text_widget.count("1.0", "end", "displaylines")
    line_count = counted[0] if counted else 10
    line_count = max(2, min(line_count, 30))
    text_widget.configure(height=line_count)

    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()

    x = screen_w - width - MARGIN_RIGHT
    y = MARGIN_TOP

    logging.info(f"Placing popup: x={x} y={y} width={width} height={height} screen_w={screen_w} screen_h={screen_h}")
    win.geometry(f"{width}x{height}+{x}+{y}")
    return win