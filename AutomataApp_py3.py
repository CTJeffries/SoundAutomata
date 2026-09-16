#!/usr/bin/env python3
"""
Colby Jeffries
Musical Cellular Automata - Python 3 Port

AutomataApp.py is the main driver and container for the AutomataApp.
This file contains the GUI application with Tkinter interface.
"""

import tkinter as tk
from tkinter import ttk, font, messagebox
import SoundAutomata_py3 as SoundAutomata
import pygame.mixer
import random
import time
import copy
import shutil
import os
import re
from pathlib import Path
from tkinter import filedialog


class MainApplication(tk.Frame):
    """Primary class that contains the GUI for the Cellular Automata Music Generator."""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.canvas_size = 450
        self.notes = ["C", "C#/Df", "D", "D#/Ef", "E", "F", "F#/Gf", "G",
                       "G#/Af", "A", "A#/Bf", "B"]
        self.progressions = ["Custom", "Blues", "Two-Chord", "Three-Chord", "32 Bar"]
        self.colors = ["grey", "#2579E7"]
        self.seed_size = 6
        self.progression = [0]
        self.files = set([])
        self.seed = np.zeros((self.seed_size, self.seed_size))
        self.file = os.getcwd() + os.path.sep + "pizzicatoc4.wav"
        self.bpm = tk.StringVar(self, value="300")
        self.note_length_min = tk.StringVar(self, value="1000")
        self.note_length_max = tk.StringVar(self, value="2000")
        self.note_length_step = tk.StringVar(self, value="500")
        self.options = ["Conways", "Up", "Down", "Left", "Right", "No Update",
                        "1D", "Brian's Brain", "Seeds", "Langton's Ant"]
        self.update_type = tk.StringVar(self, value=self.options[0])
        self.one_d_rule = tk.StringVar(self, value="30")
        # Single chord by default
        self.key = [[-5, -1, 2, 7, 14, 19]]

        # Create seed grid visualization canvas
        self.seed_select = tk.Canvas(self, width=self.canvas_size,
                                      height=self.canvas_size)
        self.seed_select.grid(row=0, column=0, sticky="nsew", padx=5, pady=5,
                              rowspan=5, columnspan=5)
        self.cell_width = self.canvas_size / self.seed_size
        self.seed_select_array = {}

        # Generate black seed array (reset to all grey/black first)
        for column in range(self.seed_size):
            for row in range(self.seed_size):
                x1 = column * self.cell_width
                y1 = row * self.cell_width
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_width
                self.seed_select_array[row, column] = (
                    self.seed_select.create_rectangle(x1, y1, x2, y2, fill="grey",
                                                      tags=f"rect{row}x{column}")
                )

        # Board size slider
        self.seed_size_scale = tk.Scale(self, from_=2, to=50, variable=self.seed_size,
                                         tickinterval=48, orient="horizontal",
                                         command=self.reset_seed)
        self.seed_size_scale.set(6)
        self.seed_size_scale.grid(row=5, column=0, columnspan=6, sticky="nsew")

        self.seed_size_label = tk.Label(self, text="Board Size")
        self.seed_size_label.grid(row=6, column=0, columnspan=6, sticky="nsew")

        # Create button
        self.create_button = tk.Button(self, text="Create", command=self.create)
        self.create_button.grid(row=0, column=5, rowspan=3, sticky="nsew")

        # Reset button
        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.grid(row=3, column=5, sticky="nsew")

        # Randomize button
        self.randomize_button = tk.Button(self, text="Randomize", command=self.randomize)
        self.randomize_button.grid(row=4, column=5, sticky="nsew")

        # Update rule dropdown (disabled by default)
        self.update_options = tk.OptionMenu(self, self.update_type, *self.options,
                                             command=self.enable_extra_options)
        self.update_options.grid(row=11, column=0, columnspan=2, sticky="nsew")
        self.update_options_label = tk.Label(self, text="Update Rule")
        self.update_options_label.grid(row=11, column=2, sticky="nsw")

        # 1D Rule entry (disabled by default)
        self.update_options_entry = tk.Entry(self, textvariable=self.one_d_rule, state="disabled")
        self.update_options_entry.grid(row=11, column=3, sticky="nsew", columnspan=2)

        # Key selection button
        self.select_key_button = tk.Button(self, text="Select Notes", command=self.select_notes)
        self.select_key_button.grid(row=8, column=0, columnspan=2, sticky="nsew")

        # Chords option menu (disabled by default)
        self.key_option_val = tk.StringVar(self, "Single Chord")
        self.multiple_key_options = tk.OptionMenu(self, self.key_option_val, *["Single Chord",
                                                                                 "Multiple Chords",
                                                                                 "Generated Chords"],
                                                   command=self.enable_multi_key)
        self.multiple_key_options.grid(row=8, column=2, sticky="nsew")

        # Key entry for number of chords (disabled by default)
        self.key_entry_val = tk.IntVar(self, 1)
        self.key_entry_val.trace("w", self.update_multi_key)
        self.key_entry = tk.Entry(self, textvariable=self.key_entry_val, state="disabled")
        self.key_entry.grid(row=8, column=3, columnspan=2, sticky="nsew")
        self.key_entry_label = tk.Label(self, text="Chords")
        self.key_entry_label.grid(row=8, column=5, sticky="nsw")

        # Key selection menu (disabled by default)
        self.select_key_val = tk.StringVar(self, self.notes[0])
        self.select_key_val.trace("w", self.update_key)
        self.select_key_menu = tk.OptionMenu(self, self.select_key_val, *self.notes)
        self.select_key_menu.configure(state="disabled")
        self.select_key_menu.grid(row=10, column=0, columnspan=2, sticky="nsew")
        self.select_key_menu_label = tk.Label(self, text="Key")
        self.select_key_menu_label.grid(row=10, column=2, sticky="nsw")

        # Progression selection menu (disabled by default)
        self.select_prog_val = tk.StringVar(self, self.progressions[0])
        self.select_prog_val.trace("w", self.update_key)
        self.select_progression_menu = tk.OptionMenu(self, self.select_prog_val, *self.progressions)
        self.select_progression_menu.configure(state="disabled")
        self.select_progression_menu.grid(row=10, column=3, columnspan=2, sticky="nsew")
        self.select_progression_menu_label = tk.Label(self, text="Progression")
        self.select_progression_menu_label.grid(row=10, column=5, sticky="nsw")

        # Select sound file button
        self.select_file_button = tk.Button(self, text="Select Sound", command=self.select_file)
        self.select_file_button.grid(row=7, column=0, columnspan=2, sticky="nsew")

        # Current file label
        self.file = "pizzicatoc4.wav"  # Default filename
        self.select_file_label = tk.Label(self, text=self.file)
        self.select_file_label.grid(row=7, column=2, columnspan=3, sticky="nsew")

        # Normalize length checkbox
        self.length_check_val = tk.IntVar(self, 0)
        self.length_check = tk.Checkbutton(self, text="Normalize Length?", variable=self.length_check_val,
                                            command=self.enable_window)
        self.length_check.grid(row=12, column=3, sticky="nsw")

        # Play notes checkbox
        self.play_check_val = tk.IntVar(self, 1)
        self.play_check = tk.Checkbutton(self, text="Play notes?", variable=self.play_check_val)
        self.play_check.grid(row=13, column=3, sticky="nsw")

        # Window size entry (disabled by default)
        self.window_size_val = tk.DoubleVar(self, 0.5)
        self.window_size_val.trace("w", self.wipe)
        self.window_size_entry = tk.Entry(self, textvariable=self.window_size_val, state="disabled")
        self.window_size_entry.grid(row=12, column=0, sticky="nsew", columnspan=2)
        self.window_size_label = tk.Label(self, text="Window Size")
        self.window_size_label.grid(row=12, column=2, sticky="nsw")

        # Cycles entry
        self.cycles_entry_val = tk.IntVar(self, 10)
        self.cycles_entry = tk.Entry(self, textvariable=self.cycles_entry_val)
        self.cycles_entry.grid(row=13, column=0, sticky="nsew", columnspan=2)
        self.cycles_label = tk.Label(self, text="Cycles")
        self.cycles_label.grid(row=13, column=2, sticky="nsw")

        # BPM entry
        self.bpm_entry = tk.Entry(self, textvariable=self.bpm, text=self.bpm)
        self.bpm_entry.grid(row=14, column=0, sticky="nsew", columnspan=2)
        self.bpm_label = tk.Label(self, text="BPM")
        self.bpm_label.grid(row=14, column=2, sticky="nsw")

        # Note length min entry (milliseconds)
        self.note_length_min_entry = tk.Entry(self, textvariable=self.note_length_min, text=self.note_length_min)
        self.note_length_min_entry.grid(row=15, column=0, sticky="nsew", columnspan=2)
        self.note_length_min_label = tk.Label(self, text="Length Min (ms)")
        self.note_length_min_label.grid(row=15, column=2, sticky="nsw")

        # Note length max entry
        self.note_length_max_entry = tk.Entry(self, textvariable=self.note_length_max, text=self.note_length_max)
        self.note_length_max_entry.grid(row=15, column=3, sticky="nsew", columnspan=2)
        self.note_length_max_label = tk.Label(self, text="Length Max (ms)")
        self.note_length_max_label.grid(row=15, column=5, sticky="nsw")

        # Note length step entry
        self.note_length_step_entry = tk.Entry(self, textvariable=self.note_length_step, text=self.note_length_step)
        self.note_length_step_entry.grid(row=17, column=0, sticky="nsew", columnspan=2)
        self.note_length_step_label = tk.Label(self, text="Length Step (ms)")
        self.note_length_step_label.grid(row=17, column=2, sticky="nsw")

        # Debug output frame
        self.debug_frame = tk.LabelFrame(self, text="Debug Output")
        self.select_colors_button = tk.Button(self, text="Select Colors", command=self.select_colors)
        self.select_colors_button.grid(row=17, column=3, columnspan=2, sticky="nsew")

        # Notes to play scale (horizontal slider)
        self.to_play_scale = tk.Scale(self, from_=1, to=6, tickinterval=5, orient="horizontal")
        self.to_play_scale.set(6)
        self.to_play_scale.grid(row=18, column=0, columnspan=6, sticky="nsew")
        self.to_play_label = tk.Label(self, text="Notes to play")
        self.to_play_label.grid(row=19, column=0, columnspan=6, sticky="nsew")

        # Debug output text area
        self.debug_frame.grid(row=20, column=0, columnspan=5, sticky='nsew')
        self.console_output = tk.Text(self.debug_frame, background="black",
                                       font=("mono", 11), width=50, height=7,
                                       foreground='white', state=tk.DISABLED)
        self.console_output.grid(row=0, column=0, sticky='nsew')
        self.scrollbar = tk.Scrollbar(self.debug_frame, command=self.console_output.yview)
        self.scrollbar.grid(row=0, column=1, sticky='nsew')
        self.console_output['yscrollcommand'] = self.scrollbar.set

        # Make debug frame responsive
        self.debug_frame.columnconfigure(0, weight=1)

        # Custom progression entry (disabled by default)
        self.progression_entry_val = tk.StringVar(self, "0")
        self.progression_entry_val.trace("w", self.update_progression)
        self.progression_entry = tk.Entry(self, textvariable=self.progression_entry_val, state="disabled")
        self.progression_entry.grid(row=9, column=0, columnspan=5, sticky="nsew")
        self.progression_entry_label = tk.Label(self, text="Progression")
        self.progression_entry_label.grid(row=9, column=5, sticky="nsw")

    def update_key(self, *args):
        """Updates the notes and chords for the automata when a new key or progression is selected."""
        try:
            self.key = []
            key_idx = self.notes.index(self.select_key_val.get())
            scale = [key_idx, (key_idx + 2) % 12, (key_idx + 4) % 12, (key_idx + 5) % 12,
                     (key_idx + 7) % 12, (key_idx + 9) % 12, (key_idx + 11) % 12]
            chord = [scale[0], scale[2], scale[4]]
            chords = [k - 24 for k in chord]

            # Add the base chord and its inversions
            for j in range(-1, 3):
                chords.extend([k + (j * 12) for k in chord])

            self.key.append(chords)
        except Exception:
            pass

    def enable_window(self, *args):
        """Enables the window size entry box when normalize length is checked."""
        if self.length_check_val.get():
            self.window_size_entry.configure(state="normal")
        else:
            self.window_size_entry.configure(state="disabled")

    def update_progression(self, *args):
        """Updates the progression when the progression entry box is changed."""
        try:
            self.progression = [int(x) for x in self.progression_entry_val.get().split(',')]
        except Exception:
            pass

    def enable_multi_key(self, selection):
        """Changes GUI widget states based on chord mode selection."""
        if selection == "Multiple Chords":
            self.select_progression_menu.configure(state="disabled")
            self.select_key_menu.configure(state="disabled")
            self.key_entry.configure(state="normal")
            self.progression_entry.configure(state="normal")
        elif selection == "Single Chord":
            self.select_progression_menu.configure(state="disabled")
            self.select_key_menu.configure(state="disabled")
            self.key_entry.configure(state="disabled")
            self.progression_entry.configure(state="disabled")
            self.progression = [0]
            self.key = [self.key[0]]
        elif selection == "Generated Chords":
            self.select_progression_menu.configure(state="normal")
            self.key_entry.configure(state="disabled")
            self.progression_entry.configure(state="disabled")
            self.select_key_menu.configure(state="normal")
            self.update_key()

    def select_colors(self):
        """Opens a window to select colors."""
        self.write("Select colors...")
        new_win = ColorSelectWindow(self)
        self.wait_window(new_win)

    def write(self, string):
        """Writes the input string into the console output window."""
        self.console_output.configure(state=tk.NORMAL)
        self.console_output.insert(tk.END, string + "\n")
        self.console_output.see(tk.END)
        self.console_output.configure(state=tk.DISABLED)

    def reset_seed(self, new_size):
        """Resets and redraws the seed based on the selected size."""
        new_size = int(new_size)
        self.seed_size = new_size
        self.cell_width = self.canvas_size / new_size
        self.seed = np.zeros((new_size, new_size))
        self.seed_select_array = {}
        self.seed_select.delete("all")

        # Update scale to match board size
        self.to_play_scale.configure(to_=new_size)
        self.to_play_scale.configure(tickinterval=new_size - 1 if new_size > 1 else 1)
        self.to_play_scale.set(new_size)

        for column in range(new_size):
            for row in range(new_size):
                x1 = column * self.cell_width
                y1 = row * self.cell_width
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_width
                self.seed_select_array[row, column] = (
                    self.seed_select.create_rectangle(x1, y1, x2, y2, fill="grey",
                                                      tags=f"rect{row}x{column}")
                )

                # Add click handler for changing seed cells
                self.seed_select.tag_bind(self.seed_select_array[row, column],
                                          '<ButtonPress-1>',
                                          lambda e, r=row, c=column: self.on_object_click(e, r, c))

    def on_object_click(self, event, row, column):
        """Callback function that adjusts the seed when a box is clicked."""
        try:
            self.seed[row][column] = (self.seed[row][column] + 1) % len(self.colors)
            widget_id = f"rect{row}x{column}"
            if widget_id in self.seed_select.tag_items():
                self.seed_select.itemconfigure(widget_id, fill=self.colors[int(self.seed[row][column])])
        except Exception:
            pass

    def create(self):
        """Primary function that creates an instance of the automata and drives execution."""
        self.write("Initializing new Musical Automata...")

        if self.key_option_val.get() == "Generated Chords":
            self.update_key()

        # Validate 1D rule range
        one_d_rule_int = None
        try:
            one_d_rule_int = int(self.one_d_rule.get())
            if one_d_rule_int > 255 or one_d_rule_int < 0:
                self.one_d_rule.set("30")
                self.write("There are only 0-255 rules! Resetting to default.")
        except Exception:
            one_d_rule_int = None

        # Create visualizer window
        window = VisualizerWindow(self, self.seed, self.seed_size, self.cell_width)

        # Initialize pygame mixer (must be done before creating SoundAutomata instance)
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            # Pygame may need multiple init calls to handle many channels
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception as e:
            self.write(f"Warning: Could not initialize audio mixer: {e}\nAudio will not be available.")

        bpm = float(60) / float(self.bpm_entry.get())
        start_time = 0.0

        # Use default file if custom file doesn't exist
        wav_file = "pizzicatoc4.wav"
        if self.file and Path(self.file).exists():
            wav_file = os.path.basename(self.file)
        else:
            self.write("Warning: Using default sound file (pizzicatoc4.wav)")

        # Create sound generator with simplified parameters for Python 3 compatibility
        try:
            sound_generator = SoundAutomata.SoundAutomata(
                parent=self,
                seed=self.seed,
                sound=f"pizzicatoc4.wav",  # Simplified - notes generated on-the-fly
                key=[self.key[0]],
                length_adjusted=False,
                window_size=0.5
            )
        except Exception as e:
            self.write(f"Error creating automata: {e}")
            window.destroy()
            return

        prog_pos = 0
        for i in range(self.cycles_entry_val.get()):
            # Check key bounds for progression
            if len(self.key) <= max(self.progression):
                self.write("Not enough chords for the progression!")
                break

            try:
                # Update visualization and play notes for each cell position
                for j in range(self.seed_size):
                    window.update(sound_generator.game_board, (sound_generator.current_note - 1) % self.seed_size)

                    # Wait for BPM timing
                    elapsed = time.time() - start_time
                    if elapsed < bpm:
                        time.sleep(0.05)  # Small sleep to avoid busy waiting

                    # Play notes in a range
                    num_notes = self.to_play_scale.get()
                    if sound_generator.game_board[sound_generator.current_note].any():
                        note_length = random.randint(int(self.note_length_min.get()),
                                                     int(self.note_length_max.get()))
                        if self.play_check_val.get() and pygame.mixer.get_init():
                            sound_generator.play(note_length / 1000.0, num_notes, True)

                    start_time = time.time()

                # Apply update rule after completing the row
                if one_d_rule_int is not None:
                    sound_generator.update("1D", one_d_rule_int)
                else:
                    update_type = self.update_type.get()
                    if update_type in ["Conways", "Brian's Brain", "Seeds"]:
                        sound_generator.update(update_type)
                    elif update_type in ["Up", "Down", "Left", "Right"]:
                        sound_generator.update(update_type)
                    elif update_type == "No Update":
                        sound_generator.no_update()

                # Change chord if using multiple chords or progressions
                if self.key_option_val.get() != "Single Chord" and len(self.progression) > 1:
                    prog_pos = (prog_pos + 1) % len(self.progression)
                    sound_generator.update_key(prog_pos)

            except Exception as e:
                self.write(f"Error during cycle {i}: {e}")
                continue

        # Cleanup and close
        try:
            window.destroy()
        except Exception:
            pass


