#!/usr/bin/python3

import gensim
import pickle

wordsfile = "words.pkl"
vecsFile = 'vecs.pkl'

error = .01
numCandidates = 10

def loadVec():
    print("Loading vectors...")
    vecs = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    print("Vectors loaded!")
    return vecs

def getCandidates(guess, score, words, vecs):
    print("Searching...")
    candidates = []
    filteredWords = []
    score = float(score)/100

    for word in words:
        '''
        say guess is beer - 11.7
        check beer vs all other words
            if the similarity is close to 11.7, then it should be a part of the ring around the main word
        '''
        potentialScore = vecs.similarity(word, guess)
        if abs(score - potentialScore) <= error:
            if word.isalnum() and word.islower():
                candidates.append((word, score-potentialScore))
                filteredWords.append(word)

    candidates.sort(key=lambda y: abs(y[1]), reverse=False)

    if len(candidates) > numCandidates:
        candidates = candidates[:numCandidates]

    return filteredWords, candidates

'''
returns up to k number of guesses based on the most recent guess and score
'''
def getKGuesses(guess, score, k):
    pass


def main():
    vecs = loadVec()
    words = [""] * 3000000
    for i in range(3000000):
        words[i] = (vecs.index_to_key[i])

    print("Pruning...")
    actualWords = []
    for word in words:
        if word.isalnum() and word.islower():
            actualWords.append(word)
    words = actualWords
    print("Done pruning!")
        

    while True:
        word = input("Entered word: ")
        score = input("Enter its score: ")

        words, possibilities = getCandidates(word, score, words, vecs)
        print("Guesses:")
        for i, possib in enumerate(possibilities):
            print(f'{i+1}: {possib[0]} {possib[1]}')

if __name__ == "__main__":
    main()

