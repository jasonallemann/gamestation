#
# This file contains the code for controlling the Simon game, which is implemented in the Simon class.
#
# Call startGame() to start a game, and endGame() to finish it.
# Call test() to begin the test for the current level. It will also set up the game variable for the next level.
#
# test() can be called indefinitely to continue playing. It is up to the calling code to limit the levels
# and stop playing if it returns False (indicating user failed to match the sequence).
#
# At any time, the calling code can access the Sequence variable, which is the list of the expected colours for the current level.
#
# For an example of the usage of this class, see the playSimon() function in offlineTests.py
#
import sys
import time
import random

import console

#
# Class to control playing Simon.
#
class Simon:
    def __init__( self ):
        self.CurrentLevel = 0
        self.Sequence = []
        self.ActualSequence = []

    #
    # Starts a game of Simon.
    # Initializes game variables for the first round.
    #
    def startGame( self ):
        self.CurrentLevel = 1
        self.Sequence.clear()
        self.Sequence.append( random.choice( ["red", "green", "blue", "yellow"] ) )
        self.ActualSequence.clear()

    #
    # Ends a game of Simon.
    # Resets all the players to the bottom of the board.
    #
    def endGame( self ):
        console.resetPlayers()
        console.waitForPlayers()

    #
    # Performs the test for the current round, and sets up the variables for the next round.
    # This function will wait for the buttons to be pressed and match the results with the
    # expected results.
    #
    # Returns:
    #   True - if the user correctly matches the sequence of the current level
    #   False - otherwise
    #
    def test( self ):
        console.RedCount = console.GreenCount = console.BlueCount = console.YellowCount = 0
        self.ActualSequence.clear()

        passed = True
        count = 0
        RedPrevious = GreenPrevious = BluePrevious = YellowPrevious = 0
#        motorIncrement = console.Full / 10 / self.CurrentLevel
        motorIncrement = console.Full / 50

        #
        # Loop to test that the next button pressed matches the expected colour.
        # Will stop once all the colours are matched, or if the button is incorrect.
        #
        while count < self.CurrentLevel and passed == True:
            time.sleep( 0.1 )
            if console.RedCount > RedPrevious:
                RedPrevious += 1
                self.ActualSequence.append( "red" )
                if self.Sequence[count] == "red":
                    count += 1
                    console.movePlayer( console.RedPlayer, motorIncrement )
                else:
                    passed = False
            
            if console.GreenCount > GreenPrevious:
                GreenPrevious += 1
                self.ActualSequence.append( "green" )
                if self.Sequence[count] == "green":
                    count += 1
                    console.movePlayer( console.GreenPlayer, motorIncrement )
                else:
                    passed = False
            
            if console.BlueCount > BluePrevious:
                BluePrevious += 1
                self.ActualSequence.append( "blue" )
                if self.Sequence[count] == "blue":
                    count += 1
                    console.movePlayer( console.BluePlayer, motorIncrement )
                else:
                    passed = False
            
            if console.YellowCount > YellowPrevious:
                YellowPrevious += 1
                self.ActualSequence.append( "yellow" )
                if self.Sequence[count] == "yellow":
                    count += 1
                    console.movePlayer( console.YellowPlayer, motorIncrement )
                else:
                    passed = False

        # Increment the level count and add another random colour to the colour sequence.
        self.CurrentLevel += 1
        self.Sequence.append( random.choice( ["red", "green", "blue", "yellow"] ) )
        
        return passed
