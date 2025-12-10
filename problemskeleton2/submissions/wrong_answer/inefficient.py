def evilness(word: str) -> int:
    return sum(ord(c) for c in word)

def main():
    n, k = map(int, input().split())
    data = []
    for i in range(n):
        w = input().strip()
        e = evilness(w)
        data.append((e, i, w))
        if len(data) < k:
            print("- -")
            continue
        data.sort()
        kth_least_word = data[k - 1][2]
        kth_most_word = data[len(data) - k][2]
        print(kth_least_word, kth_most_word)

if __name__ == "__main__":
    main()