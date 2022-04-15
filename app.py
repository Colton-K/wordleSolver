#!/usr/bin/python3

from flask import Flask, render_template, request
import semantleClass
import socket

app = Flask(__name__)

solver = semantleClass.SemantleSolver()

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

@app.route("/")  #[#number: word,number: word]
def index():
    #guesses = solver.getCandidates(5)
    guesses = ["number: word","number: word"]
    return render_template(base, guesses=guesses, haveGuesses=(len(guesses)>0))

@app.route("/submitGuess", methods=["POST"])
def submitGuess():
    guess = request.form["guess"]
    score = request.form["score"]
    #  print(f"Received guess, score: {guess} {score}")
    solver.inputGuess(guess, score)

    return index()

@app.route("/reset")
def reset():
    solver.loadVec()
    solver.loadWords()

    return index()

def main():
    solver.loadWords()
    app.run(host=getIP(), port=80)
    pass

if __name__ == "__main__":
    main()

