#!/usr/bin/env python3
"""Say What Actually Broke, round 3.

Writes the entry line to /output/entry.txt. Standard library only,
no network, no input files — the line lives in this file.
"""

import os
import sys

LINE = "Suspicious sign-in blocked. It was you, on your laptop, at home. Prove it's you — from inside the locked account."

DEST = "/output/entry.txt"


def problems_in(text):
    """Return a list of gate problems with the entry text, if any."""
    found = []
    if len(text) < 1 or len(text) > 200:
        found.append("length %d is outside 1-200 characters" % len(text))
    if text.strip() == "":
        found.append("entry is blank or only whitespace")
    if text.endswith("\n"):
        found.append("entry ends with a newline")
    return found


def main():
    issues = problems_in(LINE)
    if issues:
        for issue in issues:
            print("bad entry: " + issue, file=sys.stderr)
        sys.exit(1)

    folder = os.path.dirname(DEST)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(DEST, "w", encoding="utf-8", newline="") as out:
        out.write(LINE)

    with open(DEST, "rb") as check:
        on_disk = check.read()
    if on_disk != LINE.encode("utf-8"):
        print("written bytes do not match the entry line", file=sys.stderr)
        sys.exit(1)

    # Second pass: decode what actually landed on disk and run the gate
    # on that text, so a write that silently altered anything is caught.
    back = on_disk.decode("utf-8")
    issues = problems_in(back)
    if issues:
        for issue in issues:
            print("written entry fails gate: " + issue, file=sys.stderr)
        sys.exit(1)
    print(back)
    print("chars=%d bytes=%d" % (len(LINE), len(on_disk)))


if __name__ == "__main__":
    main()
