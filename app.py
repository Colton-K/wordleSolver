#!/usr/bin/python3

from flask import Flask, render_template, request
import socket

import semantleClass
import wordleClass

app = Flask(__name__)


semantleSolver = semantleClass.SemantleSolver()
wordleSolver = wordleClass.WordleSolver()
puzzle = "semantle"

base = 'index.html'

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route("/")
def index():
    guesses = solver.getCandidates(5)
    return render_template(base, guesses=guesses, haveGuesses=(len(guesses)>0))

@app.route("/submitGuess", methods=["POST"])
def submitGuess():
    guess = request.form["guess"]
    score = request.form["score"]
    #  print(f"Received guess, score: {guess} {score}")
    if puzzle == "semantle":
        semantleSolver.inputGuess(guess, score)
    elif puzzle == "wordle":
        wordleSolver.inputGuess(guess, score)

    return index()

@app.route("/reset")
def reset():
    if puzzle == "semantle":
        semantleSolver.loadVec()
        semantleSolver.loadWords()
    elif puzzle == "wordle":
        wordleSolver.readWords()

    return index()

@app.route("/setPuzzle", method=["POST"])
def setPuzzle():
    global puzzle

    suggested = request.form["puzzle"]
    if suggested == "wordle":
        puzzle = "wordle"
    elif suggested == "semantle":
        puzzle = "semantle"
    
    return index()

def main():
    if puzzle == "semantle":
        semantleSolver.loadWords()
    elif puzzle == "wordle":
        wordleSolver.readWords()

    app.run(host=getIP(), port=80)
    pass

if __name__ == "__main__":
    main()

