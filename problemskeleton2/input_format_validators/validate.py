#!/usr/bin/env python3
"""
Input validator for The Evil Word.

Format:
    n k
    w1
    w2
    ...
    wn

Constraints:
    1 <= k <= n <= 200000
    each wi is non-empty and uses only visible ASCII [33,126] (i.e., '!'-'~')

Exit code 42 on success; any other code on failure.
"""

import re
import sys
from typing import NoReturn


def fail(msg: str) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(1)


def main() -> None:
    first_line = sys.stdin.readline()
    if not first_line:
        fail("Missing first line")

    if not re.fullmatch(r"[1-9]\d* [1-9]\d*\n?", first_line):
        fail("First line must be two positive integers")

    n_str, k_str = first_line.strip().split()
    n = int(n_str)
    k = int(k_str)

    if not (1 <= k <= n <= 200_000):
        fail("n,k out of range or k>n")

    count = 0
    for line in sys.stdin:
        if count >= n:
            fail("Too many lines after expected words")
        word = line.rstrip("\n")
        if len(word) == 0:
            fail("Empty word not allowed")
        for ch in word:
            code = ord(ch)
            if code < 33 or code > 126:
                fail("Invalid character (outside !-~)")
        count += 1

    if count < n:
        fail("Too few words")

    sys.exit(42)


if __name__ == "__main__":
    main()
