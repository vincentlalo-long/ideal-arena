package arena;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    private static final String SDK = "java/0.2.0";

    public static void main(String[] args) throws Exception {
        Strategy bot = new MyStrategy();
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String line;

        while ((line = reader.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;

            Object parsed;
            try {
                parsed = Json.parse(line);
            } catch (RuntimeException e) {
                System.err.println("arena-agent: ignoring malformed line");
                continue;
            }
            if (!(parsed instanceof Map)) continue;

            Map<String, Object> msg = Json.asObject(parsed);
            String type = Json.asString(msg.get("type"), "");
            String reply = null;

            switch (type) {
                case "hello":
                    reply = "{\"type\":\"ready\",\"sdk\":\"" + SDK + "\"}";
                    break;
                case "reset":
                    bot.reset(Json.asLong(msg.get("seed"), 0L));
                    Map<String, Object> ack = new LinkedHashMap<>();
                    ack.put("type", "ack");
                    ack.put("episode", Json.asString(msg.get("episode"), ""));
                    reply = Json.stringify(ack);
                    break;
                case "act":
                    Object action = bot.act(msg.get("obs"));
                    Map<String, Object> response = new LinkedHashMap<>();
                    response.put("type", "action");
                    response.put("t", Json.asLong(msg.get("t"), 0L));
                    response.put("action", action);
                    reply = Json.stringify(response);
                    break;
                default:
                    break;
            }

            if (reply != null) {
                System.out.println(reply);
                System.out.flush();
            }
        }
    }
}
