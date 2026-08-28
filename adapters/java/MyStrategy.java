package arena;

import java.util.List;

public class MyStrategy implements Strategy {
    @Override
    public void reset() {}

    @Override
    public int step(List<Integer> historySelf, List<Integer> historyOpp) {
        if (historyOpp == null || historyOpp.isEmpty()) {
            return 1;
        }
        return historyOpp.get(historyOpp.size() - 1);
    }
}
