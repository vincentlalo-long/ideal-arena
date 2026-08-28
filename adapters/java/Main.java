package arena;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class Main {
    private static List<Integer> parseArray(String json, String key) {
        List<Integer> list = new ArrayList<>();
        int keyIdx = json.indexOf("\"" + key + "\"");
        if (keyIdx == -1) return list;
        int start = json.indexOf("[", keyIdx);
        int end = json.indexOf("]", start);
        if (start == -1 || end == -1) return list;

        String content = json.substring(start + 1, end).trim();
        if (content.isEmpty()) return list;

        String[] tokens = content.split(",");
        for (String token : tokens) {
            String clean = token.trim();
            if (!clean.isEmpty()) {
                try {
                    list.add(Integer.parseInt(clean));
                } catch (NumberFormatException ignored) {}
            }
        }
        return list;
    }

    public static void main(String[] args) throws Exception {
        Strategy bot = new MyStrategy();
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String line;

        while ((line = reader.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;

            if (line.contains("\"RESET\"")) {
                bot.reset();
                System.out.println("{\"status\":\"OK\"}");
                System.out.flush();
            } else {
                List<Integer> histSelf = parseArray(line, "history_self");
                List<Integer> histOpp = parseArray(line, "history_opp");
                int action = bot.step(histSelf, histOpp);
                System.out.println("{\"action\":" + action + "}");
                System.out.flush();
            }
        }
    }
}
