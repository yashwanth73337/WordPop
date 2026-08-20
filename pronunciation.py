from nltk.corpus import cmudict

_pron_dict = cmudict.dict()

# ARPAbet -> IPA (rough General American mapping)
IPA_MAP = {
    'AA': 'ɑ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔ', 'AW': 'aʊ', 'AY': 'aɪ',
    'EH': 'ɛ', 'ER': 'ɝ', 'EY': 'eɪ', 'IH': 'ɪ', 'IY': 'i', 'OW': 'oʊ',
    'OY': 'ɔɪ', 'UH': 'ʊ', 'UW': 'u',
    'B': 'b', 'CH': 'tʃ', 'D': 'd', 'DH': 'ð', 'F': 'f', 'G': 'g',
    'HH': 'h', 'JH': 'dʒ', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n',
    'NG': 'ŋ', 'P': 'p', 'R': 'r', 'S': 's', 'SH': 'ʃ', 'T': 't',
    'TH': 'θ', 'V': 'v', 'W': 'w', 'Y': 'j', 'Z': 'z', 'ZH': 'ʒ'
}

# ARPAbet -> plain-English respelling
SIMPLE_MAP = {
    'AA': 'ah', 'AE': 'a', 'AH': 'uh', 'AO': 'aw', 'AW': 'ow', 'AY': 'eye',
    'EH': 'eh', 'ER': 'er', 'EY': 'ay', 'IH': 'ih', 'IY': 'ee', 'OW': 'oh',
    'OY': 'oy', 'UH': 'uu', 'UW': 'oo',
    'B': 'b', 'CH': 'ch', 'D': 'd', 'DH': 'th', 'F': 'f', 'G': 'g',
    'HH': 'h', 'JH': 'j', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n',
    'NG': 'ng', 'P': 'p', 'R': 'r', 'S': 's', 'SH': 'sh', 'T': 't',
    'TH': 'th', 'V': 'v', 'W': 'w', 'Y': 'y', 'Z': 'z', 'ZH': 'zh'
}


def _is_vowel(phone):
    return phone[-1].isdigit()


def _syllabify(phones):
    """Group ARPAbet phones into syllables, one vowel per syllable (onset-maximizing)."""
    syllables = []
    current = []
    for ph in phones:
        current.append(ph)
        if _is_vowel(ph):
            syllables.append(current)
            current = []
    if current:
        if syllables:
            syllables[-1].extend(current)
        else:
            syllables.append(current)
    return syllables


def _ipa_for_syllable(syll):
    text, stress_mark = "", ""
    for ph in syll:
        if _is_vowel(ph):
            base, stress = ph[:-1], ph[-1]
            symbol = IPA_MAP.get(base, base.lower())
            if base == 'AH' and stress == '0':
                symbol = 'ə'
            elif base == 'ER' and stress == '0':
                symbol = 'ɚ'
            if stress == '1':
                stress_mark = 'ˈ'
            elif stress == '2':
                stress_mark = 'ˌ'
            text += symbol
        else:
            text += IPA_MAP.get(ph, ph.lower())
    return stress_mark + text


def _simple_for_syllable(syll):
    text, stressed = "", False
    for ph in syll:
        if _is_vowel(ph):
            base, stress = ph[:-1], ph[-1]
            text += SIMPLE_MAP.get(base, base.lower())
            if stress == '1':
                stressed = True
        else:
            text += SIMPLE_MAP.get(ph, ph.lower())
    return text.upper() if stressed else text


def get_pronunciation(word):
    """Returns {"ipa": "/.../", "simple": "huh-LOH"} or None if not in cmudict."""
    word = word.strip().lower()
    entries = _pron_dict.get(word)
    if not entries:
        return None

    phones = entries[0]
    syllables = _syllabify(phones)

    ipa = "/" + "".join(_ipa_for_syllable(s) for s in syllables) + "/"
    simple = "-".join(_simple_for_syllable(s) for s in syllables)

    return {"ipa": ipa, "simple": simple}


if __name__ == "__main__":
    for w in ["hello", "research", "photosynthesis"]:
        print(w, "->", get_pronunciation(w))