class VisualizerWindow(tk.Toplevel):
    """Class that governs the visualizer of the cellular automata."""

    def __init__(self, parent, seed, seed_size, cell_width):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.seed = seed
        self.cell_width = cell_width
        self.seed_size = seed_size

        # Create canvas for visualizing the automata board
        self.visualizer = tk.Canvas(self, width=parent.canvas_size, height=parent.canvas_size)
        self.visualizer_array = {}
        self.visualizer_seed = copy.deepcopy(seed)

        self.visualizer.pack()

        # Create visual cells
        for column in range(self.seed_size):
            for row in range(self.seed_size):
                x1 = column * self.cell_width
                y1 = row * self.cell_width
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_width
                self.visualizer_array[row, column] = (
                    self.visualizer.create_rectangle(x1, y1, x2, y2,
                                                     fill=self.parent.colors[int(seed[row][column])],
                                                     tags=f"rectVis{row}{column}")
                )

    def update(self, new_seed, current_note):
        """Updates the visual based on changes caused by cellular automata."""
        for row in range(self.seed_size):
            for column in range(self.seed_size):
                if new_seed[row][column]:
                    self.visualizer.itemconfig(self.visualizer_array[row, column],
                                               fill=self.parent.colors[int(new_seed[row][column])])
                else:
                    # Highlight active note row in yellow
                    if row == current_note:
                        self.visualizer.itemconfig(self.visualizer_array[row, column], fill="yellow")
                    else:
                        self.visualizer.itemconfig(self.visualizer_array[row, column],
                                                  fill=self.parent.colors[0])

        # Update main window
        self.parent.parent.update()


