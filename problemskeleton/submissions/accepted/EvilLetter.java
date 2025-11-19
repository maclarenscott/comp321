import java.io.BufferedInputStream;
import java.io.IOException;
import java.util.PriorityQueue;

public class EvilLetter {
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

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        String sn = fs.next();
        if (sn == null) return;
        long n = Long.parseLong(sn);
        long k = Long.parseLong(fs.next());
        String s = fs.next();

        PriorityQueue<Integer> minheap = new PriorityQueue<>();
        for (int i = 0; i < s.length(); i++) {
            int val = s.charAt(i);
            minheap.offer(val);
            if (minheap.size() > k) {
                minheap.poll();
            }
        }

        char ans = (char) (int) minheap.peek();
        System.out.println(ans);
    }
}
