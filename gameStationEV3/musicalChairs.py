#
# This file contains the code for controlling the Musical Chairs game, which is implemented in the MusicalChairs class.
#
# When the music 'stops' the last person to press their button is eliminated.
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
# The calling code can access the orderedPlayers variable for an ordered list of the results from the last
# round. Or call winner() or lastPlayer() to get those players from the last round.
#
# For an example of the usage of this class, see the playMusicalChairs() function in offlineTests.py
#
import sys
import time
import threading
import random

import console

#
# Class to control playing  Musical Chairs.
#
class MusicalChairs:
    # These are the thread functions, which wait for each button to be pressed and record the time they were pressed.
    def redButtonTime( self ):
        console.waitForButton( console.RedPlayer )
        self.redTime = time.time()

    def greenButtonTime( self ):
        console.waitForButton( console.GreenPlayer )
        self.greenTime = time.time()

    def blueButtonTime( self ):
        console.waitForButton( console.BluePlayer )
        self.blueTime = time.time()

    def yellowButtonTime( self ):
        console.waitForButton( console.YellowPlayer )
        self.yellowTime = time.time()

    #
    # Starts a game of Musical Chairs.
    # Initializes the game board (all players are moved up to the first bar) and game variables.
    # inMin and inMax specify the minimum and maximum time to play the music, in seconds.
    # The actual duration of the music for each round will be a random number of seconds between these two values.
    #
    def startGame( self, inMin, inMax ):
        self.minMusicTime = inMin
        self.maxMusicTime = inMax

        self.orderedPlayers = []
        self.orderedTimes = []

        console.movePlayer( console.RedPlayer, console.Third )
        console.movePlayer( console.GreenPlayer, console.Third )
        console.movePlayer( console.BluePlayer, console.Third )
        console.movePlayer( console.YellowPlayer, console.Third )
        console.waitForPlayers()

        self.PlayerStatus = { "red": True, "green": True, "blue": True, "yellow": True }

    #
    # Ends the current game.
    # Resets the game board so all the players to the bottom of the board.
    #
    def endGame( self ):
        console.resetPlayers()
        console.waitForPlayers()

    #
    # Begins a round of Musical Chairs.
    # Then waits for a random number of seconds between the minimum and maximum music play times.
    # Then sets the base start time and starts the threads to wait for the button press of
    # each active player.
    #
    def beginRound( self ):
        self.orderedPlayers.clear()
        self.orderedTimes.clear()

        time.sleep( random.randint( self.minMusicTime, self.maxMusicTime ) )

        self.startTime = time.time()
        self.redTime = self.greenTime = self.blueTime = self.yellowTime = 0

        # Start the threads to wait for the active players' buttons to be pressed.
        if self.PlayerStatus["red"] == True:
            self.tRed = threading.Thread( target=self.redButtonTime, daemon=True )
            self.tRed.start()
    
        if self.PlayerStatus["green"] == True:
            self.tGreen = threading.Thread( target=self.greenButtonTime, daemon=True )
            self.tGreen.start()

        if self.PlayerStatus["blue"] == True:
            self.tBlue = threading.Thread( target=self.blueButtonTime, daemon=True )
            self.tBlue.start()

        if self.PlayerStatus["yellow"] == True:
            self.tYellow = threading.Thread( target=self.yellowButtonTime, daemon=True )
            self.tYellow.start()

    #
    # Ends a round of Musical Chairs.
    # Wait for all the active player button threads to finish, then compare their times to the baseline and
    # eliminate the player with the slowest reaction time.
    #
    def endRound( self ):
        # Wait for all the active players buttons to be pressed (by waiting for their threads to finish)
        if self.PlayerStatus["red"] == True:
            self.tRed.join()
            self.determineOrder( self.redTime - self.startTime, "red" )

        if self.PlayerStatus["green"] == True:
            self.tGreen.join()
            self.determineOrder( self.greenTime - self.startTime, "green" )

        if self.PlayerStatus["blue"] == True:
            self.tBlue.join()
            self.determineOrder( self.blueTime - self.startTime, "blue" )

        if self.PlayerStatus["yellow"] == True:
            self.tYellow.join()
            self.determineOrder( self.yellowTime - self.startTime, "yellow" )

        # Eliminate the slowest player (which will be the last player in the ordered player list)
        self.PlayerStatus[ self.orderedPlayers[ len( self.orderedPlayers ) - 1] ] = False
#        print( "Eliminated: {}".format(self.orderedPlayers[ len( self.orderedPlayers ) - 1]), file=sys.stderr )
#        print( self.PlayerStatus, file=sys.stderr )

        console.movePlayer( self.orderedPlayers[ len( self.orderedPlayers ) - 1], -console.Third )
#        console.waitForPlayers()

    #
    # Determine's the order of a player's time.
    # Inserts the player into the ordered player list.
    #
    def determineOrder( self, time, colour ):
        insertIndex = 0
        for curTime in self.orderedTimes:
            if time < curTime:
                break
            else:
                insertIndex += 1

        self.orderedTimes.insert( insertIndex, time )
        self.orderedPlayers.insert( insertIndex, colour )

    #
    # Returns the fastest player, who will be first in the ordered player list.
    #
    def winner( self ):
        return self.orderedPlayers[0]

    #
    # Returns the slowest player, who will be last in the ordered player list.
    #
    def lastPlayer( self ):
        return self.orderedPlayers[len( self.orderedPlayers ) - 1]
