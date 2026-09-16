## Colby Jeffries
## Musical Cellular Automata
## AutomataApp.py

## This is the main driver, and container for the AutomataApp.

## Libraries and Dependencies --------------------------------------------------
import SoundAutomata        ## SoundAutomata Library
import pygame.mixer         ## Used to play audio.
import random               ## Used for random numbers and selection.
import time                 ## Used for timing.
import copy                 ## Used for deep copies.
import shutil               ## Used to delete files
import tkFileDialog         ## Used to prompt for file selection.
import os                   ## Used for files and paths.
import re                   ## Used to check for valid HEX codes.

import Tkinter as tk        ## GUI package.
import numpy as np          ## Used for arrays.

## -----------------------------------------------------------------------------
## MainApplication -------------------------------------------------------------
## Primary class that contains the GUI.
class MainApplication(tk.Frame):
    ## MainApplication constructor. Creates all of the interface pieces and
    ## 'global' variables.
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.canvasSize = 450
        self.notes = ["C", "C#/Df", "D", "D#/Ef", "E", "F", "F#/Gf", "G",
            "G#/Af", "A", "A#/Bf", "B"]
        self.progressions = ["Custom", "Blues", "Two-Chord", "Three-Chord",
            "32 Bar"]
        self.colors = ["grey", "#2579E7"]
        self.seedSize = 6
        self.progression = [0]
        self.files = set([])
        self.seed = np.zeros((self.seedSize,self.seedSize))
        self.file = os.getcwd() + os.path.sep + "pizzicatoc4.wav"
        self.bpm = tk.StringVar(self, value="300")
        self.noteLengthMin = tk.StringVar(self, value="1000")
        self.noteLengthMax = tk.StringVar(self, value="2000")
        self.noteLengthStep = tk.StringVar(self, value="500")
        self.options = ["Conways", "Up", "Down", "Left", "Right", "No Update",
            "1D", "Brian's Brain", "Seeds", "Langton's Ant"]
        self.updateType = tk.StringVar(self, value = self.options[0])
        self.oneDRule = tk.StringVar(self, value = "30")
        self.key = [[-5, -1, 2, 7, 14, 19]]
        self.seedSelect = tk.Canvas(self, width = self.canvasSize,
            height = self.canvasSize)
        self.seedSelect.grid(row = 0, column = 0, sticky="nsew", padx = 5,
            pady = 5, rowspan = 5, columnspan = 5)
        self.cellwidth = self.canvasSize/self.seedSize
        self.seedSelectArray = {}
        ## Generate black seed array.
        for column in range(self.seedSize):
            for row in range(self.seedSize):
                x1 = column * self.cellwidth
                y1 = row * self.cellwidth
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellwidth
                self.seedSelectArray[row,column] = (
                    self.seedSelect.create_rectangle(x1,y1,x2,y2, fill="grey",
                    tags="rect"+str(row)+str(column)))

        self.seedSizeScale = tk.Scale(self, from_=2, to_=50,
            variable=self.seedSize, tickinterval =48, orient="horizontal",
            command=self.resetSeed)
        self.seedSizeScale.set(6)
        self.seedSizeScale.grid(row = 5, column = 0, columnspan = 6,
            sticky = "nsew")
        self.seedSizeLabel = tk.Label(self, text="Board Size")
        self.seedSizeLabel.grid(row = 6, column = 0, columnspan = 6,
            sticky ="nsew")
        self.createButton = tk.Button(self, text="Create", command=self.create)
        self.createButton.grid(row = 0, column = 5, rowspan = 3, sticky="nsew")
        self.resetButton = tk.Button(self, text="Reset",
            command=self.reset)
        self.resetButton.grid(row = 3, column = 5, sticky="nsew")
        self.randomizeButton = tk.Button(self, text="Randomize",
            command=self.randomize)
        self.randomizeButton.grid(row = 4, column = 5, sticky="nsew")
        self.updateOptions = tk.OptionMenu(self, self.updateType, *self.options,
            command = self.enableExtraOptions)
        self.updateOptions.grid(row = 11, column = 0, columnspan = 2,
            sticky="nsew")
        self.updateOptionsLabel = tk.Label(self, text="Update Rule")
        self.updateOptionsLabel.grid(row = 11, column = 2, sticky = "nsw")
        self.updateOptionsEntry = tk.Entry(self, textvariable=self.oneDRule,
            text=self.oneDRule, state = "disabled")
        self.updateOptionsEntry.grid(row = 11, column = 3, sticky="nsew",
            columnspan = 2)
        self.updateOptionsLabel2 = tk.Label(self, text="1D Rule")
        self.updateOptionsLabel2.grid(row = 11, column = 5, sticky="nsw")
        self.selectKey = tk.Button(self, text="Select Notes",
            command=self.selectNotes)
        self.selectKey.grid(row = 8, column = 0, columnspan = 2, sticky ="nsew")
        self.keyOptionVal = tk.StringVar(self, "Single Chord")
        self.multipleKeyOptions = tk.OptionMenu(self, self.keyOptionVal,
            *["Single Chord", "Multiple Chords", "Generated Chords"],
            command=self.enableMultiKey)
        self.multipleKeyOptions.grid(row = 8, column = 2, sticky = "nsew")
        self.keyEntryVal = tk.IntVar(self, 1)
        self.keyEntryVal.trace("w", self.updateMultiKey)
        self.keyEntry = tk.Entry(self, textvariable=self.keyEntryVal,
            state="disabled")
        self.keyEntry.grid(row = 8, column = 3, columnspan = 2, sticky ="nsew")
        self.keyEntryLabel = tk.Label(self, text="Chords")
        self.keyEntryLabel.grid(row = 8, column = 5, sticky="nsw")
        self.selectKeyVal = tk.StringVar(self, self.notes[0])
        self.selectKeyVal.trace("w", self.updateKey)
        self.selectKeyMenu = tk.OptionMenu(self, self.selectKeyVal, *self.notes)
        self.selectKeyMenu.configure(state = "disabled")
        self.selectKeyMenu.grid(row = 10, column = 0, columnspan = 2,
            sticky = "nsew")
        self.selectKeyMenuLabel = tk.Label(self, text = "Key")
        self.selectKeyMenuLabel.grid(row = 10, column = 2, sticky = "nsw")
        self.selectProgVal = tk.StringVar(self, self.progressions[0])
        self.selectProgVal.trace("w", self.updateKey)
        self.selectProgressionMenu = tk.OptionMenu(self, self.selectProgVal,
            *self.progressions)
        self.selectProgressionMenu.configure(state = "disabled")
        self.selectProgressionMenu.grid(row = 10, column = 3, columnspan = 2,
            sticky = "nsew")
        self.selectProgressionMenuLabel = tk.Label(self, text = "Progression")
        self.selectProgressionMenuLabel.grid(row = 10, column = 5,
            sticky = "nsw")
        self.selectFile = tk.Button(self, text="Select Sound",
            command=self.selectFile)
        self.selectFile.grid(row = 7, column = 0, columnspan = 2,
            sticky ="nsew")
        self.selectFileLabel = tk.Label(self,
            text=self.file.split(os.path.sep)[-1])
        self.selectFileLabel.grid(row = 7, column = 2, columnspan = 3,
            sticky ="nsew")
        self.lengthCheckVal = tk.IntVar(self, 0)
        self.lengthCheck = tk.Checkbutton(self, text="Normalize Length?",
            variable = self.lengthCheckVal, command = self.enableWindow)
        self.lengthCheck.grid(row = 12, column = 3, sticky="nsw")
        self.playCheckVal = tk.IntVar(self, 1)
        self.playCheck = tk.Checkbutton(self, text="Play notes?",
            variable = self.playCheckVal)
        self.playCheck.grid(row = 13, column = 3, sticky="nsw")
        self.windowSizeVal = tk.DoubleVar(self, 0.5)
        self.windowSizeVal.trace("w", self.wipe)
        self.windowSizeEntry = tk.Entry(self, textvariable = self.windowSizeVal,
            state = "disabled")
        self.windowSizeEntry.grid(row = 12, column = 0, sticky ="nsew",
            columnspan = 2)
        self.windowSizeLabel = tk.Label(self, text="Window Size")
        self.windowSizeLabel.grid(row = 12, column = 2, sticky ="nsw")
        self.cyclesEntryVal = tk.IntVar(self,10)
        self.cyclesEntry = tk.Entry(self, textvariable = self.cyclesEntryVal)
        self.cyclesEntry.grid(row = 13, column = 0, sticky = "nsew",
            columnspan = 2)
        self.cyclesLabel = tk.Label(self, text = "Cycles")
        self.cyclesLabel.grid(row = 13, column = 2, sticky = "nsw")
        self.bpmEntry = tk.Entry(self, textvariable=self.bpm, text=self.bpm)
        self.bpmEntry.grid(row = 14, column = 0, sticky="nsew", columnspan = 2)
        self.bpmLabel = tk.Label(self, text="BPM")
        self.bpmLabel.grid(row = 14, column = 2, sticky="nsw")
        self.noteLengthMinEntry = tk.Entry(self,
            textvariable=self.noteLengthMin, text=self.noteLengthMin)
        self.noteLengthMinEntry.grid(row = 15, column = 0, sticky="nsew",
            columnspan = 2)
        self.noteLengthMinLabel = tk.Label(self, text="Length Min (ms)")
        self.noteLengthMinLabel.grid(row = 15, column = 2, sticky="nsw")
        self.noteLengthMaxEntry = tk.Entry(self,
            textvariable=self.noteLengthMax, text=self.noteLengthMax)
        self.noteLengthMaxEntry.grid(row = 15, column = 3, sticky="nsew",
            columnspan = 2)
        self.noteLengthMaxLabel = tk.Label(self, text="Length Max (ms)")
        self.noteLengthMaxLabel.grid(row = 15, column =5, sticky="nsw")
        self.noteLengthStepEntry = tk.Entry(self,
            textvariable=self.noteLengthStep, text=self.noteLengthStep)
        self.noteLengthStepEntry.grid(row = 17, column = 0, sticky="nsew",
            columnspan = 2)
        self.noteLengthStepLabel = tk.Label(self, text="Length Step (ms)")
        self.noteLengthStepLabel.grid(row = 17, column = 2, sticky="nsw")
        self.debugFrame = tk.LabelFrame(root, text="Debug Output")
        self.selectColorsButton = tk.Button(self, text="Select Colors",
            command=self.selectColors)
        self.selectColorsButton.grid(row = 17, column = 3, columnspan = 2,
            sticky="nsew")
        self.notesToPlay = 6
        self.toPlayScale = tk.Scale(self, from_=1, to_=6, tickinterval = 5,
            orient="horizontal")
        self.toPlayScale.set(6)
        self.toPlayScale.grid(row = 18, column = 0, columnspan = 6,
            sticky = "nsew")
        self.toPlayLabel = tk.Label(self, text="Notes to play")
        self.toPlayLabel.grid(row=19, column=0, columnspan = 6,
            sticky = "nsew")
        self.debugFrame.grid(row=20, column=0, columnspan=5, sticky='nsew')
        self.consoleOutput = tk.Text(self.debugFrame, background="black",
            font=("mono", 11), width = 50, height=7,
            foreground='white', state=tk.DISABLED)
        self.consoleOutput.grid(row=0, column=0, sticky='nsew')
        self.scrollbar = tk.Scrollbar(self.debugFrame,
            command=self.consoleOutput.yview)
        self.scrollbar.grid(row=0, column=1, sticky='nsew')
        self.consoleOutput['yscrollcommand'] = self.scrollbar.set
        self.debugFrame.columnconfigure(0, weight=1)
        self.progressionEntryVal = tk.StringVar(self, "0")
        self.progressionEntryVal.trace("w", self.updateProgression)
        self.progressionEntry = tk.Entry(self,
            textvariable=self.progressionEntryVal,
            text=self.progressionEntryVal, state = "disabled")
        self.progressionEntry.grid(row = 9, column = 0, columnspan = 5,
            sticky = "nsew")
        self.progressionEntryLabel = tk.Label(self, text="Progression")
        self.progressionEntryLabel.grid(row = 9, column = 5, sticky = "nsw")

    ## Function that updates the notes and chords for the Automata
    ## when a new key or progression is selected in the generated chords mode.
    def updateKey(self, *args):
        self.key = []
        key = self.notes.index(self.selectKeyVal.get())
        scale = [key, (key+2)%12, (key+4)%12, (key+5)%12, (key+7)%12, (key+9)%12
            , (key+11)%12]
        for i in range(len(scale)):
            chord = [scale[i], scale[(i+2)%7], scale[(i+4)%7]]
            chords = [scale[i]-24]
            for j in range(-1,3):
                map(chords.append, [k + (j*12) for k in chord])
            self.key.append(chords)

        while switch(self.selectProgVal.get()):
            if case("Blues"):
                self.progressionEntry.configure(state="disabled")
                self.progression = [0,0,0,0,3,3,0,0,4,3,0,0]
                break
            if case("Two-Chord"):
                self.progressionEntry.configure(state="disabled")
                self.progression = [0, random.choice([2,4])]
                break
            if case("Three-Chord"):
                self.progressionEntry.configure(state="disabled")
                other = random.choice((range(1,4)+[6]))
                self.progression = random.choice([[0, other, 4, 4],
                    [0, 0, other, 4], [0, other, 0, 4], [0, other, 4, other]])
                break
            if case("32 Bar"):
                self.progressionEntry.configure(state="disabled")
                choices = [[0, random.choice((range(1,4)+[6])), 4, 4],
                    [0, 0, random.choice((range(1,4)+[6])), 4],
                    [0, random.choice((range(1,4)+[6])), 0, 4],
                    [0, random.choice((range(1,4)+[6])), 4,
                    random.choice((range(1,4)))]]
                first = random.choice(choices)
                choices.remove(first)
                second = random.choice(choices)
                self.progression = first + first + second + first
                break
            if case("Custom"):
                self.progressionEntry.configure(state="normal")
                self.progressionEntryVal.set(str(self.progression)[1:-1])
                break

    ## Function that enables the window size entry box when normalize
    ## length is checked.
    def enableWindow(self, *args):
        self.wipe()
        if self.lengthCheckVal.get():
            self.windowSizeEntry.configure(state = "normal")
        else:
            self.windowSizeEntry.configure(state = "disabled")

    ## Function that updates the progression when the progression entry box is
    ## changed.
    def updateProgression(self, *args):
        try:
            self.progression = self.progressionEntryVal.get().split(",")
            self.progression = map(int, self.progression)
        except:
            pass

    ## Function that changes the key length based on mode and how many chords
    ## are selected.
    def updateMultiKey(self, *args):
        try:
            if self.keyEntryVal.get() > len(self.key):
                for i in range(self.keyEntryVal.get() - len(self.key)):
                    self.key.append(self.key[0])
            else:
                if self.keyEntryVal.get() == 0:
                    self.write("Cannot have 0 chords, setting to 1.")
                    self.keyEntryVal.set(1)

                self.key = self.key[:self.keyEntryVal.get()]
        except:
            pass

    ## Function that changes GUI widget states based on what mode is selected.
    def enableMultiKey(self, selection):
        while switch(selection):
            if case("Multiple Chords"):
                self.selectProgressionMenu.configure(state = "disabled")
                self.selectKeyMenu.configure(state = "disabled")
                self.keyEntry.configure(state="normal")
                self.progressionEntry.configure(state="normal")
                break
            if case("Single Chord"):
                self.selectProgressionMenu.configure(state = "disabled")
                self.selectKeyMenu.configure(state = "disabled")
                self.keyEntry.configure(state="disabled")
                self.progressionEntry.configure(state="disabled")
                self.progression = [0]
                self.key = [self.key[0]]
                break
            if case("Generated Chords"):
                self.selectProgressionMenu.configure(state = "normal")
                self.keyEntry.configure(state="disabled")
                self.progressionEntry.configure(state="disabled")
                self.selectKeyMenu.configure(state = "normal")
                self.updateKey()
                break

    ## Function that opens the ColorSelectWindow when the corresponding
    ## button is pressed.
    def selectColors(self):
        self.write("Select colors...")
        newwin = ColorSelectWindow(self)
        self.wait_window(newwin)

    ## Writes the input string into the console output window.
    def write(self, string):
        self.consoleOutput["state"] = tk.NORMAL
        self.consoleOutput.insert(tk.END, string + "\n")
        self.consoleOutput.see(tk.END)
        self.consoleOutput["state"] = tk.DISABLED

    ## Function that resets the seed.
    def reset(self):
        self.resetSeed(self.seedSize)
        self.write("Seed reset!")

    ## Function that changes multiple GUI widgets based on mode and
    ## update selections.
    def enableExtraOptions(self, selection):
        self.reset()
        if selection == "1D":
            self.updateOptionsEntry.config(state="normal")
            self.colors = ["grey", "#2579E7"]
        elif selection == "Brian's Brain":
            self.colors.append("#1E1E1E")
        elif selection == "Langton's Ant":
            self.colors = ["grey", "#2579E7"]
            for i in range(8):
                self.colors.append("#00FF00")

        else:
            self.updateOptionsEntry.config(state="disabled")
            self.colors = ["grey", "#2579E7"]

    ## Cleans up all extra files generated during runtime.
    def wipe(self, *args):
        if not self.files == set():
            for i in self.files:
                if os.path.exists(i[:-4]):
                    shutil.rmtree(i[:-4])
                self.files = set([])

    ## Function that opens a window to select the audio file to be used
    ## by the automata.
    def selectFile(self):
        self.write("Select a file...")
        self.file = tkFileDialog.askopenfilename(initialdir = os.getcwd(),
            title = "Select a Sound", filetypes = [("Microsoft WAV", "*.wav")])
        while self.file == () or self.file == "":
            self.write("No file selected, Select a file...")
            self.file = tkFileDialog.askopenfilename(initialdir = os.getcwd(),
                title = "Select a Sound",
                filetypes = [("Microsoft WAV", "*.wav")])
        self.selectFileLabel.config(text = self.file.split(os.path.sep)[-1])

    ## Function that opens the NoteSelectWindow when the corresponding
    ## button is pressed.
    def selectNotes(self):
        self.write("Select new notes...")
        for i in range(len(self.key)):
            newwin = NotesSelectWindow(self, i)
            self.wait_window(newwin)

    ## Function that randomizes the seed.
    def randomize(self):
        self.write("Seed randomized!")
        for row in range(self.seedSize):
            for column in range(self.seedSize):
                self.seed[row][column] = random.choice(range(2))
                self.seedSelect.itemconfig(self.seedSelectArray[row,column],
                        fill=self.colors[int(self.seed[row][column])])

    ## Function that resets the seed and redraws it if the size has been
    ## changed.
    def resetSeed(self, newSize):
        newSize = int(newSize)
        self.seedSize = int(newSize)
        self.cellwidth = self.canvasSize/self.seedSize
        self.seed = np.zeros((self.seedSize,self.seedSize))
        self.seedSelectArray = {}
        self.seedSelect.delete("all");
        self.toPlayScale.configure(to_=newSize)
        self.toPlayScale.configure(tickinterval=newSize-1)
        self.toPlayScale.set(newSize)
        for column in range(self.seedSize):
            for row in range(self.seedSize):
                x1 = column * self.cellwidth
                y1 = row * self.cellwidth
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellwidth
                self.seedSelectArray[row,column] = (
                    self.seedSelect.create_rectangle(x1,y1,x2,y2, fill="grey",
                    tags="rect"+str(row)+ "x" +str(column)))
                self.seedSelect.tag_bind(self.seedSelectArray[row,column],
                    '<ButtonPress-1>', lambda event,
                    var=(row,column) :self.onObjectClick(event,var))

    ## Function that creates an instance of the SoundAutomata and
    ## VisualizerWindow classes and drives their execution. Primary function.
    def create(self):
        self.write("Initializing new Musical Automata...")
        if self.keyOptionVal.get() == "Generated Chords":
            self.updateKey()
        if self.updateType.get() == "1D":
            if int(self.oneDRule.get()) > 255 or int(self.oneDRule.get()) < 0:
                self.oneDRule.set(30)
                self.write("There are only 0-255 rules! Resetting to default.")
        window = VisualizerWindow(self, self.seed, self.seedSize,
            self.cellwidth)
        self.parent.update()
        bpm = float(60)/float(self.bpmEntry.get())
        start_time = 0
        self.files.add(self.file)
        soundGenerator = SoundAutomata.SoundAutomata(self, self.seed, self.file,
            self.key, self.lengthCheckVal.get(), self.windowSizeVal.get())
        progPos = 0
        for i in range(self.cyclesEntryVal.get()):
            if len(self.key) <= max(self.progression):
                self.write("Not enough chords for the progression!")
                break
            try:
                for j in range(self.seedSize):
                    window.update(soundGenerator.gameBoard,
                        (soundGenerator.currentNote-1)%self.seedSize)
                    while (time.time() - start_time) < bpm:
                        pass

                    soundGenerator.play(random.choice(range(int(
                        self.noteLengthMin.get()),
                        int(self.noteLengthMax.get())+1,
                        int(self.noteLengthStep.get()))),
                        self.toPlayScale.get(), self.playCheckVal.get())

                    start_time = time.time()
                    if (self.updateType.get() == "1D" or self.updateType.get()
                        == "Langton's Ant"):
                        soundGenerator.update(self.updateType.get(),
                            self.oneDRule.get())

                if not (self.updateType.get() == "1D" or self.updateType.get()
                    == "Langton's Ant"):
                    soundGenerator.update(self.updateType.get(),
                        self.oneDRule.get())
                if self.keyOptionVal.get() != "Single Chord":
                    progPos = (progPos + 1)%len(self.progression)
                    soundGenerator.updateKey(progPos)
            except Exception as e:
                pass

        window.destroy()

    ## Callback function that adjusts the seed when a box is clicked.
    def onObjectClick(self, event, (row, column)):
        self.seed[row][column] = (self.seed[row][column] + 1) % len(self.colors)
        event.widget.itemconfigure("rect"+str(row)+"x"+str(column),
            fill = self.colors[int(self.seed[row][column])])

    ## Function that updates the current seed in case of color changes.
    def updateCurrentSeed(self):
        for i in range(self.seedSize):
            for j in range(self.seedSize):
                self.seedSelect.itemconfigure("rect"+str(i)+"x"+str(j),
                    fill=self.colors[int(self.seed[i][j])])

    ## Overload of the destroy function. Calls the wipe function to clean up
    ## all files created during runtime when the application is closed.
    def destroy(self):
        self.wipe()
        self.quit()


