#
# This file contains the code for controlling the Race to the Top game, which is implemented in the RaceToTheTop class.
#
# Call startGame() to start a game, and endGame() to finish it.
#
# At the end of the game, the calling code can access the orderedPlayers variable to get the finishing order.
#
# For an example of the usage of this class, see the playRaceToTheTop() function in offlineTests.py
#
import sys
import time
import threading
import random

import console

#
# Class to control playing Race to the Top.
#
class RaceToTheTop:
    # Initialize variables.
    def __init__( self ):
        self.PlayingMadDash = False
        self.winCount = 50
        self.motorStep = console.Full / self.winCount

    #
    # Starts a game of Race to the Top.
    # Initializes game variables and starts the main game loop, which continuously polls the button counts
    # and moves the corresponding players up the game board.
    # Once a player reaches the winCount number of presses, the loop exits.
    #
    def startGame( self, winCount ):
        self.orderedPlayers = []
        self.orderedCounts = []

        self.winCount = winCount
        self.motorStep = console.Full / self.winCount

        self.RedCurrent = self.GreenCurrent = self.BlueCurrent = self.YellowCurrent = 0
        console.RedCount = console.GreenCount = console.BlueCount = console.YellowCount = 0
        RPrevious = GPrevious = BPrevious = YPrevious = 0

        self.PlayingMadDash = True
        while self.PlayingMadDash:
            time.sleep( 0.5 )

            self.RedCurrent = console.RedCount
            self.GreenCurrent = console.GreenCount
            self.BlueCurrent = console.BlueCount
            self.YellowCurrent = console.YellowCount

            # If any of the button counts hits the winCount number of presses, tally the results and set the play flag to False.
            if self.RedCurrent >= self.winCount or self.GreenCurrent >= self.winCount or self.BlueCurrent >= self.winCount or self.YellowCurrent >= self.winCount:
                self.determineOrder( self.RedCurrent, console.RedPlayer )
                self.determineOrder( self.GreenCurrent, console.GreenPlayer )
                self.determineOrder( self.BlueCurrent, console.BluePlayer )
                self.determineOrder( self.YellowCurrent, console.YellowPlayer )
                self.PlayingMadDash = False

#            print( "R {}, G {}, B {}, Y {}".format( self.RedCurrent, self.GreenCurrent, self.BlueCurrent, self.YellowCurrent ), file=sys.stderr  )

            # Update the position of each player on the game board.
            self.RedCurrent = min( self.winCount, self.RedCurrent )
            if self.RedCurrent > RPrevious:
                console.moveRedPlayer( ( self.RedCurrent - RPrevious ) * self.motorStep )
                RPrevious = self.RedCurrent

            self.GreenCurrent = min( self.winCount, self.GreenCurrent )
            if self.GreenCurrent > GPrevious:
                console.moveGreenPlayer( ( self.GreenCurrent - GPrevious ) * self.motorStep )
                GPrevious = self.GreenCurrent

            self.BlueCurrent = min( self.winCount, self.BlueCurrent )
            if self.BlueCurrent > BPrevious:
                console.moveBluePlayer( ( self.BlueCurrent - BPrevious ) * self.motorStep )
                BPrevious = self.BlueCurrent

            self.YellowCurrent = min( self.winCount, self.YellowCurrent )
            if self.YellowCurrent > YPrevious:
                console.moveYellowPlayer( ( self.YellowCurrent - YPrevious ) * self.motorStep )
                YPrevious = self.YellowCurrent

    #
    # Ends a game of Race to the Top.
    # Resets all the players to the bottom of the board.
    #
    def endGame( self ):
        console.resetPlayers()
        console.waitForPlayers()

    #
    # Determine's the order of a player's button count.
    # Inserts the player into the ordered player list.
    #
    def determineOrder( self, count, colour ):
        insertIndex = 0
        for curCount in self.orderedCounts:
            if count > curCount:
                break
            else:
                insertIndex += 1

        self.orderedCounts.insert( insertIndex, count )
        self.orderedPlayers.insert( insertIndex, colour )
