import java.io.BufferedInputStream;
import java.io.IOException;
import java.util.PriorityQueue;

public class EvilWord {
    private static class FastScanner {
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        private int readByte() throws IOException {
            if (ptr >= len) {
                len = System.in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }

        String next() throws IOException {
            StringBuilder sb = new StringBuilder();
            int b;
            while ((b = readByte()) != -1 && b <= ' ') {}
            if (b == -1) return null;
            do {
                sb.append((char) b);
            } while ((b = readByte()) > ' ');
            return sb.toString();
        }
    }

    private static class Entry implements Comparable<Entry> {
        long score;
        int idx;
        String word;
        Entry(long s, int i, String w) { score = s; idx = i; word = w; }
        @Override
        public int compareTo(Entry other) {
            if (this.score != other.score) return Long.compare(this.score, other.score);
            return Integer.compare(this.idx, other.idx); // arrival order tiebreak
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        String sn = fs.next();
        if (sn == null) return;
        int n = Integer.parseInt(sn);
        int k = Integer.parseInt(fs.next());

        PriorityQueue<Entry> smallest = new PriorityQueue<>((a, b) -> {
            // max-heap: invert compareTo
            int cmp = Long.compare(b.score, a.score);
            if (cmp != 0) return cmp;
            return Integer.compare(b.idx, a.idx);
        });
        PriorityQueue<Entry> largest = new PriorityQueue<>(); // min-heap by score, then idx

        StringBuilder out = new StringBuilder();
        for (int i = 0; i < n; i++) {
            String w = fs.next();
            long score = 0;
            for (int j = 0; j < w.length(); j++) {
                score += (int) w.charAt(j);
            }

            smallest.offer(new Entry(score, i, w));
            if (smallest.size() > k) smallest.poll();

            largest.offer(new Entry(score, i, w));
            if (largest.size() > k) largest.poll();

            if (i + 1 < k) {
                out.append("- -\\n");
            } else {
                String kthSmall = smallest.peek().word;
                String kthLarge = largest.peek().word;
                out.append(kthSmall).append(' ').append(kthLarge).append('\\n');
            }
        }

        System.out.print(out.toString());
    }
}
