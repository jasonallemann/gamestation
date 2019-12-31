#
# This file contains all the code for managing the console.
#
# This includes functions for moving the players up and down on the game board and
# waiting for players to press their buttons.
#
import sys
import time
import threading
import random

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, LargeMotor

Full = 1200
Quarter = Full / 4
Third = Full / 3
Half = Full / 2
ThreeQuarters = Full * 3 / 4

RedPlayer = "red"
GreenPlayer = "green"
BluePlayer = "blue"
YellowPlayer = "yellow"

MotorSpeed = 50

RedCount = 0
GreenCount = 0
BlueCount = 0
YellowCount = 0

#
# Button count thread functions.
# These functions continuously count the number of button presses for each player when they are running.
#
def redButtonCountThread():
    global RedCount
    while TouchSensor( INPUT_1 ).wait_for_bump( None, 50 ):
        RedCount += 1

def greenButtonCountThread():
    global GreenCount
    while TouchSensor( INPUT_2 ).wait_for_bump( None, 50 ):
        GreenCount += 1

def blueButtonCountThread():
    global BlueCount
    while TouchSensor( INPUT_3 ).wait_for_bump( None, 50 ):
        BlueCount += 1

def yellowButtonCountThread():
    global YellowCount
    while TouchSensor( INPUT_4 ).wait_for_bump( None, 50 ):
        YellowCount += 1

#
# Initialized the console.
# Starts all the button count threads, which run for the duration of gameplay.
#
def initialize():
    threading.Thread( target=redButtonCountThread, daemon=True ).start()
    threading.Thread( target=greenButtonCountThread, daemon=True ).start()
    threading.Thread( target=blueButtonCountThread, daemon=True ).start()
    threading.Thread( target=yellowButtonCountThread, daemon=True ).start()

RedCurrent = GreenCurrent = BlueCurrent = YellowCurrent = 0
RedDistance = GreenDistance = BlueDistance = YellowDistance = 0

# def moveRedPlayer():
#     global RedDistance
#     LargeMotor( OUTPUT_A ).on_for_degrees( SpeedPercent( MotorSpeed ), -RedDistance )

# def moveGreenPlayer():
#     global GreenDistance
#     LargeMotor( OUTPUT_B ).on_for_degrees( SpeedPercent( MotorSpeed ), GreenDistance )

# def moveBluePlayer():
#     global BlueDistance
#     LargeMotor( OUTPUT_C ).on_for_degrees( SpeedPercent( MotorSpeed ), BlueDistance )

# def moveYellowPlayer():
#     global YellowDistance
#     LargeMotor( OUTPUT_D ).on_for_degrees( SpeedPercent( MotorSpeed ), -YellowDistance )

tRed = None
tGreen = None
tBlue = None
tYellow = None

def waitForButton( inPlayer ):
    if inPlayer == RedPlayer:
        TouchSensor( INPUT_1 ).wait_for_bump()
    elif inPlayer == GreenPlayer:
        TouchSensor( INPUT_2 ).wait_for_bump()
    elif inPlayer == BluePlayer:
        TouchSensor( INPUT_3 ).wait_for_bump()
    elif inPlayer == YellowPlayer:
        TouchSensor( INPUT_4 ).wait_for_bump()

def moveRedPlayer( inDistance ):
    global RedCurrent
    LargeMotor( OUTPUT_A ).on_for_degrees( SpeedPercent( MotorSpeed ), -inDistance, True, False )
    RedCurrent += inDistance

def moveGreenPlayer( inDistance ):
    global GreenCurrent
    LargeMotor( OUTPUT_B ).on_for_degrees( SpeedPercent( MotorSpeed ), inDistance, True, False )
    GreenCurrent += inDistance

def moveBluePlayer( inDistance ):
    global BlueCurrent
    LargeMotor( OUTPUT_C ).on_for_degrees( SpeedPercent( MotorSpeed ), inDistance, True, False )
    BlueCurrent += inDistance

def moveYellowPlayer( inDistance ):
    global YellowCurrent
    LargeMotor( OUTPUT_D ).on_for_degrees( SpeedPercent( MotorSpeed ), -inDistance, True, False )
    YellowCurrent += inDistance

