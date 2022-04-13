#!/usr/bin/python3

import os

debug = 0

scores = {}
grey = ""
yellow = []
green = []

def readWords():
    with open('words', 'r') as fh:
        words = [s.rstrip() for s in fh.readlines()]
    return words

"""
very basic scoring method, basically just takes the sum of the frequency of each letter that is in the word
"""
def getWordScores(words):
    # TODO: make a better hueristic for getting word scores
    global scores
    wordScores = {}

    for word in words:
        score = 0
    
        letters = set(word)
        #  print(letters)
    
        for letter in letters:
            score += scores[letter]

        wordScores[word] = score

    #  print(wordScores)
    return wordScores

def grepMethod(characters, information):
    global grey
    global yellow
    global green

    for i in range(len(characters)):
        letter, info = characters[i], information[i]

        if info == 'n':
            grey += letter
        elif info == 'y':
            yellow.append((letter, i))
        elif info == 'g':
            green.append((letter, i))

    grepString = ""

    for (letter, position) in yellow:
        # remove from grey
        grey = grey.replace(letter, '')
        # apply filter
        grepString += f' | grep {letter} | grep -v {"."*position+letter+"."*(4-position)}'

    for (letter, position) in green:
        # remove from grey
        grey = grey.replace(letter, '')
        # apply filter
        grepString += f' | grep {"."*position+letter+"."*(4-position)}'

    grepString = f'cat words | grep -v [{grey}]'+grepString
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

    return words

def getBestScore(scores):
    return max(scores, key=scores.get)

def main():
    # generate word scores
    for word in readWords():
        letters = set(word)
        for letter in letters:
            if letter in scores:
                scores[letter] += 1
            else:
                scores[letter] = 1
    
    print("First guess should be:", getBestScore(getWordScores(readWords())))
    while (1):
        word = str(input("enter guess: "))
        output = str(input("enter result: "))

        potentialWords = grepMethod(word, output)
        wordScores = getWordScores(potentialWords)
        print(f'Guess: {getBestScore(wordScores)}')

if __name__ == "__main__":
    main()

