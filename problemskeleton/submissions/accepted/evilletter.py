import sys
import heapq

data = sys.stdin.read().strip().split()
if not data:
    sys.exit(0)

n = int(data[0])
k = int(data[1])
s = data[2]

minheap = []  # store largest k ASCII codes
for ch in s:
    heapq.heappush(minheap, ord(ch))
    if len(minheap) > k:
        heapq.heappop(minheap)

sys.stdout.write(chr(minheap[0]) + "\n")
