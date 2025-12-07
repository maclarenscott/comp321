import sys

# WRONG: ranks words by length instead of ASCII sum, so it fails when shorter words have higher ASCII totals.
data = sys.stdin.read().splitlines()
if not data:
    sys.exit(0)

n, k = map(int, data[0].split())
words = data[1:]

small_max = []
large_min = []
import heapq
out = []
for i, w in enumerate(words):
    score = len(w)  # incorrect metric
    heapq.heappush(small_max, (-score, w))
    if len(small_max) > k:
        heapq.heappop(small_max)
    heapq.heappush(large_min, (score, w))
    if len(large_min) > k:
        heapq.heappop(large_min)
    if i + 1 < k:
        out.append("- -")
    else:
        out.append(f"{small_max[0][1]} {large_min[0][1]}")

sys.stdout.write("\n".join(out) + "\n")
