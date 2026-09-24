import subprocess


def get_primary_selection():
    """
    Reads whatever text is currently selected (X11's 'primary selection') —
    this is automatic on Linux the moment you select text, no Ctrl+C needed.
    Returns the raw selected text, or None if nothing is selected / xclip fails.
    """
    try:
        result = subprocess.run(
            ["xclip", "-o", "-selection", "primary"],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode != 0:
            return None
        return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


if __name__ == "__main__":
    text = get_primary_selection()
    print(f"Current selection: {text!r}")