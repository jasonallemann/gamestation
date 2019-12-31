#
# This file contains the code for controlling the Hot Potato game, which is implemented in the HotPotato class.
#
# The player with the potato is indicated on the game board by the player being moved up a short distance.
#
# Call startGame() to start a game, and endGame() to finish it.
# Call beginRound() and endRound() to play a round.
# The calling code should start the music before calling beginRound() and end the music before calling endRound()
# beginRound() won't return until a random period of time has passed between the minimum and maximum
# times passed into the startGame() function. The calling code can wait longer before calling endRound() if desired.
#
# There are only three rounds to this game, so it is up the calling code to ensure beginRound() and endRound()
# are only called three times.
#
# At any time, the calling code can access the ActivePlayers variable for a list of the players remaining in the game.
#
# For an example of the usage of this class, see the playHotPotato() function in offlineTests.py
#
import sys
import time
import threading
import random

import console

#
# Class to control playing Hot Potato.
#
class HotPotato:
    def __init__( self ):
        self.pototoHeight = 100
        self.ActivePlayers = []

    #
    # The passingThread runs until the music is 'stopped' (when the MusicPlaying variable is False).
    # It continuously waits for the player currently 'holding' the potato to press their button, then
    # 'passes' the potato to the next player.
    #
    def passingThread( self ):
        console.movePlayer( self.currentPlayer, self.pototoHeight )
        console.waitForPlayers()

        while self.MusicPlaying == True:
            console.waitForButton( self.currentPlayer )

            if self.MusicPlaying:
                console.movePlayer( self.currentPlayer, -self.pototoHeight )
                self.currentPlayer = self.nextPlayer( self.currentPlayer )
                console.movePlayer( self.currentPlayer, self.pototoHeight )
                console.waitForPlayers()

    #
    # Starts a game of Hot Potato.
    # Initializes the game board (all players are moved up to the first bar) and game variables.
    # inMin and inMax specify the minimum and maximum time to play the music, in seconds.
    # The actual duration of the music for each round will be a random number of seconds between these two values.
    #
    def startGame( self, inMin, inMax ):
        self.minMusicTime = inMin
        self.maxMusicTime = inMax
        self.MusicPlaying = False
        self.lastPlayer = ""
        self.currentPlayer = ""
        
        console.movePlayer( console.RedPlayer, console.Third )
        console.movePlayer( console.GreenPlayer, console.Third )
        console.movePlayer( console.BluePlayer, console.Third )
        console.movePlayer( console.YellowPlayer, console.Third )
        console.waitForPlayers()

        self.ActivePlayers = [console.RedPlayer, console.GreenPlayer, console.BluePlayer, console.YellowPlayer]

    #
    # Ends the current game.
    # Resets the game board so all the players to the bottom of the board.
    #
    def endGame( self ):
        console.resetPlayers()
        console.waitForPlayers()

    #
    # Begins a round of Hot Potato.
    # 'Starts' the music by setting the MusicPlaying variable to True, then starts the passing thread,
    # which continuously monitors the touch sensors and 'passes' the potato between players.
    # Then waits for a random number of seconds between the minimum and maximum music play times.
    #
    def beginRound( self ):
        self.MusicPlaying = True

        self.currentPlayer = random.choice( self.ActivePlayers )
        self.pt = threading.Thread( target=self.passingThread, daemon=True )
        self.pt.start()

        time.sleep( random.randint( self.minMusicTime, self.maxMusicTime ) )

    #
    # Ends a round of Hot Potato.
    # 'Stops' the music by setting the MusicPlaying variable to False, then waits for the passing thread to finish.
    # Removes the player 'holding' the potato from the active player list.
    #
    def endRound( self ):
        self.MusicPlaying = False
        self.pt.join()

        self.lastPlayer = self.currentPlayer
        self.ActivePlayers.remove( self.lastPlayer )

        console.movePlayer( self.currentPlayer, -console.Third - self.pototoHeight )
#        console.waitForPlayers()

    #
    # Determines who the next player should be.
    # Returns the player to the right of the current one, but could be changed to pick a random player.
    #
    def nextPlayer( self, currentPlayer ):
        index = self.ActivePlayers.index( currentPlayer )
        if index == len( self.ActivePlayers ) - 1:
            index = 0
        else:
            index += 1

        return self.ActivePlayers[index]
    
    #
    # Returns the winning player.
    #
    def winner( self ):
        return self.ActivePlayers[0]
