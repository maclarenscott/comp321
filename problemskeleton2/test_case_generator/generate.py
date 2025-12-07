"""Test case generator for The Evil Word with deterministic tie-breaking.

Generates sample and secret cases and can write matching .ans files.
"""

import argparse
import random
from pathlib import Path
from typing import List, Tuple

VISIBLE = [chr(i) for i in range(33, 127)]


def evilness(word: str) -> int:
    return sum(ord(c) for c in word)


def compute_answers(words: List[str], k: int) -> List[str]:
    import heapq
    # (-score, -idx, word) for k-th smallest
    small_max: List[Tuple[int, int, str]] = []
    # (score, idx, word) for k-th largest
    large_min: List[Tuple[int, int, str]] = []
    out: List[str] = []
    for i, w in enumerate(words):
        score = evilness(w)
        heapq.heappush(small_max, (-score, -i, w))
        if len(small_max) > k:
            heapq.heappop(small_max)
        heapq.heappush(large_min, (score, i, w))
        if len(large_min) > k:
            heapq.heappop(large_min)
        if i + 1 < k:
            out.append("- -")
        else:
            out.append(f"{small_max[0][2]} {large_min[0][2]}")
    return out


def write_case(outdir: Path, name: str, n: int, k: int, words: List[str], with_answers: bool) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    case_path = outdir / f"{name}.in"
    lines = [f"{n} {k}\n"] + [w + "\n" for w in words]
    case_path.write_text("".join(lines))
    if with_answers:
        ans_lines = compute_answers(words, k)
        (outdir / f"{name}.ans").write_text("\n".join(ans_lines) + "\n")


def make_samples() -> List[Tuple[str, int, int, List[str]]]:
    sample1_words = ["hello", "x", "bb", "abc", "wow"]
    sample2_words = ["abc", "xyz", "a"]
    return [
        ("sample1", 5, 2, sample1_words),
        ("sample2", 3, 1, sample2_words),
    ]


def rand_word(rng: random.Random, length: int) -> str:
    return "".join(rng.choice(VISIBLE) for _ in range(length))


def make_secret(seed: int) -> List[Tuple[str, int, int, List[str]]]:
    rng = random.Random(seed)
    cases: List[Tuple[str, int, int, List[str]]] = []

    cases.append(("secret01", 1, 1, ["!"]))
    cases.append(("secret02", 2, 2, ["A", "z"]))
    cases.append(("secret03", 5, 3, ["abc"] * 5))
    cases.append(("secret04", 5, 2, ["~", "!", "}}", "!!", "|"]))
    cases.append(("secret05", 6, 2, ["~~~~~", "A", "xyz", "9", "!!!!!!!!!", "Hi!"]))
    cases.append(("secret06", 6, 1, ["short", "VERYVERYLONG", "mid", "Z", "p\"p", "q"]))
    cases.append(("secret07", 7, 3, ["aa", "bb", "cc", "dd", "ee", "ff", "gg"]))
    cases.append(("secret08", 8, 4, ["aA", "bB", "cC", "dD", "eE", "fF", "gG", "hH"]))
    cases.append(("secret09", 10, 5, ["Aa", "b`", "c_", "d^", "e]", "f[", "gZ", "hY", "iX", "jW"]))
    cases.append(("secret10", 10, 2, ["!", "!!", "!!!", "!!!!", "!!!!!", "!!!!!!", "!!!", "!!", "!", "!!!!!!!!"]))
    cases.append(("secret11", 10, 9, ["xyz", "abc", "abc", "zzz", "yyy", "xxx", "mid", "wow", "low", "high"]))
    cases.append(("secret12", 12, 6, [rand_word(rng, rng.randint(1, 6)) for _ in range(12)]))
    cases.append(("secret13", 20, 10, [rand_word(rng, rng.randint(1, 12)) for _ in range(20)]))
    cases.append(("secret14", 50, 25, [rng.choice(["~", "!", "A", "{", "0"]) for _ in range(50)]))
    cases.append(("secret15", 80, 40, [rand_word(rng, rng.randint(1, 8)) for _ in range(80)]))

    words16 = [rng.choice(VISIBLE) for _ in range(5000)]
    cases.append(("secret16", len(words16), 2500, words16))

    words17 = [rand_word(rng, 20) for _ in range(200)]
    cases.append(("secret17", len(words17), 50, words17))

    words18 = [rng.choice(["A", "B", "~", "#", "$"]) for _ in range(1000)]
    cases.append(("secret18", len(words18), 990, words18))

    words19 = [rand_word(rng, rng.randint(1, 30)) for _ in range(150)]
    cases.append(("secret19", len(words19), 2, words19))

    words20 = [rng.choice(VISIBLE) for _ in range(10000)]
    cases.append(("secret20", len(words20), 5000, words20))

    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", action="store_true")
    parser.add_argument("--secret", action="store_true")
    parser.add_argument("--outdir", type=Path, help="output directory")
    parser.add_argument("--with-answers", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    tasks: List[Tuple[str, int, int, List[str]]] = []
    if args.samples:
        tasks.extend(make_samples())
    if args.secret:
        tasks.extend(make_secret(args.seed))

    if not tasks:
        raise SystemExit("Specify --samples or --secret to generate cases.")

    if args.outdir:
        for name, n, k, words in tasks:
            write_case(args.outdir, name, n, k, words, args.with_answers)
    else:
        name, n, k, words = tasks[0]
        print(f"{n} {k}")
        for w in words:
            print(w)
        if len(tasks) > 1:
            print("# additional cases not printed; use --outdir")


if __name__ == "__main__":
    main()
