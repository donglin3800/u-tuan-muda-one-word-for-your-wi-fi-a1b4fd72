"""One Word for Your Wi-Fi: Clickbait.

The word is the whole entry. My Wi-Fi promises full bars and then
delivers nothing, exactly like a clickbait headline promises a story
and delivers nothing. You click, you wait, nothing loads.

This program writes that one word to /output/entry.txt, exactly as
the gate requires: UTF-8 text, 1 to 20 characters, a single word with
no whitespace and no trailing newline, so the file holds 9 bytes.
"""

import sys
from pathlib import Path

WORD = "Clickbait"

OUTPUT_PATH = "/output/entry.txt"
LOCAL_FALLBACK = "output/entry.txt"


def check_word(word):
    """Refuse anything that would fail the gate before writing it."""
    if not 1 <= len(word) <= 20:
        raise ValueError("entry must be 1 to 20 characters")
    if word != word.strip() or any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word with no whitespace")
    if not word.isalpha():
        raise ValueError("entry must be letters only")
    return word


def write_entry(word, path=OUTPUT_PATH):
    """Write the word with no trailing newline, then read it back.

    The grader reads /output/entry.txt, so that path is tried first.
    If it cannot be written (a local run without a writable /output),
    fall back to ./output/entry.txt and say so, instead of crashing.
    """
    target = Path(path)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(word, encoding="utf-8")
    except OSError:
        target = Path(LOCAL_FALLBACK)
        print(f"warning: {path} not writable, using {target}", file=sys.stderr)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(word, encoding="utf-8")
    if target.read_text(encoding="utf-8") != word:
        raise RuntimeError("entry on disk does not match the word")
    return target


def main():
    word = check_word(WORD)
    target = write_entry(word)
    print(f"Wrote {word!r} to {target}")


if __name__ == "__main__":
    main()