## -----------------------------------------------------------------------------
## VisualizerWindow ------------------------------------------------------------
## Class that governs the visualizer of the cellular automata.
class VisualizerWindow(tk.Toplevel):
    ## Class constructor. Initializes values and GUI elements.
    def __init__(self, parent, seed, seedSize, cellwidth):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.seed = seed
        self.cellwidth = cellwidth
        self.seedSize = seedSize
        self.visualizer = tk.Canvas(self, width = self.parent.canvasSize,
            height = self.parent.canvasSize)
        self.visualizerArray = {}
        self.visualizerSeed = copy.deepcopy(self.seed)
        self.visualizer.pack()
        for column in range(self.seedSize):
            for row in range(self.seedSize):
                x1 = column * self.cellwidth
                y1 = row * self.cellwidth
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellwidth
                self.visualizerArray[row,column] = (
                    self.visualizer.create_rectangle(x1,y1,x2,y2,
                    fill=self.parent.colors[int(self.seed[row][column])],
                    tags="rectVis"+str(row)+str(column)))

    ## Updates the visual based on changes caused by cellular automata changes.
    def update(self, newSeed, currentNote):
        for row in range(self.seedSize):
            for column in range(self.seedSize):
                if newSeed[row][column]:
                    self.visualizer.itemconfig(self.visualizerArray[row,column],
                        fill=self.parent.colors[int(newSeed[row][column])])
                else:
                    if row == currentNote:
                        self.visualizer.itemconfig(
                            self.visualizerArray[row,column], fill="yellow")
                    else:
                        self.visualizer.itemconfig(
                            self.visualizerArray[row,column],
                            fill=self.parent.colors[0])

        self.parent.parent.update()


