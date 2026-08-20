import requests

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"
MAX_DEFINITIONS_PER_POS = 3


def clean_word(text):
    """Strip whitespace/newlines, keep only the first word, strip surrounding punctuation."""
    if not text:
        return ""
    text = text.strip()
    parts = text.split()
    if not parts:
        return ""
    word = parts[0]
    return word.strip(".,;:!?\"'()[]{}")


def fetch_word_data(word):
    """
    Look up a word using the online Free Dictionary API (fallback only).
    Returns {"word": ..., "meanings": [...]} or None if not found/error/offline.
    """
    word = clean_word(word)
    if not word:
        return None

    try:
        response = requests.get(API_URL.format(word), timeout=5)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except ValueError:
        return None

    if not isinstance(data, list) or not data:
        return None

    entry = data[0]

    meanings = []
    for meaning in entry.get("meanings", []):
        part_of_speech = meaning.get("partOfSpeech", "")
        definitions = []
        for d in meaning.get("definitions", [])[:MAX_DEFINITIONS_PER_POS]:
            definitions.append({
                "definition": d.get("definition", ""),
                "example": d.get("example", "")
            })
        if part_of_speech and definitions:
            meanings.append({
                "part_of_speech": part_of_speech,
                "definitions": definitions
            })

    return {
        "word": entry.get("word", word),
        "meanings": meanings
    }


if __name__ == "__main__":
    import json
    result = fetch_word_data("hello")
    print(json.dumps(result, indent=2))