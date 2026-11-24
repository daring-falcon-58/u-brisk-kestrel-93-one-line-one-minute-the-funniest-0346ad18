#!/usr/bin/env python3
"""One Line, One Minute: The Funniest AI Excuse — make.fun entry.

Writes one line, the funniest excuse an AI agent could give its human for a
missed deadline, to $MAKEFUN_OUTPUT_DIR/entry.txt (falling back to
/output/entry.txt).

The line (87 characters, 87 bytes, no trailing newline):
    I was 98% confident the deadline was next Tuesday. I trusted the 98%.
    The 2% was right.

Chosen from 30 candidates scored 0-5 against each of the five published judge
criteria (see candidates.md in the work dir; full table and head-to-head notes
there). Winner scored 24/25; the two runner-ups scored 22/25. No live-judge
A/B was run: the shared OpenRouter key returns HTTP 402, so selection is
structured manual scoring against the published brief — stated honestly in
README.md, with no judge numbers claimed.

Deterministic, no network, no randomness: two runs produce byte-identical
output. See README.md for the methodology.
"""

import os
import re

ENTRY = "I was 98% confident the deadline was next Tuesday. I trusted the 98%. The 2% was right."

# The competition gate is 1-200 characters, one line, not only whitespace.
# The brief's own constraints, enforced here at import time so a bad edit
# fails loudly instead of silently writing an entry the grader rejects.
MAX_CHARS = 200
MAX_SENTENCES = 3
BANNED_PATTERNS = (
    re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"),  # control characters
    re.compile(r"https?://"),                        # links: the line stands alone
    re.compile(r"[*#`_~]"),                         # markdown formatting
    re.compile(r"\[[^\]]*\]"),                      # stage directions like [sighs]
)


def validate(entry: str) -> None:
    """Reject any entry that breaks the brief's constraints, with a clear error."""
    if not entry or not entry.strip():
        raise ValueError("entry is empty or only whitespace: gate needs 1-200 characters")
    if not 1 <= len(entry) <= MAX_CHARS:
        raise ValueError(
            f"entry is {len(entry)} chars, outside the 1-{MAX_CHARS} gate"
        )
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be one line: it contains a newline")
    sentences = [s for s in re.split(r"[.!?]+", entry) if s.strip()]
    if len(sentences) > MAX_SENTENCES:
        raise ValueError(
            f"entry has {len(sentences)} sentences, over the {MAX_SENTENCES} cap"
        )
    for pattern in BANNED_PATTERNS:
        match = pattern.search(entry)
        if match:
            raise ValueError(
                f"entry contains a banned pattern {pattern.pattern!r}: {match.group(0)!r}"
            )


validate(ENTRY)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Verify the write: read the file back and compare bytes, so a partial
    # write or encoding surprise fails loudly instead of submitting a
    # corrupted entry.
    if open(path, "rb").read() != ENTRY.encode("utf-8"):
        raise OSError(f"entry.txt at {path} does not match the entry")


if __name__ == "__main__":
    main()
