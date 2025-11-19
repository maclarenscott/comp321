"""Test case generator for the Evil Letter problem.

Usage examples:
    # Generate one random case to stdout (no files created)
    python3 generate.py --n 10 --k 3 --seed 1

    # Write curated sample cases (with answers) into ../data/sample
    python3 generate.py --samples --outdir ../data/sample --with-answers

    # Write curated secret cases (with answers) into ../data/secret
    python3 generate.py --secret --outdir ../data/secret --with-answers

This script can also generate arbitrary random cases when --samples/--secret
are not provided.
"""

import argparse
import random
import sys
from pathlib import Path
from typing import List, Tuple

VISIBLE_ASCII = [chr(i) for i in range(33, 127)]


def kth_evil_char(text: str, k: int) -> str:
    """Return the k-th largest ASCII character (counting duplicates)."""
    values = sorted((ord(c) for c in text), reverse=True)
    return chr(values[k - 1])


def format_case(n: int, k: int, text: str) -> str:
    return f"{n} {k}\n{text}\n"


def write_case(outdir: Path, name: str, n: int, k: int, text: str, with_answers: bool) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    case_path = outdir / f"{name}.in"
    case_path.write_text(format_case(n, k, text))
    if with_answers:
        ans_path = outdir / f"{name}.ans"
        ans_path.write_text(kth_evil_char(text, k) + "\n")


def random_string(rng: random.Random, length: int) -> str:
    return "".join(rng.choice(VISIBLE_ASCII) for _ in range(length))


def bursty_string(rng: random.Random, length: int, hot: str, cold: str) -> str:
    """Create a string with long runs of hot/cold characters."""
    chunks = []
    remaining = length
    while remaining > 0:
        use_hot = rng.random() < 0.6
        chunk_char = hot if use_hot else cold
        chunk_len = rng.randint(1, min(200, remaining))
        chunks.append(chunk_char * chunk_len)
        remaining -= chunk_len
    return "".join(chunks)


def make_samples() -> List[Tuple[str, int, int, str]]:
    cases = []
    cases.append(("sample1", 4, 2, "5364"))
    cases.append(("sample2", 3, 1, "ax)"))
    # Mix of repeated high/low punctuation to show ties and mid positions
    cases.append(("sample3", 8, 5, "~~!!}}<<"))
    return cases


def make_secret_cases(seed: int) -> List[Tuple[str, int, int, str]]:
    rng = random.Random(seed)
    cases = []

    cases.append(("secret01", 1, 1, "!"))
    cases.append(("secret02", 2, 2, "Az"))
    cases.append(("secret03", 6, 3, "~~~~~~"))
    cases.append(("secret04", 10, 1, "76543210!!"))
    cases.append(("secret05", 10, 10, "abcdefgXYZ"))

    # Alternating extremes
    text = ("~!" * 30) + "*" * 40
    cases.append(("secret06", len(text), len(text) // 2, text))

    # Mostly mid-ascii with occasional spikes
    text = "".join("M" if rng.random() < 0.8 else rng.choice("{}[]<>?~") for _ in range(200))
    cases.append(("secret07", len(text), 50, text))

    # Random small sizes, various k
    for idx in range(8, 13):
        length = rng.randint(20, 80)
        text = random_string(rng, length)
        k = rng.randint(1, length)
        cases.append((f"secret{idx:02d}", length, k, text))

    # Bursty duplicates with high vs low ASCII to test counting duplicates
    text = bursty_string(rng, 300, "~", "A")
    cases.append(("secret13", len(text), 120, text))

    # Strictly increasing ASCII values
    inc_chars = "!" + "123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    text = inc_chars
    cases.append(("secret14", len(text), len(text) // 3, text))

    # Strictly decreasing ASCII values
    dec_chars = "~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:987654321!"
    cases.append(("secret15", len(dec_chars), len(dec_chars) - 5, dec_chars))

    # Medium random with k near 1
    text = random_string(rng, 500)
    cases.append(("secret16", len(text), 1, text))

    # Medium random with k near n
    text = random_string(rng, 700)
    cases.append(("secret17", len(text), len(text) - 2, text))

    # Sparse high characters inside many lows
    low = "#"
    high = "~"
    text = list(low * 2000)
    for pos in rng.sample(range(2000), 25):
        text[pos] = high
    text = "".join(text)
    cases.append(("secret18", len(text), 25, text))

    # Mixed digits and letters to check ASCII ordering across classes
    text = "0123456789" * 50 + "ABCDE" * 40 + "xyz" * 60
    cases.append(("secret19", len(text), 500, text))

    # Near-maximum size with random printable characters
    big_length = 200_000
    big_text = random_string(rng, big_length)
    big_k = 150_000
    cases.append(("secret20", big_length, big_k, big_text))

    return cases


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate test cases for Evil Letter")
    parser.add_argument("--n", type=int, help="length of the string (for ad-hoc generation)")
    parser.add_argument("--k", type=int, help="rank to query (for ad-hoc generation)")
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    parser.add_argument("--outdir", type=Path, help="directory to write cases into")
    parser.add_argument("--with-answers", action="store_true", help="emit matching .ans files")
    parser.add_argument("--samples", action="store_true", help="generate the curated sample set")
    parser.add_argument("--secret", action="store_true", help="generate the curated secret set")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    tasks: List[Tuple[str, int, int, str]] = []

    if args.samples:
        tasks.extend(make_samples())
    if args.secret:
        tasks.extend(make_secret_cases(args.seed))

    if not tasks:
        if args.n is None or args.k is None:
            raise SystemExit("Provide --n and --k for ad-hoc generation, or use --samples/--secret.")
        rng = random.Random(args.seed)
        text = random_string(rng, args.n)
        tasks.append(("case", args.n, args.k, text))

    if args.outdir:
        for name, n, k, text in tasks:
            write_case(args.outdir, name, n, k, text, args.with_answers)
    else:
        name, n, k, text = tasks[0]
        print(format_case(n, k, text), end="")
        if len(tasks) > 1:
            print("# Additional cases were generated but not written because no --outdir was provided", file=sys.stderr)


if __name__ == "__main__":
    main()
