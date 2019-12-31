#!/usr/bin/env python3
#
# This is the main program for running the game station and communicating with Alexa.
#
# All communication for managing the state of each game is done via events sent to and from the Alexa skill.
#
import os
import sys
import time
import logging
import json
import threading

import console
import musicalChairs
import hotPotato
import simon
import race
import trivia

from agt import AlexaGadget
from ev3dev2.led import Leds

# Set the logging level to INFO to see messages from AlexaGadget
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
logger = logging.getLogger(__name__)

#
# Main gadget class.
#
class MindstormsGadget(AlexaGadget):
    # Initialize the game objects.
    def __init__(self):
        super().__init__()
        console.initialize()
        self.s = simon.Simon()
        self.m = musicalChairs.MusicalChairs()
        self.h = hotPotato.HotPotato()
        self.r = race.RaceToTheTop()
        self.t = trivia.Trivia()

    def on_connected( self, device_addr ):
        logger.info( "{} connected to Echo device".format( self.friendly_name ) )

    def on_disconnected( self, device_addr ):
        logger.info( "{} disconnected from Echo device".format( self.friendly_name ) )

    # Handles the Custom.Mindstorms.Gadget control directive.
    def on_custom_mindstorms_gadget_control( self, directive ):
        try:
            payload = json.loads( directive.payload.decode( "utf-8" ) )
            print( "Control payload: {}".format( payload ), file=sys.stderr )
            controlType = payload["type"]

            #
            # Events for Simon
            #

            # The skill has started a game of Simon.
            # Start the game, then tell the skill to read the first colour sequence.
            if controlType == "simonStartGame":
                self.s.startGame()
                print( "Test Sequence: {}".format( self.s.Sequence ), file=sys.stderr )
                self._send_event( "simonSequence", self.s.Sequence )

            # The skill has read the colour sequence.
            # Test the user, and send the results to the skill. If level 10 was passed, tell the skill
            # to end the game.
            if controlType == "simonTest":
                result = self.s.test()
                if result == True and self.s.CurrentLevel < 11:
                    print( "Test Sequence: {}".format( self.s.Sequence ), file=sys.stderr )
                    self._send_event( "simonSequence", self.s.Sequence )
                else:
                    print( "Actual Sequence: {}".format( self.s.ActualSequence ), file=sys.stderr )
                    endSimonData = { "level": self.s.CurrentLevel - 1, "passed": result }
                    self._send_event( "simonEnd", json.dumps( endSimonData ) )

            # The skill has completed finishing the game.
            if controlType == "simonEndGame":
                time.sleep( 4.0 )
                self.s.endGame()

            #
            # Events for Musical Chairs
            #

            # The skill has started a game of Musical Chairs.
            # Start the game, begin the first round, then tell the skill to stop the music.
            if controlType == "musicalChairsStartGame":
                time.sleep( 2 )
                self.m.startGame( 2, 10 )
                self.m.beginRound()
                self._send_event( "musicalChairsStopMusic", "" )

            # The skill has started the next round.
            # Begin the round, then tell the skill to stop the music.
            if controlType == "musicalChairsNextRound":
                self.m.beginRound()
                self._send_event( "musicalChairsStopMusic", "" )

            # The skill has stopped the music.
            # End the round. If this is the last round, tell the skill the game is finished,
            # otherwise tell the skill the round has finished.
            if controlType == "musicalChairsMusicStopped":
                self.m.endRound()
                if len( self.m.orderedPlayers ) == 2:
                    self._send_event( "musicalChairsFinishedGame", self.m.winner() )
                else:
                    self._send_event( "musicalChairsFinishedRound", self.m.lastPlayer() )

            # The skill has completed finishing the game.
            if controlType == "musicalChairsFinishGame":
                time.sleep( 4.0 )
                self.m.endGame()

            #
            # Events for Hot Potato
            #

            # The skill has started a game of hot potato.
            # Start the game, begin the first round, tell the skill to stop the music.
            if controlType == "hotPotatoStartGame":
                time.sleep( 4 )
                self.h.startGame( 5, 12 )
                time.sleep( 0.5 )
                self.h.beginRound()
                self._send_event( "hotPotatoStopMusic", "" )

            # The skill has started the next round.
            # Begin the round, then tell the skill to stop the music.
            if controlType == "hotPotatoNextRound":
                time.sleep( 3 )
                self.h.beginRound()
                self._send_event( "hotPotatoStopMusic", "" )

            # The skill has stopped the music.
            # End the round. If only 1 player is left, tell the skill the game is finished,
            # otherwise tell the skill the round has finished.
            if controlType == "hotPotatoMusicStopped":
                self.h.endRound()
                print( self.h.ActivePlayers, file=sys.stderr )
                if len( self.h.ActivePlayers ) == 1:
                    self._send_event( "hotPotatoFinishedGame", self.h.winner() )
                else:
                    self._send_event( "hotPotatoFinishedRound", self.h.lastPlayer )

            # The skill has completed finishing the game.
            if controlType == "hotPotatoFinishGame":
                time.sleep( 4 )
                self.h.endGame()

            #
            # Events for Race to the Top
            #

            # The skill has started a game of Race to the Top.
            if controlType == "raceStartGame":
                time.sleep( 4 ) # Give Alexa chance to speak before starting. Doesn't need to be exact.
                self.r.startGame( 50 )
                print( "Race order: {}".format( self.r.orderedPlayers ), file=sys.stderr )
                self._send_event( "raceFinishedGame", self.r.orderedPlayers )

            # The skill has completed finishing the game.            
            if controlType == "raceFinishGame":
                time.sleep( 4 ) # Give Alexa chance to speak before finishing. Doesn't need to be exact.
                self.r.endGame()

            #
            # Events for LEGO Trvia
            #

            # The skill has started a game of Trivia
            if controlType == "triviaStartGame":
                time.sleep( 2 ) # Give Alexa chance to speak before starting. Doesn't need to be exact.
                self.t.startGame()
                result = self.t.randomQuestion()
                print( "Question payload: {}".format( result ), file=sys.stderr )
                self._send_event( "triviaAskQuestion", json.dumps( result ) )

            # The skill has asked the questions, now wait for a player to press their button to answer.
            if controlType == "triviaAskedQuestion":
                player = self.t.waitForPlayer()
                self._send_event( "triviaAskForAnswer", player )

            # The player answered the question correctly, update the display and ask another question.
            # If a play won the game, finish the game.
            if controlType == "triviaCorrectAnswer":
                gameOver = self.t.correctAnswer()
                if gameOver:
                    self._send_event( "triviaFinishedGame", self.t.AnswerPlayer )
                else:
                    result = self.t.randomQuestion()
                    print( "Question payload: {}".format( result ), file=sys.stderr )
                    self._send_event( "triviaAskQuestion", json.dumps( result ) )

            # The player answered incorrectly, see if anyone else want's to answer.
            if controlType == "triviaIncorrectAnswer":
                player = self.t.waitForPlayer()
                self._send_event( "triviaAskForAnswer", player )

            # The skill has completed finishing the game.
            if controlType == "triviaFinishGame":
                time.sleep( 4 ) # Give Alexa chance to speak before finishing. Doesn't need to be exact.
                self.t.endGame()

        except KeyError:
            print( "Missing expected parameters: {}".format( directive ), file=sys.stderr )

    def _send_event(self, name, payload):
        self.send_custom_event( 'Custom.Mindstorms.Gadget', name, payload )

if __name__ == '__main__':
    gadget = MindstormsGadget()

    os.system('setfont Lat7-Terminus12x6')
    Leds().all_off()

    # Gadget main entry point
    gadget.main()
