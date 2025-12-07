import heapq
import sys


def main() -> None:
    try:
        first = input().strip()
    except EOFError:
        return
    if not first:
        return
    n, k = map(int, first.split())

    small_max = []  # (-score, -idx, word) keep k smallest (later arrival wins ties)
    large_min = []  # (score, idx, word) keep k largest
    out_lines = []

    for i in range(n):
        try:
            w = input().rstrip("\n")
        except EOFError:
            break
        score = sum(ord(ch) for ch in w)

        heapq.heappush(small_max, (-score, -i, w))
        if len(small_max) > k:
            heapq.heappop(small_max)

        heapq.heappush(large_min, (score, i, w))
        if len(large_min) > k:
            heapq.heappop(large_min)

        if i + 1 < k:
            out_lines.append("- -")
        else:
            kth_smallest = small_max[0][2]
            kth_largest = large_min[0][2]
            out_lines.append(f"{kth_smallest} {kth_largest}")

    sys.stdout.write("\n".join(out_lines) + ("\n" if out_lines else ""))


if __name__ == "__main__":
    main()
