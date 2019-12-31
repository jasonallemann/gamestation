#!/usr/bin/env python3
#
# This program can be run directly, independent of Alexa, for testing purposes.
# It is useful for running snippets of code to test various aspects of the console.
#
# Predefined functions exist to illustrate the program flow for running the built in games.
#
import os
import sys
import time

import console
import simon
import musicalChairs
import hotPotato
import race

#
# Example function illustrating how to play Simon.
#
def playSimon():
    s = simon.Simon()
    s.startGame()
    print( s.Sequence, file=sys.stderr )
    while s.CurrentLevel < 11 and s.test():
        print( s.Sequence, file=sys.stderr )

    s.endGame()

#
# Example function illustrating how to play Musical Chairs.
#
def playMusicalChairs():
    m = musicalChairs.MusicalChairs()
    m.startGame( 1, 2 )
    
    m.beginRound()
    print( "Round 1", file=sys.stderr )
    m.endRound()
    print( m.orderedPlayers, file=sys.stderr )

    m.beginRound()
    print( "Round 2", file=sys.stderr )
    m.endRound()
    print( m.orderedPlayers, file=sys.stderr )

    m.beginRound()
    print( "Round 3", file=sys.stderr )
    m.endRound()
    print( m.orderedPlayers, file=sys.stderr )

    time.sleep( 1 )
    m.endGame()

#
# Example function illustrating how to play Hot Potato.
#
def playHotPotato():
    h = hotPotato.HotPotato()
    h.startGame( 5, 7 )

    h.beginRound()
    h.endRound()
    print( h.ActivePlayers, file=sys.stderr )

    h.beginRound()
    h.endRound()
    print( h.ActivePlayers, file=sys.stderr )

    h.beginRound()
    h.endRound()
    print( h.ActivePlayers, file=sys.stderr )

    h.endGame()

#
# Example function illustrating how to play Race to the Top.
#
def playRaceToTheTop():
    r = race.RaceToTheTop()
    r.startGame( 50 )
    time.sleep( 1 )
    r.endGame()
    print( "Order: {}".format( r.orderedPlayers ), file=sys.stderr  )
    print( "Counts: {}".format( r.orderedCounts ), file=sys.stderr  )

if __name__ == '__main__':
    console.initialize()
#    playMusicalChairs()
#    playSimon()
#    playHotPotato()
    playRaceToTheTop()
