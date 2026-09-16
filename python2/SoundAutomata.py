## Colby Jeffries
## Musical Cellular Automata
## SoundAutomata.py

## Contains the SoundAutomata class. Governs the cellular automata and all
## audio generation.

## Libraries and Dependencies --------------------------------------------------
import time                         ## Used for timing.
import wave                         ## Used to open/save .wav files.
import os                           ## Used for file paths.
import copy                         ## Used for deep copies.
import math                         ## Used for math constants.
import paulstretch                  ## Used to stretch audio.
import random                       ## Used to pick notes to play.

import numpy as np                  ## Used for arrays.
import pygame.mixer as pgm          ## Used to play/initialize audio.
import pygame.sndarray as pgsa      ## Used to create arrays out of sounds.

## -----------------------------------------------------------------------------
## SoundAutomata ---------------------------------------------------------------
## Governs the cellular automata and audio generation.
class SoundAutomata:
    ## Class constructor. Initializes all values.
    def __init__(self, parent, seed = np.random.randint(2,size = (4,4)),
        sound = "sinec4.wav", key = [[0,4,7,12]], lengthAdjusted = False,
            windowSize = 0.5):
        self.parent = parent
        self.gameBoard = seed
        self.lengthAdjusted = lengthAdjusted
        self.windowSize = windowSize
        self.basicNote = sound
        if not os.path.exists(self.basicNote[:-4]):
            os.mkdir(self.basicNote[:-4])
        self.size = len(self.gameBoard[1])
        self.gameBoardTemp = copy.deepcopy(self.gameBoard)
        self.key = key
        self.generateNotes()
        self.noteArray = []
        for i in self.key:
            self.noteArray.append([pgm.Sound(self.basicNote[:-4] + "/" + str(j)
                + ".wav") for j in i])
        self.currentNote = 0
        self.currentKey = 0

    ## Helper function to count the amount of neighbors in a cells Moore
    ## neighborhood.
    def countneighbors(self, x, y):
        count = 0
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                curx = i % self.size
                cury = j % self.size
                if self.organismAt(curx, cury) and (curx != x or cury != y):
                    count += 1

        return count

    ## Returns whether or not there is an alive cell at (x,y).
    def organismAt(self, x, y):
        if self.gameBoard[x][y] == 1:
            return True
        else:
            return False

    ## Function that updates the automata based on the specified 1-D rule.
    def oneDUpdate(self, rule):
        binRule = bin(int(rule))[2:].zfill(8)
        for i in range(self.size):
            prevVal = []
            for j in range(i-1,i+2):
                curj = j % self.size
                prevVal.append(self.organismAt((self.currentNote-1)%self.size,
                    curj))

            while switch(prevVal):
                if case([1,1,1]):
                    self.gameBoardTemp[self.currentNote][i] = binRule[0]
                    break
                if case([1,1,0]):
                    self.gameBoardTemp[self.currentNote][i] = binRule[1]
                    break
                if case([1,0,1]):
                    self.gameBoardTemp[self.currentNote][i] = binRule[2]
                    break
                if case([1,0,0]):
                    self.gameBoardTemp[self.currentNote][i] = binRule[3]
                    break
                if case([0,1,1]):
                    self.gameBoardTemp[self.currentNote][i] = binRule[4]
                    break
                if case([0,1,0]):
                    self.gameBoardTemp[self.currentNote][i] = binRule[5]
                    break
                if case([0,0,1]):
                    self.gameBoardTemp[self.currentNote][i] = binRule[6]
                    break
                if case([0,0,0]):
                    self.gameBoardTemp[self.currentNote][i] = binRule[7]
                    break
                print("The 1D rules broke. What did you do?")
                break

        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## Function to update the automata according to Conway's Game of Life.
    def conwaysUpdate(self):
        for i in range(self.size):
            for j in range(self.size):
                count = self.countneighbors(i,j)
                if self.organismAt(i,j):
                    if count not in [2,3]:
                        self.gameBoardTemp[i][j] = 0
                else:
                    if count == 3:
                        self.gameBoardTemp[i][j] = 1

        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## Function that does not update the cellular automata.
    ## Copies the gameboard.
    def noUpdate(self):
        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## Slides the cellular automata 1 cell to the right on each update.
    def rightUpdate(self):
        for i in range(self.size):
            for j in range(self.size):
                curx = (j-1) % self.size
                if self.organismAt(i,curx):
                    self.gameBoardTemp[i][j] = 1
                else:
                    self.gameBoardTemp[i][j] = 0

        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## Slides the cellular automata 1 cell to the left on each update.
    def leftUpdate(self):
        for i in range(self.size):
            for j in range(self.size):
                curx = (j+1) % self.size
                if self.organismAt(i,curx):
                    self.gameBoardTemp[i][j] = 1
                else:
                    self.gameBoardTemp[i][j] = 0

        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## Slides the cellular automata 1 cell down on each update.
    def downUpdate(self):
        for i in range(self.size):
            for j in range(self.size):
                cury = (i-1) % self.size
                if self.organismAt(cury,j):
                    self.gameBoardTemp[i][j] = 1
                else:
                    self.gameBoardTemp[i][j] = 0

        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## Slides the cellular automata 1 cell up on each update.
    def upUpdate(self):
        for i in range(self.size):
            for j in range(self.size):
                cury = (i+1) % self.size
                if self.organismAt(cury,j):
                    self.gameBoardTemp[i][j] = 1
                else:
                    self.gameBoardTemp[i][j] = 0

        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## Updates the cellular automata according to the rules of Brian's Brain.
    def bBUpdate(self):
        for i in range(self.size):
            for j in range(self.size):
                count = self.countneighbors(i,j)
                while switch(self.gameBoard[i][j]):
                    if case(1):
                        self.gameBoardTemp[i][j] = 2
                        break
                    if case(2):
                        self.gameBoardTemp[i][j] = 0
                        break
                    if case(0):
                        if count == 2:
                            self.gameBoardTemp[i][j] = 1

                        break

        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## Updates the cellular automata according to the rules of seeds.
    def seedsUpdate(self):
        for i in range(self.size):
            for j in range(self.size):
                count = self.countneighbors(i,j)
                if not self.organismAt(i,j):
                    if count == 2:
                        self.gameBoardTemp[i][j] = 1
                else:
                    self.gameBoardTemp[i][j] = 0

        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## Updates the cellular automata according to the rules of Langton's Ant.
    def langtonsUpdate(self):
        for i in range(self.size):
            for j in range(self.size):
                current = self.gameBoard[i][j]
                while switch(current):
                    if case(2):
                        self.gameBoardTemp[i][j] = 0
                        if self.gameBoard[(i+1)%self.size][j] in [0,6,7,8,9]:
                            self.gameBoardTemp[(i+1)%self.size][j] = 9
                        else:
                            self.gameBoardTemp[(i+1)%self.size][j] = 3
                        break
                    if case(3):
                        self.gameBoardTemp[i][j] = 0
                        if self.gameBoard[i][(j-1)%self.size] in [0,6,7,8,9]:
                            self.gameBoardTemp[i][(j-1)%self.size] = 6
                        else:
                            self.gameBoardTemp[i][(j-1)%self.size] = 4
                        break
                    if case(4):
                        self.gameBoardTemp[i][j] = 0
                        if self.gameBoard[(i-1)%self.size][j] in [0,6,7,8,9]:
                            self.gameBoardTemp[(i-1)%self.size][j] = 7
                        else:
                            self.gameBoardTemp[(i-1)%self.size][j] = 5
                        break
                    if case(5):
                        self.gameBoardTemp[i][j] = 0
                        if self.gameBoard[i][(j+1)%self.size] in [0,6,7,8,9]:
                            self.gameBoardTemp[i][(j+1)%self.size] = 8
                        else:
                            self.gameBoardTemp[i][(j+1)%self.size] = 2
                        break
                    if case(6):
                        self.gameBoardTemp[i][j] = 1
                        if self.gameBoard[(i+1)%self.size][j] in [1,2,3,4,5]:
                            self.gameBoardTemp[(i+1)%self.size][j] = 3
                        else:
                            self.gameBoardTemp[(i+1)%self.size][j] = 9
                        break
                    if case(7):
                        self.gameBoardTemp[i][j] = 1
                        if self.gameBoard[i][(j-1)%self.size] in [1,2,3,4,5]:
                            self.gameBoardTemp[i][(j-1)%self.size] = 4
                        else:
                            self.gameBoardTemp[i][(j-1)%self.size] = 6
                        break
                    if case(8):
                        self.gameBoardTemp[i][j] = 1
                        if self.gameBoard[(i-1)%self.size][j] in [1,2,3,4,5]:
                            self.gameBoardTemp[(i-1)%self.size][j] = 5
                        else:
                            self.gameBoardTemp[(i-1)%self.size][j] = 7
                        break
                    if case(9):
                        self.gameBoardTemp[i][j] = 1
                        if self.gameBoard[i][(j+1)%self.size] in [1,2,3,4,5]:
                            self.gameBoardTemp[i][(j+1)%self.size] = 2
                        else:
                            self.gameBoardTemp[i][(j+1)%self.size] = 8
                        break
                    break


        self.gameBoard = copy.deepcopy(self.gameBoardTemp)

    ## General update function. Calls the proper update function based on the
    ## the specified update type.
    def update(self, type, oneDRule):
        while switch(type):
            if case("Conways"):
                self.conwaysUpdate()
                break
            if case("Up"):
                self.upUpdate()
                break
            if case("Down"):
                self.downUpdate()
                break
            if case("Left"):
                self.leftUpdate()
                break
            if case("Right"):
                self.rightUpdate()
                break
            if case("No Update"):
                self.noUpdate()
                break
            if case("1D"):
                self.oneDUpdate(oneDRule)
                break
            if case("Brian's Brain"):
                self.bBUpdate()
                break
            if case("Seeds"):
                self.seedsUpdate()
                break
            if case("Langton's Ant"):
                self.langtonsUpdate()
                break
            print "Not a valid update type."
            break

    ## Speeds up the audio in snd_array by a factor.
    def speedx(self, snd_array, factor):
        indices = np.round(np.arange(0, len(snd_array), factor))
        indices = indices[indices < len(snd_array)].astype(int)
        return snd_array[indices]

    ## Generates audio files of all of the specified pitches based on the
    ## original audio file. Sound length can be normalized.
    def generateNotes(self):
        self.parent.write("Generating notes...")
        for i in range(-36,60):
            for key in self.key:
                if i in key:
                    if not os.path.exists(self.basicNote[:-4] + os.path.sep +
                        str(i) + '.wav'):
                        factor = 2**(1.0 * i / 12.0)
                        if self.lengthAdjusted:
                            (samplerate,smp)=paulstretch.load_wav(
                                self.basicNote)
                            paulstretch.paulstretch(samplerate, smp, factor,
                                self.windowSize,
                                self.basicNote[:-4]+"temp"+".wav")
                            note = pgm.Sound(self.basicNote[:-4]+"temp"+".wav")
                        else:
                            note = pgm.Sound(self.basicNote)

                        note.set_volume(0)
                        note.play()
                        basicNoteArray = pgsa.array(note)
                        basicNoteResampled = []
                        for ch in range(basicNoteArray.shape[1]):
                            sound_channel = basicNoteArray[:,ch]
                            basicNoteResampled.append(np.array(
                                self.speedx(sound_channel, factor)))

                        basicNoteResampled = np.transpose(np.array(
                            basicNoteResampled)).copy(order='C')
                        noteOut = pgsa.make_sound(basicNoteResampled.astype(
                            basicNoteArray.dtype))
                        noteFile = wave.open(self.basicNote[:-4] + os.path.sep +
                            str(i) + '.wav', 'w')
                        noteFile.setframerate(44100)
                        noteFile.setnchannels(2)
                        noteFile.setsampwidth(2)
                        noteFile.writeframesraw(noteOut.get_raw())
                        noteFile.close()
                        self.parent.write(self.parent.notes[
                            i%len(self.parent.notes)] + "(" +
                            str(i//len(self.parent.notes)+5) + ") Generated!")

        if os.path.exists(self.basicNote[:-4]+"temp"+".wav"):
            os.remove(self.basicNote[:-4]+"temp"+".wav")

    ## Plays one time step of the cellular automata.
    def play(self, notelen, num, musicCheck):
        if musicCheck:
            toPlay = []
            for i in range(len(self.gameBoard[self.currentNote])):
                if self.gameBoard[self.currentNote][i] > 0:
                    toPlay.append(i)

            if num > len(toPlay):
                num = len(toPlay)

            n = len(toPlay)-num
            toPlay = toPlay[n//2:len(toPlay)-n//2]
            for j in range(num):
                if self.gameBoard[self.currentNote][toPlay[j]]:
                    self.noteArray[self.currentKey][toPlay[j]%len(
                        self.key[self.currentKey])].set_volume(1/self.gameBoard[
                        self.currentNote][toPlay[j]])
                    self.noteArray[self.currentKey][toPlay[j]%len(self.key[
                        self.currentKey])].play(0, notelen)

        self.currentNote = (self.currentNote + 1) % self.size

    ## Moves the progression forward one chord. Will wrap around.
    def updateKey(self, val):
        self.currentKey = self.parent.progression[val]

## -----------------------------------------------------------------------------
## switch ----------------------------------------------------------------------
## Python switch statement, used in update.
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

## -----------------------------------------------------------------------------
## Main ------------------------------------------------------------------------
## If this file is called as a script. It will tell you not to do that.
if __name__ == "__main__":
    print("Don't run me! Run AutomataApp.py!")
