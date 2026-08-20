from nltk.corpus import wordnet as wn

MAX_DEFINITIONS_PER_POS = 3

POS_MAP = {
    'n': 'noun',
    'v': 'verb',
    'a': 'adjective',
    's': 'adjective',  # WordNet's "satellite adjective" - treat as adjective
    'r': 'adverb'
}


def clean_word(text):
    """Strip whitespace/newlines, keep only the first word, strip punctuation, lowercase it."""
    if not text:
        return ""
    text = text.strip()
    parts = text.split()
    if not parts:
        return ""
    word = parts[0]
    return word.strip(".,;:!?\"'()[]{}").lower()


def fetch_word_data_offline(word):
    """
    Look up a word in WordNet.
    Returns {"word": ..., "meanings": [...]} or None if not found.
    """
    word = clean_word(word)
    if not word:
        return None

    synsets = wn.synsets(word)
    if not synsets:
        return None

    grouped = {}
    for syn in synsets:
        pos_label = POS_MAP.get(syn.pos())
        if not pos_label:
            continue
        grouped.setdefault(pos_label, [])
        if len(grouped[pos_label]) >= MAX_DEFINITIONS_PER_POS:
            continue
        examples = syn.examples()
        grouped[pos_label].append({
            "definition": syn.definition(),
            "example": examples[0] if examples else ""
        })

    if not grouped:
        return None

    meanings = [
        {"part_of_speech": pos_label, "definitions": defs}
        for pos_label, defs in grouped.items()
    ]

    return {"word": word, "meanings": meanings}


if __name__ == "__main__":
    import json
    result = fetch_word_data_offline("hello")
    print(json.dumps(result, indent=2))