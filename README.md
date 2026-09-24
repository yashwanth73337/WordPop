# WordPop

A lightweight background utility that gives you instant word definitions — highlight any word in any application (browser, PDF reader, text editor, etc.), press **Ctrl+M**, and a popup shows you the definition, pronunciation, part of speech, and examples — right there, without switching apps or opening a browser tab.

Works fully offline by default. If you're connected to the internet, it automatically tries an online dictionary first for richer definitions, and falls back to its offline database if that fails — so it never leaves you stuck, on a flight or with a dead connection.

Supports **Windows 10/11** and **Ubuntu (GNOME, X11 session)**.

## Who this is for

- Anyone who reads a lot on their PC — articles, PDFs, research papers, books — and wants quick definitions without breaking focus.
- Best suited for general English vocabulary. It's built on WordNet (a well-established, freely available lexical database), so common and academic words are covered well. Highly specialized jargon (e.g. cutting-edge technical/scientific terms) may not always be found — no general dictionary, online or offline, covers that kind of vocabulary reliably.

## Features

- **Global hotkey (Ctrl+M)** — works in any application, not just specific ones
- **Offline-first** — uses WordNet + CMU Pronouncing Dictionary, no internet required for everyday words
- **Online fallback** — automatically tries a live dictionary API first when you're connected, for richer definitions
- **Pronunciation** — both IPA (`/həˈloʊ/`) and a plain-English simplified respelling (`huh-LOH`)
- **All parts of speech** — noun, verb, adjective, adverb, etc., each with up to 3 definitions and an example
- **Verb forms (V1–V4)** — base, past simple, past participle, and -ing form, shown automatically for verbs
- **Comparative/superlative** — shown automatically for adjectives that genuinely have them (e.g. good → better → best)
- **Draggable popup** — click and drag the title to reposition it anywhere on screen
- **Selectable text** — click-drag to highlight any part of the definition and copy it (Ctrl+C)
- **Runs silently in the background**
- **Auto-start** — launches automatically when you log in

---

## Windows Setup

### Requirements