## -----------------------------------------------------------------------------
## NotesSelect -----------------------------------------------------------------
## Class that governs the window to select new notes.
class NotesSelectWindow(tk.Toplevel):
    ## Intializes all values and GUI elements.
    def __init__(self, parent, val):
        tk.Toplevel.__init__(self, parent)
        self.wm_title("Select Key/Chord " + str(val+1))
        self.parent = parent
        self.val = val
        self.noteArray = []
        self.noteCheckArray = []
        self.octaveLabelArray = []
        for i in range(-36,60):
            if i in self.parent.key[val]:
                self.noteArray.append(tk.IntVar(self, 1))
            else:
                self.noteArray.append(tk.IntVar(self, 0))

        for i in range(8):
            self.octaveLabelArray.append(tk.Label(self, text = str(i+2)))
            self.octaveLabelArray[i].grid(row = i, column = 0)
            for j in range(12):
                self.noteCheckArray.append(tk.Checkbutton(self,
                    text = self.parent.notes[j],
                    variable = self.noteArray[i*12 + j]))
                self.noteCheckArray[i*12+j].grid(row = i, column = j+1,
                    sticky = "nsew")

        self.confirmButton = tk.Button(self, text="Confirm",
            command = self.confirm)
        self.confirmButton.grid(row = 12, column = 0, columnspan = 13,
            sticky = "nsew")

    ## Function that confirms selection and closes the note select window.
    def confirm(self):
        key = []
        for i in range(len(self.noteArray)):
            if self.noteArray[i].get() == 1:
                key.append(i-36)

        self.parent.key[self.val] = key
        self.destroy()

