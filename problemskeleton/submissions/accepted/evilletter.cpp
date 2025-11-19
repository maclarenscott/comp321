#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, k;
    if (!(cin >> n >> k)) return 0;
    string s;
    cin >> s;

    priority_queue<int, vector<int>, greater<int>> minheap; // keeps largest k ASCII codes
    for (char c : s) {
        minheap.push(static_cast<unsigned char>(c));
        if (static_cast<int>(minheap.size()) > k) {
            minheap.pop();
        }
    }

    char ans = static_cast<char>(minheap.top());
    cout << ans << "\n";
    return 0;
}