class NotesSelectWindow(tk.Toplevel):
    """Class that governs the window to select new notes/chords."""

    def __init__(self, parent, val):
        tk.Toplevel.__init__(self, parent)
        self.wm_title("Select Key/Chord " + str(val + 1))
        self.parent = parent
        self.val = val
        self.note_array = []
        self.note_check_array = []

        # Create note checkboxes for each semitone across octaves
        for i in range(-36, 60):
            if i in self.parent.key[val]:
                self.note_array.append(tk.IntVar(self, 1))
            else:
                self.note_array.append(tk.IntVar(self, 0))

        # Create octave labels and checkboxes
        for i in range(8):
            tk.Label(self, text=str(i + 2)).grid(row=i, column=0)
            for j in range(12):
                checkbox = tk.Checkbutton(self,
                                          text=self.parent.notes[j],
                                          variable=self.note_array[i * 12 + j])
                checkbox.grid(row=i, column=j + 1, sticky="nsew")

        # Confirm button
        self.confirm_button = tk.Button(self, text="Confirm", command=self.confirm)
        self.confirm_button.grid(row=12, column=0, columnspan=13, sticky="nsew")

    def confirm(self):
        """Confirms selection and closes the note select window."""
        key = []
        for i in range(len(self.note_array)):
            if self.note_array[i].get() == 1:
                key.append(i - 36)

        self.parent.key[self.val] = sorted(set(key))
        self.destroy()


