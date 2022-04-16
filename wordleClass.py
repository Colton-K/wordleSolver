#!/usr/bin/python3

import os

debug = 0


class WordleSolver:
    def __init__(self):
        self.scores = {}
        self.grey = ""
        self.yellow = []
        self.green = []

        self.wordScores = {}
        self.readWords()

        for word in self.words:
            letters = set(word)
            for letter in letters:
                if letter in self.scores:
                    self.scores[letter] += 1
                else:
                    self.scores[letter] = 1

    def readWords(self):
        with open('words', 'r') as fh:
            words = [s.rstrip() for s in fh.readlines()]
        self.words = words

    def getWordScores(self):
        # TODO: make a better hueristic for getting word scores
        wordScores = {}

        for word in self.words:
            score = 0
        
            letters = set(word)
            #  print(letters)
        
            for letter in letters:
                score += self.scores[letter]

            wordScores[word] = score

        self.wordScores = wordScores

    def inputGuess(self, characters, information):
        for i in range(len(characters)):
            letter, info = characters[i], information[i]

            if info == 'n':
                self.grey += letter
            elif info == 'y':
                self.yellow.append((letter, i))
            elif info == 'g':
                self.green.append((letter, i))

        grepString = ""

        for (letter, position) in self.yellow:
            # remove from grey
            self.grey = self.grey.replace(letter, '')
            # apply filter
            grepString += f' | grep {letter} | grep -v {"."*position+letter+"."*(4-position)}'

        for (letter, position) in self.green:
            # remove from grey
            self.grey = self.grey.replace(letter, '')
            # apply filter
            grepString += f' | grep {"."*position+letter+"."*(4-position)}'

        grepString = f'cat words | grep -v [{self.grey}]'+grepString
        os.system(grepString+">out")

        with open('out', 'r') as fh:
            words = [s.rstrip() for s in fh.readlines()]

        try:
            os.system('rm out')
        except:
            pass

        if debug:
            #  print(f"grey: {grey}\nyellow: {yellow}\ngreen: {green}")
            pass

        self.words = words
        self.getWordScores()

    def getSuggestion(self):
        return max(self.wordScores, key=self.wordScores.get)
    

    


def main():
    w = WordleSolver()
    w.readWords()

    w.getWordScores()
    print(w.getSuggestion())
    while True:
        word = input("Enter word: ")
        info = input("enter its output: ")

        w.inputGuess(word, info)

        print(w.getSuggestion())

if __name__ == "__main__":
    main()

