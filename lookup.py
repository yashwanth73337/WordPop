import socket

from dictionary_local import fetch_word_data_offline, clean_word
from dictionary_api import fetch_word_data as fetch_word_data_online
from pronunciation import get_pronunciation
from word_forms import get_verb_forms, get_adjective_forms

CONNECTIVITY_CHECK_TIMEOUT = 1.0  # seconds


def has_internet():
    """Fast check: can we actually reach the internet right now?"""
    try:
        socket.setdefaulttimeout(CONNECTIVITY_CHECK_TIMEOUT)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except OSError:
        return False


def _attach_forms(word, meanings):
    """Adds V1-V4 forms to verb meanings, and comparative/superlative to adjective meanings."""
    for meaning in meanings:
        pos = meaning.get("part_of_speech", "").lower()
        if pos == "verb":
            meaning["forms"] = get_verb_forms(word)
        elif pos == "adjective":
            forms = get_adjective_forms(word)
            if forms["comparative"] or forms["superlative"]:
                meaning["forms"] = forms
    return meanings


def lookup_word(raw_text):
    """
    Full lookup: cleans the input, then:
      - if internet is reachable: tries the online API first (richer definitions),
        falls back to offline WordNet only if the word isn't found online.
      - if no internet: goes straight to offline WordNet, no waiting.
    Pronunciation always comes from the offline CMU dictionary either way.
    Verb/adjective meanings get V1-V4 or comparative/superlative forms attached.
    """
    word = clean_word(raw_text)
    if not word:
        return None

    result = None
    source = None

    if has_internet():
        result = fetch_word_data_online(word)
        source = "online" if result else None

        if result is None:
            result = fetch_word_data_offline(word)
            source = "offline" if result else None
    else:
        result = fetch_word_data_offline(word)
        source = "offline" if result else None

    if result is None:
        return None

    meanings = _attach_forms(word, result.get("meanings", []))

    return {
        "word": result.get("word", word),
        "pronunciation": get_pronunciation(word),
        "meanings": meanings,
        "source": source
    }


if __name__ == "__main__":
    import json
    for w in ["go", "good", "hello"]:
        print(f"\n--- {w} ---")
        print(json.dumps(lookup_word(w), indent=2))