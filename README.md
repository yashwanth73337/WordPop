# WordPop

A lightweight Windows background utility that gives you instant word definitions — highlight any word in any application (browser, PDF reader, Word, etc.), press **Ctrl+M**, and a popup shows you the definition, pronunciation, part of speech, and examples — right there, without switching apps or opening a browser tab.

Works fully offline by default. If you're connected to the internet, it automatically tries an online dictionary first for richer definitions, and falls back to its offline database if that fails — so it never leaves you stuck, on a flight or with a dead connection.

## Who this is for

- Anyone who reads a lot on their Windows PC — articles, PDFs, research papers, books — and wants quick definitions without breaking focus.
- Best suited for general English vocabulary. It's built on WordNet (a well-established, freely available lexical database), so common and academic words are covered well. Highly specialized jargon (e.g. cutting-edge technical/scientific terms) may not always be found — no general dictionary, online or offline, covers that kind of vocabulary reliably.
- Windows 10/11 only (it relies on Windows-specific APIs for the hotkey and cursor position).

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
- **Runs silently in the background** — lives in your system tray, no console window
- **Optional auto-start** — can be set to launch automatically when you log into Windows

## Requirements

- Windows 10 or 11
- Python 3.9 or newer ([python.org](https://www.python.org/downloads/))
- An internet connection **only** for the one-time setup below (downloading dependencies and offline dictionary data). After that, the tool itself works fully offline.

## Setup

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

This downloads WordNet (definitions) and the CMU Pronouncing Dictionary (pronunciation) to your computer — about 35MB, one-time only. After this, no internet is needed for lookups.

```
python -m nltk.downloader wordnet omw-1.4 cmudict
```

### 5. Test it

```
pythonw dictionary_popup.py
```

Check your system tray (bottom-right, click the `^` arrow if hidden) for a small "W" icon. Select any word in any app and press **Ctrl+M** — a popup should appear. Right-click the tray icon and choose **Quit WordPop** when you're done testing.

### 6. (Optional) Run automatically at startup

If you want WordPop to launch automatically every time you log into Windows:

```
python install_startup.py
```

To undo this later:

```
python uninstall_startup.py
```

## How to use it

1. Select/highlight a word in any application.
2. Press **Ctrl+M**.
3. A popup appears in the top-right of your screen with the word's pronunciation, part of speech, definitions, and examples.
4. Click and drag the word title to move the popup anywhere.
5. Click and drag inside the definition text to select it, then Ctrl+C to copy.
6. Click the **✕** to close the popup.
7. To fully stop WordPop, right-click its tray icon and choose **Quit WordPop**.

## Project structure

| File | Purpose |
|---|---|
| `dictionary_popup.py` | Main entry point — hotkey listener, tray icon, background orchestration |
| `popup_ui.py` | Builds and displays the popup window |
| `lookup.py` | Coordinates offline/online lookup and attaches pronunciation + word forms |
| `dictionary_local.py` | Offline definitions via WordNet |
| `dictionary_api.py` | Online fallback via a free dictionary API |
| `pronunciation.py` | Converts CMU dictionary data into IPA and simplified respellings |
| `word_forms.py` | Generates verb forms (V1–V4) and adjective comparative/superlative forms |
| `install_startup.py` | Adds WordPop to Windows Startup |
| `uninstall_startup.py` | Removes WordPop from Windows Startup |
| `requirements.txt` | Python dependencies |

## Troubleshooting

- **Nothing happens when I press Ctrl+M** — make sure WordPop is actually running (check the system tray). Also check that only one copy is running — WordPop refuses to start a second instance, but if you're unsure, open Task Manager → Details tab and confirm there's only one `python.exe`/`pythonw.exe` for WordPop.
- **Something seems broken and I can't tell why** — check `wordpop.log`, created automatically in the project folder. It logs errors that would otherwise be silent (since `pythonw.exe` shows no console window).
- **A word isn't found** — WordPop tries the online API first (if connected), then falls back to WordNet. If a word genuinely isn't in either, you'll see "No definition found." This is more likely for slang, brand-new terms, or narrow technical jargon.

## Limitations

- Simplified pronunciation respellings are auto-generated from phonetic data and, while accurate for the vast majority of words, may occasionally sound slightly off for unusual words.
- Some words have multiple valid pronunciations (e.g. "research" as a noun vs. verb) — only one is shown.
- Coverage is strongest for general and academic English; highly specialized or very new terms may not be found.

## License

MIT — free to use, modify, and share.