## -----------------------------------------------------------------------------
## ColorSelectWindow -----------------------------------------------------------
## Class that governs the window to select the colors used.
class ColorSelectWindow(tk.Toplevel):
    ## Initializes all values and GUI elements.
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.wm_title("Select Colors")
        self.parent = parent
        self.entryArray = []
        self.entryValArray = []
        self.canvasArray = []
        for i in range(len(self.parent.colors) - 1):
            self.entryValArray.append(tk.StringVar(self,
                value = self.parent.colors[i+1]))
            self.entryValArray[i].trace("w", self.update)
            self.entryArray.append(tk.Entry(self,
                textvariable = self.entryValArray[i],
                text = self.parent.colors[i+1]))
            self.entryArray[i].grid(row = i, column = 1, sticky ="nsew")
            self.canvasArray.append(tk.Canvas(self, width = 100, height = 25))
            self.canvasArray[i].grid(row = i, column = 0, sticky = "nsew")
            self.canvasArray[i].configure(
                background=self.entryValArray[i].get())

        self.confirmButton = tk.Button(self, text="Confirm",
            command = self.confirm)
        self.confirmButton.grid(row = len(self.parent.colors), column = 0,
            columnspan = 2, sticky = "nsew")

    ## Updates the colors based on changes in the entry boxes.
    def update(self, *args):
        for i in range(len(self.canvasArray)):
            color = re.search(r'^#(?:[0-9a-fA-F]{3}){2}$',
                self.entryValArray[i].get())
            if color:
                self.canvasArray[i].configure(
                    background=self.entryValArray[i].get())
            else:
                self.canvasArray[i].configure(background="black")

        return True

    ## Function to confirm the changes and return them to the main class.
    def confirm(self):
        for i in range(len(self.parent.colors) - 1):
            color = re.search(r'^#(?:[0-9a-fA-F]{3}){2}$',
                self.entryValArray[i].get())
            if color:
                self.parent.colors[i+1] = self.entryValArray[i].get()
            else:
                self.parent.colors[i+1] = "#000000"
                self.parent.write("Invalid color selected.")

        self.parent.updateCurrentSeed()
        self.destroy()

## -----------------------------------------------------------------------------
## switch ----------------------------------------------------------------------
## Python switch statement.
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

## -----------------------------------------------------------------------------
## Main ------------------------------------------------------------------------
## If this file is called as a script, this is executed. Initializes main
## class and runs the Tk main loop.
if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Musical Cellular Automata")
    root.resizable(width=False, height=False)
    app = MainApplication(root)
    app.grid(row = 0, column = 0, sticky = "nsew")
    pygame.init()
    pygame.mixer.init(44100,-16,2,4069)
    pygame.mixer.set_num_channels(10000)
    root.mainloop()
