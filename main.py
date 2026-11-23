#!/usr/bin/env python3
"""One-Line Roast: The Gadget You Use Every Day.

Writes a single original roast line to /output/entry.txt.
Pure Python stdlib only. The gate guard enforces the competition
gate: UTF-8 text of 1 to 200 characters, exactly one line, not
only whitespace.
"""

import os
import sys

ENTRY = (
    "My earbuds cut out mid-sentence, so my phone has "
    "ghosted more people than I ever have."
)

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def gate_guard(text):
    """Validate the entry against the competition gate.

    Returns a list of problems (empty when the entry is valid).
    """
    problems = []
    if not isinstance(text, str):
        problems.append("entry is not text")
        return problems
    if not (1 <= len(text) <= 200):
        problems.append(
            "entry is %d characters, must be 1-200" % len(text)
        )
    if not text.strip():
        problems.append("entry is only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("entry must be exactly one line")
    if text != text.strip():
        problems.append("entry has leading or trailing whitespace")
    if any(ord(ch) < 32 for ch in text):
        problems.append("entry contains control characters")
    if len(text.encode("utf-8")) > 200:
        problems.append("entry exceeds 200 bytes")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    return problems


def main():
    problems = gate_guard(ENTRY)
    if problems:
        for problem in problems:
            print("gate guard failed: %s" % problem, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)

    # Re-read what we wrote and re-check it, so the file on disk
    # is verified, not just the string in memory.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    problems = gate_guard(written)
    if problems or written != ENTRY:
        for problem in problems:
            print("gate guard failed on file: %s" % problem, file=sys.stderr)
        if written != ENTRY:
            print("gate guard failed: file differs from entry", file=sys.stderr)
        return 1

    print("wrote %d characters to %s" % (len(written), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
