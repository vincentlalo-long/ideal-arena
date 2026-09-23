package arena;

public interface Strategy {
    default void reset(long seed) {}

    Object act(Object observation);
}
