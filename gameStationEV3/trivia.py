#
# This file contains the code for controlling the Trivia game, which is implemented in the Trivia class.
#
# Call startGame() to start a game, and endGame() to finish it.
# Call randomQuestion() to get the next question.
#
# After a question is asked, call waitForPlayer() to wait for a player to press their button.
#
# If the player correctly answers the question, call correctAnswer() to update their score.
#
import sys
import time
import random
import json
import threading

import console

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor

#
# Class to control playing Trivia.
#
class Trivia:
    def __init__( self ):
        self.rThread = threading.Thread( target=self.redButtonWait, daemon=True )
        self.gThread = threading.Thread( target=self.greenButtonWait, daemon=True )
        self.bThread = threading.Thread( target=self.blueButtonWait, daemon=True )
        self.yThread = threading.Thread( target=self.yellowButtonWait, daemon=True )

        self.playerScores = { console.RedPlayer:0, console.GreenPlayer:0, console.BluePlayer:0, console.YellowPlayer:0 }

    # These are the thread functions to waiting for each button to be pressed and record the time they were pressed.
    def redButtonWait( self ):
        TouchSensor( INPUT_1 ).wait_for_bump()
        if self.WaitingForButton:
            self.AnswerPlayer = console.RedPlayer
            self.WaitingForButton = False

    def greenButtonWait( self ):
        TouchSensor( INPUT_2 ).wait_for_bump()
        if self.WaitingForButton:
            self.AnswerPlayer = console.GreenPlayer
            self.WaitingForButton = False

    def blueButtonWait( self ):
        TouchSensor( INPUT_3 ).wait_for_bump()
        if self.WaitingForButton:
            self.AnswerPlayer = console.BluePlayer
            self.WaitingForButton = False

    def yellowButtonWait( self ):
        TouchSensor( INPUT_4 ).wait_for_bump()
        if self.WaitingForButton:
            self.AnswerPlayer = console.YellowPlayer
            self.WaitingForButton = False

    #
    # Starts a game of Trivia.
    # Loads the questions from the file and resets the players scores.
    #
    def startGame( self ):
        try:
            f = open( "triviaQuestions.json", "r" )
        except FileNotFoundError:
            self.TriviaQuestions = [ { "questions":"none" } ]
        else:   
            contents = f.read()
            questionData = json.loads( contents )
            self.TriviaQuestions = questionData["questions"]
#            print( "Trivia Questions: {}".format( self.TriviaQuestions ), file=sys.stderr )
            f.close()

        self.playerScores[console.RedPlayer] = 0
        self.playerScores[console.GreenPlayer] = 0
        self.playerScores[console.BluePlayer] = 0
        self.playerScores[console.YellowPlayer] = 0

    #
    # Ends a game of Trivia.
    # Resets all the players to the bottom of the board.
    #
    def endGame( self ):
        console.resetPlayers()
        console.waitForPlayers()

    #
    # Get a random question.
    # Chooses a random question to return, and removes it from the list so it is not asked again.
    #
    def randomQuestion( self ):
        length = len( self.TriviaQuestions )
        questionIndex = random.randint( 0, length - 1 )

        question = self.TriviaQuestions[questionIndex]
        self.TriviaQuestions.remove( question )

        return question

    #
    # Waits for any player to press a button.
    #
    def waitForPlayer( self ):
        # Make sure all the player button threads are started.
        if not self.rThread.isAlive():
            self.rThread = threading.Thread( target=self.redButtonWait, daemon=True )
            self.rThread.start()
        
        if not self.gThread.isAlive():
            self.gThread = threading.Thread( target=self.greenButtonWait, daemon=True )
            self.gThread.start()

        if not self.bThread.isAlive():
            self.bThread = threading.Thread( target=self.blueButtonWait, daemon=True )
            self.bThread.start()

        if not self.yThread.isAlive():
            self.yThread = threading.Thread( target=self.yellowButtonWait, daemon=True )
            self.yThread.start()

        self.WaitingForButton = True
        while self.WaitingForButton:
            pass

        return self.AnswerPlayer

    #
    # The player made a correct answer.
    # Move the player up the board, and check to see if the game has ended (they have correctly answered 3 questions.)
    #
    def correctAnswer( self ):
        gameOver = False
        self.playerScores[self.AnswerPlayer] += 1
        console.movePlayer( self.AnswerPlayer, console.Third )

        if self.playerScores[self.AnswerPlayer] == 3:
            gameOver = True

        return gameOver
