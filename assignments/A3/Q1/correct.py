import sys
import re
from collections import Counter

class Correct:
    def __init__(self):
        self.document = open('big.txt').read()
        self.words()
        self.count_words()

    def correction(self, word):
        "Most probable spelling correction for word."
        word = word.lower()
        candidates = self.candidates(word)
        return max(candidates, key=self.P)

    def candidates(self, word):
        "Generate possible spelling corrections for word."
        word = word.lower()
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.word_count)

    def edits1(self, word):
        "All edits that are one edit away from `word`."
        word = word.lower()
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        "All edits that are two edits away from `word`."
        word = word.lower()
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def words(self):
        self.words = re.findall(r'\w+', self.document.lower())

    def count_words(self):
        self.word_count = Counter(self.words)

    def P(self, word):
        "Probability of `word`."
        word = word.lower()
        N = sum(self.word_count.values())
        return self.word_count[word] / N


if __name__ == '__main__':
    correct = Correct()

    if len(sys.argv) != 2:
        print "Usage: python correct.py <word>"
	print "Example: python correct.py camputer"
        exit()

    word = sys.argv[1]
    corrected = correct.correction(word)

    print corrected
