#!/usr/bin/env python3
"""
Input validator for the Evil Letter problem.

Expected format:
    n k
    s

Constraints:
    1 <= k <= n <= 200000
    |s| = n
    s consists only of visible ASCII characters in [33, 126] (i.e., '!'-'~')

Validator returns exit code 42 on success; any other exit code means invalid.
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

    s_line = sys.stdin.readline()
    if not s_line:
        fail("Missing string line")

    s = s_line.rstrip("\n")

    if len(s) != n:
        fail(f"String length {len(s)} does not match n={n}")

    for ch in s:
        code = ord(ch)
        if code < 33 or code > 126:
            fail("String contains invalid characters (outside !-~)")

    remainder = sys.stdin.read()
    if remainder.strip() != "":
        fail("Extra data after string line")

    sys.exit(42)


if __name__ == "__main__":
    main()