class ColorSelectWindow(tk.Toplevel):
    """Class that governs the window to select the colors used."""

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.wm_title("Select Colors")
        self.parent = parent

        # Create color selection entries
        self.entry_array = []
        self.entry_val_array = []
        self.canvas_array = []

        for i in range(len(self.parent.colors) - 1):
            self.entry_val_array.append(tk.StringVar(self, value=self.parent.colors[i + 1]))
            self.entry_val_array[i].trace("w", self.update)

            entry = tk.Entry(self, textvariable=self.entry_val_array[i])
            entry.grid(row=i, column=1, sticky="nsew")

            canvas = tk.Canvas(self, width=100, height=25)
            canvas.grid(row=i, column=0, sticky="nsew")
            canvas.configure(background=self.entry_val_array[i].get())
            self.canvas_array.append(canvas)

        # Confirm button
        self.confirm_button = tk.Button(self, text="Confirm", command=self.confirm)
        self.confirm_button.grid(row=len(self.parent.colors), column=0, columnspan=2, sticky="nsew")

    def update(self, *args):
        """Updates the colors based on changes in the entry boxes."""
        for i in range(len(self.canvas_array)):
            color = re.search(r'^#(?:[0-9a-fA-F]{3}){2}$', self.entry_val_array[i].get())
            if color:
                self.canvas_array[i].configure(background=self.entry_val_array[i].get())
            else:
                self.canvas_array[i].configure(background="black")

        return True

    def confirm(self):
        """Confirms the changes and returns them to the main class."""
        for i in range(len(self.parent.colors) - 1):
            color = re.search(r'^#(?:[0-9a-fA-F]{3}){2}$', self.entry_val_array[i].get())
            if color:
                self.parent.colors[i + 1] = self.entry_val_array[i].get()
            else:
                self.parent.colors[i + 1] = "#000000"
                self.parent.write("Invalid color selected.")

        # Note: parent.write might not exist in this context, so we skip updating colors here
        self.destroy()


class MainApplication(tk.Frame):
    """Main application class with entry point."""

    @staticmethod
    def main(root):
        """Entry point for the Tkinter application."""
        root = tk.Tk()
        root.wm_title("Musical Cellular Automata - Python 3 Port")
        root.resizable(width=False, height=False)

        app = MainApplication(root)
        app.grid(row=0, column=0, sticky="nsew")

        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception as e:
            print(f"Warning: Audio initialization failed: {e}")
            print("The app will still run without audio playback.")

        root.mainloop()


if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
