#include <iostream>
#include <queue>
#include <string>
#include <utility>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    if (!(cin >> n >> k)) return 0;
    vector<string> outputs;
    outputs.reserve(n);

    // Max-heap for k smallest scores (score, idx). Later idx counts as larger for tie-breaks.
    priority_queue<tuple<long long, int, string>> smallest;
    // Min-heap for k largest scores (score, idx)
    priority_queue<tuple<long long, int, string>, vector<tuple<long long, int, string>>, greater<tuple<long long, int, string>>> largest;

    for (int i = 0; i < n; ++i) {
        string w;
        cin >> w;
        long long score = 0;
        for (unsigned char c : w) score += static_cast<int>(c);

        smallest.push({score, i, w});
        if ((int)smallest.size() > k) smallest.pop();

        largest.push({score, i, w});
        if ((int)largest.size() > k) largest.pop();

        if (i + 1 < k) {
            outputs.push_back("- -");
        } else {
            string kth_smallest = get<2>(smallest.top());
            string kth_largest = get<2>(largest.top());
            outputs.push_back(kth_smallest + " " + kth_largest);
        }
    }

    for (const auto &line : outputs) {
        cout << line << '\n';
    }
    return 0;
}