def movePlayer( inPlayer, inDistance ):
    global RedCurrent, GreenCurrent, BlueCurrent, YellowCurrent
    global RedDistance, GreenDistance, BlueDistance, YellowDistance
    global tRed, tGreen, tBlue, tYellow

    if inPlayer == "red":
        RedDistance = inDistance
#        tRed = threading.Thread( target=moveRedPlayer, daemon=True )
#        tRed.start()
        LargeMotor( OUTPUT_A ).on_for_degrees( SpeedPercent( MotorSpeed ), -RedDistance, True, False )
        RedCurrent += RedDistance
    elif inPlayer == "green":
        GreenDistance = inDistance
#        tGreen = threading.Thread( target=moveGreenPlayer, daemon=True )
#        tGreen.start()
        LargeMotor( OUTPUT_B ).on_for_degrees( SpeedPercent( MotorSpeed ), GreenDistance, True, False )
        GreenCurrent += GreenDistance
    elif inPlayer == "blue":
        BlueDistance = inDistance
#        tBlue = threading.Thread( target=moveBluePlayer, daemon=True )
#        tBlue.start()
        LargeMotor( OUTPUT_C ).on_for_degrees( SpeedPercent( MotorSpeed ), BlueDistance, True, False )
        BlueCurrent += BlueDistance
    elif inPlayer == "yellow":
        YellowDistance = inDistance
#        tYellow = threading.Thread( target=moveYellowPlayer, daemon=True )
#        tYellow.start()
        LargeMotor( OUTPUT_D ).on_for_degrees( SpeedPercent( MotorSpeed ), -YellowDistance, True, False )
        YellowCurrent += YellowDistance

def resetPlayers():
    global RedCurrent, GreenCurrent, BlueCurrent, YellowCurrent
    global RedDistance, GreenDistance, BlueDistance, YellowDistance
    global tRed, tGreen, tBlue, tYellow

    if RedCurrent != 0:
        RedDistance = -RedCurrent
        print( RedDistance, file=sys.stderr )
#        tRed = threading.Thread( target=moveRedPlayer, daemon=True )
#        tRed.start()
        LargeMotor( OUTPUT_A ).on_for_degrees( SpeedPercent( MotorSpeed ), -RedDistance, True, False )
        RedCurrent = 0
    if GreenCurrent != 0:
        GreenDistance = -GreenCurrent
#        tGreen = threading.Thread( target=moveGreenPlayer, daemon=True )
#        tGreen.start()
        LargeMotor( OUTPUT_B ).on_for_degrees( SpeedPercent( MotorSpeed ), GreenDistance, True, False )
        GreenCurrent = 0
    if BlueCurrent != 0:
        BlueDistance = -BlueCurrent
#        tBlue = threading.Thread( target=moveBluePlayer, daemon=True )
#        tBlue.start()
        LargeMotor( OUTPUT_C ).on_for_degrees( SpeedPercent( MotorSpeed ), BlueDistance, True, False )
        BlueCurrent = 0
    if YellowCurrent != 0:
        YellowDistance = -YellowCurrent
#        tYellow = threading.Thread( target=moveYellowPlayer, daemon=True )
#        tYellow.start()
        LargeMotor( OUTPUT_D ).on_for_degrees( SpeedPercent( MotorSpeed ), -YellowDistance, True, False )
        YellowCurrent = 0

def waitForPlayers():
    global tRed, tGreen, tBlue, tYellow
    global RedCurrent

#    print( RedCurrent, file=sys.stderr )

    LargeMotor( OUTPUT_A ).wait_until_not_moving()
    LargeMotor( OUTPUT_B ).wait_until_not_moving()
    LargeMotor( OUTPUT_C ).wait_until_not_moving()
    LargeMotor( OUTPUT_D ).wait_until_not_moving()
    # if tRed != None:
    #     tRed.join()
    # if tGreen != None:
    #     tGreen.join()
    # if tBlue != None:
    #     tBlue.join()
    # if tYellow != None:
    #     tYellow.join()
