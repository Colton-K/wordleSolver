#!/usr/bin/python3

import gensim

class SemantleSolver:
    def __init__(self, error=.01, wordsfile='words.pkl', vecsFile='vecs.pkl', pruneWords=True):
        self.error = error
        self.wordsfile = wordsfile
        self.vecsFile = vecsFile
        self.pruneWords = pruneWords

        self.candidates = []
        self.words = []
        self.vecs = None

    def loadVec(self):
        #  print("Loading vectors...")
        self.vecs = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
        #  print("Vectors loaded!")

    def loadWords(self):
        if not self.vecs:
            self.loadVec()

        words = [""] * 3000000
        for i in range(3000000):
            words[i] = (self.vecs.index_to_key[i])

        if self.pruneWords:
            #  print("Pruning...")
            actualWords = []
            for word in words:
                if word.isalnum() and word.islower():
                    actualWords.append(word)
            words = actualWords
            #  print("Done pruning!")
        self.words = words

    def getCandidates(self, k):
        outlist = []
        for i,entry in enumerate(self.candidates[:k]):
            outlist.append(f"{i+1}: {entry[0]}")
        return outlist

    def inputGuess(self, guess, score):
        #  print("Searching...")
        candidates = []
        filteredWords = []
        score = float(score)/100

        for word in self.words:
            potentialScore = self.vecs.similarity(word, guess)
            if abs(score - potentialScore) <= self.error:
                if word.isalnum() and word.islower():
                    candidates.append((word, score-potentialScore))
                    filteredWords.append(word)

        candidates.sort(key=lambda y: abs(y[1]), reverse=False)

        self.words = filteredWords
        self.candidates = candidates


def main():
    s = SemantleSolver()
    s.loadWords()

    while True:
        word = input("Entered word: ")
        score = input("Enter its score: ")

        s.inputGuess(word, score)

        possibilities = s.getCandidates(5)
        print("Guesses:")
        for i, possib in enumerate(possibilities):
            print(f'{i+1}: {possib[0]} {possib[1]}')

if __name__ == "__main__":
    main()

