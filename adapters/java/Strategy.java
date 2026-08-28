package arena;

import java.util.List;

public interface Strategy {
    default void reset() {}
    int step(List<Integer> historySelf, List<Integer> historyOpp);
}