- Windows 10 or 11
- Python 3.9 or newer ([python.org](https://www.python.org/downloads/))
- An internet connection **only** for the one-time setup below (downloading dependencies and offline dictionary data). After that, the tool itself works fully offline.

### 1. Clone the repository

```
git clone https://github.com/yashwanth73337/WordPop.git
cd WordPop
```

### 2. Create and activate a virtual environment

```
python -m venv wordpop-env
wordpop-env\Scripts\activate
```

Your terminal prompt should now start with `(wordpop-env)`.

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Download the offline dictionary data (one-time only)

```
python -m nltk.downloader wordnet omw-1.4 cmudict
```

### 5. Test it

```
pythonw dictionary_popup.py
```

Check your system tray (bottom-right, click the `^` arrow if hidden) for a small "W" icon. Select any word in any app and press **Ctrl+M** — a popup should appear. Right-click the tray icon and choose **Quit WordPop** when you're done testing.

### 6. (Optional) Run automatically at startup

```
python install_startup.py
```

**Important:** this only takes effect on your *next* login — it won't launch WordPop immediately. To start it right now, run `pythonw dictionary_popup.py` directly.

To undo this later:

```
python uninstall_startup.py
```

---

## Ubuntu / Linux Setup

**Currently supported: GNOME desktop on an X11 session.** GNOME on Wayland uses a different (more restricted) mechanism for reading text selections and hasn't been set up yet — if you're on Wayland, check back or open an issue. To check which you have:

```
echo $XDG_CURRENT_DESKTOP
echo $XDG_SESSION_TYPE
```

### Requirements

- Ubuntu with GNOME on X11
- Python 3.9 or newer (usually pre-installed)
- `sudo` access, for installing one small system package

### 1. Install xclip

This lets WordPop read your text selection:

```
sudo apt update
sudo apt install xclip
```

### 2. Clone the repository

```
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/yashwanth73337/WordPop.git
cd WordPop
```

### 3. Create and activate a virtual environment

```
python3 -m venv wordpop-env
source wordpop-env/bin/activate
```

Your terminal prompt should now start with `(wordpop-env)`.

### 4. Install dependencies

Linux uses a separate, smaller dependency list (no hotkey library or tray icon library needed — see [How it's different on Linux](#how-its-different-on-linux) below):

```
pip install -r requirements-linux.txt
```

### 5. Download the offline dictionary data (one-time only)

```
python3 -m nltk.downloader wordnet omw-1.4 cmudict
```

If you see a warning about `nltk_data` being "world- or group-writable," tighten its permissions:

```
chmod -R go-w ~/nltk_data
```

### 6. Test it

In one terminal, start the background process:

```
python3 dictionary_popup_linux.py
```

It should run silently with no output — that's expected. Leave it running. In a second terminal (with the venv activated the same way), select a word somewhere and run:

```
python3 trigger.py
```

A popup should appear. Press `Ctrl+C` in the first terminal to stop it when you're done testing.

### 7. Bind Ctrl+M as a system shortcut

Get the exact command to use, from inside the project folder with the venv active:

```
echo "$(pwd)/wordpop-env/bin/python3 $(pwd)/trigger.py"
```

Then: **Settings → Keyboard → Keyboard Shortcuts → View and Customize Shortcuts → Custom Shortcuts → +**

- **Name:** `WordPop Lookup`
- **Command:** the output from the `echo` command above
- **Shortcut:** Ctrl+M

With `dictionary_popup_linux.py` still running (from step 6), select a word and press **Ctrl+M** directly — no need to run `trigger.py` manually anymore.

### 8. (Optional) Run automatically at login

```
mkdir -p ~/.config/autostart
nano ~/.config/autostart/wordpop.desktop
```

Paste in (replace `/home/yourusername` with your actual home path — check with `echo $HOME`):

```
[Desktop Entry]
Type=Application
Name=WordPop
Exec=/home/yourusername/Projects/WordPop/wordpop-env/bin/python3 /home/yourusername/Projects/WordPop/dictionary_popup_linux.py
X-GNOME-Autostart-enabled=true
NoDisplay=true
```

Save (`Ctrl+O`, Enter, `Ctrl+X`). This takes effect on your next login. To remove it later, delete that file.

### How it's different on Linux

Windows and Linux need genuinely different mechanisms for a few things, so a handful of files are platform-specific:

- **No hotkey library.** Windows needs the `keyboard` library to catch a global hotkey; on Linux that requires root. Instead, GNOME's own Custom Shortcut feature runs `trigger.py`, which just signals the background process over a local socket.
- **No simulated copy.** Windows has to simulate Ctrl+C to grab your selection. Linux/X11 automatically tracks whatever you've selected (the "primary selection"), readable directly via `xclip` — no keypress simulation needed.
- **No tray icon.** GNOME doesn't support tray icons without installing an extra extension, so the Linux version skips it and just runs invisibly in the background.

Everything else — the actual dictionary lookup, offline/online fallback, pronunciation, popup rendering, verb/adjective forms — is shared, unmodified code used by both platforms.

---

## How to use it

1. Select/highlight a word in any application.
2. Press **Ctrl+M**.
3. A popup appears in the top-right of your screen with the word's pronunciation, part of speech, definitions, and examples.
4. Click and drag the word title to move the popup anywhere.
5. Click and drag inside the definition text to select it, then Ctrl+C to copy.
6. Click the **✕** to close the popup.
7. **Windows:** right-click the tray icon and choose **Quit WordPop** to stop it. **Linux:** `Ctrl+C` in the terminal running `dictionary_popup_linux.py`, or `pkill -f dictionary_popup_linux.py`.

## Project structure

| File | Purpose | Platform |
|---|---|---|
| `lookup.py` | Coordinates offline/online lookup and attaches pronunciation + word forms | Both |
| `dictionary_local.py` | Offline definitions via WordNet | Both |
| `dictionary_api.py` | Online fallback via a free dictionary API | Both |
| `pronunciation.py` | Converts CMU dictionary data into IPA and simplified respellings | Both |
| `word_forms.py` | Generates verb forms (V1–V4) and adjective comparative/superlative forms | Both |
| `popup_ui.py` | Builds and displays the popup window | Both |
| `dictionary_popup.py` | Main entry point — hotkey listener, tray icon, background orchestration | Windows |
| `install_startup.py` | Adds WordPop to Windows Startup | Windows |
| `uninstall_startup.py` | Removes WordPop from Windows Startup | Windows |
| `requirements.txt` | Python dependencies | Windows |
| `dictionary_popup_linux.py` | Main entry point — socket listener, background orchestration | Linux |
| `primary_selection.py` | Reads the X11 primary selection via xclip | Linux |
| `trigger.py` | Signals the background process to do a lookup; bound to Ctrl+M via GNOME | Linux |
| `requirements-linux.txt` | Python dependencies | Linux |

## Troubleshooting

**Windows:**
- **Nothing happens when I press Ctrl+M** — WordPop only responds while it's running in the background. Check your system tray for the "W" icon; if missing, start it with `pythonw dictionary_popup.py`. Also confirm only one copy is running (Task Manager → Details → search `python`).
- **Something seems broken and I can't tell why** — check `wordpop.log` in the project folder.

**Linux:**
- **Ctrl+M does nothing** — confirm `dictionary_popup_linux.py` is actually running (`ps aux | grep dictionary_popup_linux`), and that the Custom Shortcut command path is exactly correct (typos in the venv path are the most common cause).
- **`trigger.py` says "WordPop isn't running"** — start `dictionary_popup_linux.py` first, in a terminal or via `~/.config/autostart`.
- **Wayland** — not currently supported; check `echo $XDG_SESSION_TYPE`.

**Both:**
- **A word isn't found** — WordPop tries the online API first (if connected), then falls back to WordNet. If a word genuinely isn't in either, you'll see "No definition found." More likely for slang, brand-new terms, or narrow technical jargon.

## Limitations

- Simplified pronunciation respellings are auto-generated from phonetic data and, while accurate for the vast majority of words, may occasionally sound slightly off for unusual words.
- Some words have multiple valid pronunciations (e.g. "research" as a noun vs. verb) — only one is shown.
- Coverage is strongest for general and academic English; highly specialized or very new terms may not be found.
- Linux support currently requires GNOME on X11; other desktop environments and Wayland aren't set up yet.

## License

MIT — free to use, modify, and share.