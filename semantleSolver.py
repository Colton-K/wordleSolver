#!/usr/bin/python3

import gensim

error = .01

def loadVec():
    print("Loading vectors...")
    vecs = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    print("Vectors loaded!")
    return vecs

def getCandidates(guess, score, words, vecs):
    print("Searching...")
    candidates = []
    score = float(score)/100

    for word in words:
        #  print(f'word: {word}\tguess: {guess}')
        potentialScore = vecs.similarity(word, guess)
        if abs(score - potentialScore) <= error:
            if word.isalnum() and word.islower():
                candidates.append((word, score-potentialScore))

    candidates.sort(key=lambda y: abs(y[1]), reverse=False)

    if len(candidates) > 5:
        candidates = candidates[:5]

    return candidates

def main():
    vecs = loadVec()
    words = [""] * 3000000
    for i in range(3000000):
        words[i] = (vecs.index_to_key[i])

    while True:
        word = input("Entered word: ")
        score = input("Enter its score: ")

        possibilities = getCandidates(word, score, words, vecs)
        print("Guesses:")
        for i, possib in enumerate(possibilities):
            print(f'{i}: {possib}')

if __name__ == "__main__":
    main()

