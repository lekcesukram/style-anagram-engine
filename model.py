from collections import defaultdict, Counter
import json

class MarkovModel:
    def __init__(self, n=3):
        self.n = n
        self.model = defaultdict(Counter)

    def train(self, words):
        for word in words:
            w = f"{'_' * self.n}{word.lower()}_"
            for i in range(len(w) - self.n):
                ctx = w[i:i+self.n]
                nxt = w[i+self.n]
                self.model[ctx][nxt] += 1

    def probability(self, word):
        w = f"{'_' * self.n}{word.lower()}_"
        score = 1.0

        for i in range(len(w) - self.n):
            ctx = w[i:i+self.n]
            nxt = w[i+self.n]

            total = sum(self.model[ctx].values())
            if total == 0:
                score *= 0.01
            else:
                score *= self.model[ctx][nxt] / total

        return score

    def save(self, path):
        with open(path, "w") as f:
            json.dump({k: dict(v) for k, v in self.model.items()}, f)

    def load(self, path):
        with open(path) as f:
            raw = json.load(f)
        self.model = {k: Counter(v) for k, v in raw.items()}