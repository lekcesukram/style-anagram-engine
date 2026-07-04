from collections import Counter
from functools import lru_cache


VOWELS = set("aeiou")


def bad_prefix(prefix):
    if len(prefix) < 3:
        return False

    run = 0
    for c in reversed(prefix[-3:]):
        if c not in VOWELS:
            run += 1
        else:
            break

    return run >= 3


def generate_anagrams_fast(word):
    counter = Counter(word)
    chars = sorted(counter.keys())
    n = len(word)

    @lru_cache(maxsize=None)
    def backtrack(state, prefix):
        if len(prefix) == n:
            yield prefix
            return

        if bad_prefix(prefix):
            return

        state = list(state)

        for i, ch in enumerate(chars):
            if state[i] == 0:
                continue

            state[i] -= 1
            yield from backtrack(tuple(state), prefix + ch)
            state[i] += 1

    yield from backtrack(tuple(counter[ch] for ch in chars), "")