import sys

data = sys.stdin.read().strip().split()
if not data:
    sys.exit(0)

# WRONG: ignores duplicate characters entirely, so ranks are based on distinct ASCII codes only
n = int(data[0])
k = int(data[1])
s = data[2]

unique_vals = sorted({ord(ch) for ch in s}, reverse=True)
if k <= len(unique_vals):
    sys.stdout.write(chr(unique_vals[k - 1]) + "\n")
else:
    # fall back if k exceeds unique count (still wrong for duplicated ranks)
    sys.stdout.write(chr(unique_vals[-1]) + "\n")
