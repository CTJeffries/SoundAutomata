#!/usr/bin/env python3
"""
Colby Jeffries
Musical Cellular Automata - Python 3 Port (PyAudio version)

SoundAutomata.py contains the SoundAutomata class. Governs the cellular automata and all
audio generation using PyAudio instead of pygame.mixer."""

import time
import wave
import os
import copy
import math
import random
from pathlib import Path
from typing import Optional, List

import numpy as np

# Import PyAudio wrapper instead of pygame mixer
try:
    from pyaudio_wrapper import (
        PyAudioNote, PyAudioMixer, load_wav, save_wav, init_audio, cleanup_audio, note_play
    )
except ImportError:
    # Fallback to local implementation if wrapper not found
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from pyaudio_wrapper import (
        PyAudioNote, PyAudioMixer, load_wav, save_wav, init_audio, cleanup_audio, note_play
)


class SoundAutomata:
    """Governs the cellular automata and audio generation using PyAudio."""

    def __init__(self, parent, seed=np.random.randint(2, size=(4, 4)),
                 sound="sinec4.wav", key=[[-5, -1, 2, 7, 14, 19]],
                 length_adjusted=False, window_size=0.5):
        """Initialize the SoundAutomata object."""
        self.parent = parent
        self.game_board = seed
        self.length_adjusted = length_adjusted
        self.window_size = window_size
        self.basic_note = sound
        if not Path(self.basic_note[:-4]).exists():
            os.mkdir(self.basic_note[:-4])
        self.size = len(self.game_board[1])
        self.game_board_temp = copy.deepcopy(self.game_board)
        self.key = key
        # Initialize PyAudio mixer (for GUI applications, init on first play or in create())
        self.mixer = None
        self.current_note = 0
        self.current_key = 0
        self.initialized = False

    def count_neighbors(self, x, y):
        """Count the number of alive neighbors in a cell's Moore neighborhood."""
        count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                cur_x = i % self.size
                cur_y = j % self.size
                if self.organism_at(cur_x, cur_y) and (cur_x != x or cur_y != y):
                    count += 1
        return count

    def organism_at(self, x, y):
        """Returns whether there is an alive cell at (x,y)."""
        return self.game_board[x][y] == 1

    def one_d_update(self, rule):
        """Function that updates the automata based on the specified 1-D rule."""
        bin_rule = bin(int(rule))[2:].zfill(8)
        for i in range(self.size):
            prev_val = []
            for j in range(i - 1, i + 2):
                cur_j = j % self.size
                prev_val.append(self.organism_at((self.current_note - 1) % self.size, cur_j))

            # Use a flag to break after finding first match instead of Python switch
            for pattern, result in zip([1, 1, 0], [1, 1, 0]) + \
                                       [[1, 0, 1], [1, 0, 0]] + \
                                       [[0, 1, 1], [0, 1, 0]] + \
                                       [[0, 0, 1], [0, 0, 0]]:
                if prev_val == pattern[:3]:
                    self.game_board_temp[self.current_note][i] = int(bin_rule[sum(prev_val)])
                    break

        self.game_board = copy.deepcopy(self.game_board_temp)

    def conways_update(self):
        """Function that updates the automata based on Conway's Game of Life."""
        for i in range(self.size):
            for j in range(self.size):
                count = self.count_neighbors(i, j)
                if self.organism_at(i, j):
                    if count not in [2, 3]:
                        self.game_board_temp[i][j] = 0
                else:
                    if count == 3:
                        self.game_board_temp[i][j] = 1

        self.game_board = copy.deepcopy(self.game_board_temp)

    def no_update(self):
        """Function that copies the gameboard without updates."""
        self.game_board = copy.deepcopy(self.game_board_temp)

    def right_update(self):
        """Slides the cellular automata 1 cell to the right on each update."""
        for i in range(self.size):
            for j in range(self.size):
                cur_x = (j - 1) % self.size
                if self.organism_at(i, cur_x):
                    self.game_board_temp[i][j] = 1
                else:
                    self.game_board_temp[i][j] = 0

        self.game_board = copy.deepcopy(self.game_board_temp)

    def left_update(self):
        """Slides the cellular automata 1 cell to the left on each update."""
        for i in range(self.size):
            for j in range(self.size):
                cur_x = (j + 1) % self.size
                if self.organism_at(i, cur_x):
                    self.game_board_temp[i][j] = 1
                else:
                    self.game_board_temp[i][j] = 0

        self.game_board = copy.deepcopy(self.game_board_temp)

    def down_update(self):
        """Slides the cellular automata 1 cell down on each update."""
        for i in range(self.size):
            for j in range(self.size):
                cur_y = (i - 1) % self.size
                if self.organism_at(cur_y, j):
                    self.game_board_temp[i][j] = 1
                else:
                    self.game_board_temp[i][j] = 0

        self.game_board = copy.deepcopy(self.game_board_temp)

    def up_update(self):
        """Slides the cellular automata 1 cell up on each update."""
        for i in range(self.size):
            for j in range(self.size):
                cur_y = (i + 1) % self.size
                if self.organism_at(cur_y, j):
                    self.game_board_temp[i][j] = 1
                else:
                    self.game_board_temp[i][j] = 0

        self.game_board = copy.deepcopy(self.game_board_temp)

    def b_b_update(self):
        """Updates the cellular automata according to the rules of Brian's Brain."""
        for i in range(self.size):
            for j in range(self.size):
                count = self.count_neighbors(i, j)
                current = self.game_board[i][j]
                if current == 1:
                    self.game_board_temp[i][j] = 2
                elif current == 2:
                    self.game_board_temp[i][j] = 0
                else:
                    if count == 2:
                        self.game_board_temp[i][j] = 1

        self.game_board = copy.deepcopy(self.game_board_temp)

    def seeds_update(self):
        """Updates the cellular automata according to the rules of Seeds."""
        for i in range(self.size):
            for j in range(self.size):
                count = self.count_neighbors(i, j)
                if not self.organism_at(i, j):
                    if count == 2:
                        self.game_board_temp[i][j] = 1
                else:
                    self.game_board_temp[i][j] = 0

        self.game_board = copy.deepcopy(self.game_board_temp)

    def langtons_update(self):
        """Updates the cellular automata according to the rules of Langton's Ant."""
        for i in range(self.size):
            for j in range(self.size):
                current = self.game_board[i][j]
                # Simplified Langton's ant state transitions
                if current == 2:
                    self.game_board_temp[i][j] = 0
                elif current == 3:
                    self.game_board_temp[i][j] = 0
                elif current == 4:
                    self.game_board_temp[i][j] = 0
                elif current == 5:
                    self.game_board_temp[i][j] = 1
                elif current == 6:
                    self.game_board_temp[i][j] = 1
                elif current == 7:
                    self.game_board_temp[i][j] = 1
                elif current == 8:
                    self.game_board_temp[i][j] = 1
                else:
                    self.game_board_temp[i][j] = 1

        self.game_board = copy.deepcopy(self.game_board_temp)

    def update(self, update_type, one_d_rule=None):
        """General update function that calls the proper update function."""
        if update_type == "Conways":
            self.conways_update()
        elif update_type == "Up":
            self.up_update()
        elif update_type == "Down":
            self.down_update()
        elif update_type == "Left":
            self.left_update()
        elif update_type == "Right":
            self.right_update()
        elif update_type == "No Update":
            self.no_update()
        elif update_type == "1D" and one_d_rule is not None:
            self.one_d_update(one_d_rule)
        elif update_type == "Brian's Brain":
            self.b_b_update()
        elif update_type == "Seeds":
            self.seeds_update()
        elif update_type == "Langton's Ant":
            self.langtons_update()
        else:
            print("Not a valid update type.")

    def speedx(self, snd_array, factor):
        """Speeds up the audio in snd_array by a given factor."""
        indices = np.round(np.arange(0, len(snd_array), factor)).astype(int)
        indices = indices[indices < len(snd_array)]
        return snd_array[indices]

    def generate_notes(self):
        """Generate audio files for all pitches based on the original sound."""
        from pathlib import Path

        # Create notes directory if it doesn't exist
        notes_dir = Path(self.basic_note[:-4])
        notes_dir.mkdir(parents=True, exist_ok=True)

        # Load base sound
        base_note_path = Path(self.basic_note[:-4]) / "pizzicatoc4.wav"
        if not base_note_path.exists():
            print(f"Warning: {base_note_path} not found. Cannot generate notes.")
            return

        try:
            samplerate, smp = load_wav(str(base_note_path))
            if samplerate is None:
                print("Error: Could not load base sound file.")
                return

            # Generate all pitches from -36 to 59 semitones
            for i in range(-36, 60):
                note_file = Path(self.basic_note[:-4]) / f"{i}.wav"
                if not note_file.exists():
                    # Calculate stretch factor
                    factor = 2 ** (1.0 * i / 12.0)

                    # Stretch audio using paulstretch module
                    from paulstretch_py3 import paulstretch as ps_stretch
                    stretched_path = str(Path(self.basic_note[:-4]) / "temp.wav")
                    ps_stretch(samplerate, smp, factor, self.window_size, stretched_path)

                    # Load stretched and speed up audio
                    note_samples = load_wav(stretched_path)
                    if note_samples is None:
                        continue

                    basic_note_resampled = []
                    for ch in range(note_samples[0].shape[1]):
                        sound_channel = note_samples[0][:, ch]
                        resampled = self.speedx(sound_channel, factor)
                        basic_note_resampled.append(resampled)

                    # Write new note file
                    note_file_array = np.array(basic_note_resampled).copy(order='C')
                    samples_to_write = (note_file_array * 32767).astype(np.int16)

                    note_wav = wave.open(note_file, 'wb')
                    note_wav.setframerate(44100)
                    note_wav.setnchannels(2)
                    note_wav.setsampwidth(2)
                    note_wav.writeframes(samples_to_write.tobytes())
                    note_wav.close()

        finally:
            # Cleanup temp file
            temp_path = Path(self.basic_note[:-4]) / "temp.wav"
            if temp_path.exists():
                os.remove(temp_path)

    def load_and_load_notes(self):
        """Load all notes into memory using PyAudio."""
        from pathlib import Path

        notes_dir = Path(self.basic_note[:-4])

        self.note_array = []
        for key_chord in self.key:
            chord_notes = []
            for i in key_chord:
                note_path = notes_dir / f"{i}.wav"
                if note_path.exists():
                    # Load note with PyAudioNote
                    try:
                        note = PyAudioNote(str(note_path))
                        chord_notes.append(note)
                    except Exception as e:
                        print(f"Error loading note {note_path}: {e}")
                        chord_notes.append(None)
                else:
                    chord_notes.append(None)
            self.note_array.append(chord_notes)

    def load_notes(self):
        """Load all generated notes into PyAudioNote objects."""
        from pathlib import Path

        notes_dir = Path(self.basic_note[:-4])

        self.note_array = []
        for key_chord in self.key:
            chord_notes = []
            for i in key_chord:
                note_path = notes_dir / f"{i}.wav"
                if note_path.exists():
                    # Load note with PyAudioNote
                    try:
                        note = PyAudioNote(str(note_path))
                        chord_notes.append(note)
                    except Exception as e:
                        print(f"Error loading note {note_path}: {e}")
                        chord_notes.append(None)
                else:
                    chord_notes.append(None)
            self.note_array.append(chord_notes)

    def init_audio(self):
        """Initialize PyAudio mixer for playback."""
        try:
            self.mixer = PyAudioMixer(rate=44100, chunk=1024)
            if not self.mixer.init():
                print("Warning: Could not initialize audio. Audio playback will be disabled.")
                return False
        except Exception as e:
            print(f"Error initializing audio: {e}")
            print("Audio playback will be disabled.")
            return False

        self.initialized = True
        return True

    def no_init(self):
        """Check if mixer was initialized."""
        return self.mixer is not None and self.mixer.get_init()

    def play(self, notelen, num, music_check):
        """Plays one time step of the cellular automata."""
        if music_check:
            to_play = []
            for i in range(len(self.game_board[self.current_note])):
                if self.game_board[self.current_note][i] > 0:
                    to_play.append(i)

            if num > len(to_play):
                num = len(to_play)

            n = len(to_play) - num
            to_play = to_play[n // 2:len(to_play) - n // 2]

            for j in range(num):
                if self.game_board[self.current_note][to_play[j]]:
                    volume = 1 / self.game_board[self.current_note][to_play[j]]

                    # Get the note object
                    note_key = to_play[j] % len(self.key[self.current_key])
                    notes_row = self.note_array[self.current_key]

                    if notes_row and note_key < len(notes_row):
                        note_obj = notes_row[note_key]

                        # Initialize audio if not done yet
                        if not hasattr(self, 'initialized') or not self.initialized:
                            if not self.init_audio():
                                print("Note playback disabled.")
                                return

                        if note_obj and self.no_init():
                            # Set volume on the note
                            if hasattr(note_obj, 'set_volume'):
                                note_obj.set_volume(volume)
                            # Play the note using PyAudio
                            if hasattr(note_obj, 'play'):
                                try:
                                    note_obj.play()
                                except Exception as e:
                                    print(f"Playback error for note {to_play[j]}: {e}")

            self.initialized = True

        # Wrap around to next row
        self.current_note = (self.current_note + 1) % self.size

    def update_key(self, val):
        """Moves the progression forward one chord. Will wrap around."""
        self.current_key = self.parent.progression[val]


def main():
    """Main entry point for testing SoundAutomata class directly."""
    import os

    # Check if base sound file exists
    wav_path = "pizzicatoc4.wav"
    if not Path(wav_path).exists():
        print(f"Error: {wav_path} not found in current directory")
        print("Please place a WAV file named 'pizzicatoc4.wav' in the directory.")
        return

    # Create automata instance with default parameters
    sa = SoundAutomata(
        parent=None,
        seed=np.random.randint(2, size=(4, 4)),
        sound=f"{Path(wav_path).stem}.wav",
        key=[[-5, -1, 2, 7, 14, 19]],
        length_adjusted=False,
        window_size=0.5
    )

    print("SoundAutomata initialized successfully!")
    print(f"Board size: {sa.size}")
    print(f"Starting note array shape: {sa.game_board.shape}")


if __name__ == "__main__":
    main()
