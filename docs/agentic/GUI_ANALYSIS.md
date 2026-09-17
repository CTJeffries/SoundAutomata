# SoundAutomata - Tkinter to Textual Port Analysis

## Overview

SoundAutomata is a Musical Cellular Automata Generator application built with Python 3's Tkinter. The app combines cellular automaton algorithms (like Conway's Game of Life) with real-time audio playback using PyAudio.

---

## 1. GUI WIDGETS INVENTORY

### Main Window (`MainApplication` class)

#### **Canvas Widgets (2 instances)**
1. **`seed_select`** - Seed grid visualization canvas (450x450 pixels)
   - Displays 6x6 interactive grid cells
   - Each cell is a rectangle that can be clicked to toggle state
   - Used for visualizing and editing the automata seed pattern

2. **Visualizer Window `visualizer`** (`VisualizerWindow` class)
   - Similar canvas, displays real-time cellular automata evolution
   - Highlights active note row in yellow

#### **Scale/Slider Widgets (3 instances)**
1. **`seed_size_scale`** (Row 5)
   - Range: 2-50
   - Controls board size for cellular automata
   - Triggers `reset_seed()` callback

2. **`to_play_scale`** (Row 18, horizontal)
   - Range: 1-6
   - Controls number of notes to play simultaneously
   - Default value: 6

#### **Entry Widgets (7 instances)**
1. **`bpm_entry`** (Row 14) - Beats Per Minute
2. **`cycles_entry`** (Row 13) - Number of animation cycles
3. **`window_size_entry`** (Row 12) - Audio window size for processing
   - Enabled/disabled by `normalize_length` checkbox

4. **`note_length_min_entry`** (Row 15) - Minimum note duration in ms
5. **`note_length_max_entry`** (Row 15) - Maximum note duration in ms
6. **`note_length_step_entry`** (Row 17) - Step for random number generation
7. **`one_d_rule_entry`** (Row 11) - Rule number for 1D cellular automata

#### **Checkbutton Widgets (2 instances)**
1. **`length_check`** (Row 12) - "Normalize Length?" checkbox
   - When checked, enables `window_size_entry`
   - Triggers `enable_window()` callback

2. **`play_check`** (Row 13) - "Play notes?" checkbox
   - Controls audio playback toggle
   - Default: enabled (value=1)

#### **OptionMenu Widgets (4 instances)**
1. **`update_options`** (Row 11) - Update rule selector
   - Options: Conway's, Up, Down, Left, Right, No Update, 1D, Brian's Brain, Seeds, Langton's Ant
   - Default: "Conways"
   - Triggers `enable_extra_options()` callback

2. **`key_option_val`** (Row 8) - Key/Chord mode selector
   - Options: "Single Chord", "Multiple Chords", "Generated Chords"
   - Default: "Single Chord"
   - Triggers `enable_multi_key()` callback

3. **`select_progression_menu`** (Row 10) - Chord progression selector
   - Options: Custom, Blues, Two-Chord, Three-Chord, 32 Bar
   - Default: "Custom"
   - Enabled only for "Multiple Chords" + "Generated Chords" modes

4. **`select_key_menu`** (Row 10) - Musical key selector
   - Notes: C, C#/Df, D, D#/Ef, E, F, F#/Gf, G, G#/Af, A, A#/Bf, B
   - Enabled only for "Generated Chords" mode

#### **Button Widgets (6 instances)**
1. **`create_button`** (Row 0, col 5) - "Create" button
   - Triggers `create()` - Main execution function

2. **`reset_button`** (Row 3, col 5) - "Reset" button
   - Triggers `reset()` - Resets seed grid

3. **`randomize_button`** (Row 4, col 5) - "Randomize" button
   - Triggers `randomize()` - Randomizes seed pattern

4. **`select_key_button`** (Row 8, col 0) - "Select Notes" button
   - Opens `NotesSelectWindow` modal dialog

5. **`select_file_button`** (Row 7, col 0) - "Select Sound" button
   - Opens file dialog for WAV audio files

6. **`select_colors_button`** (Row 17, col 3) - "Select Colors" button
   - Opens `ColorSelectWindow` modal dialog

#### **Label Widgets (Multiple)**
- All buttons have corresponding labels positioned to the left of columns 0-5
- Labels describe their associated controls: BPM, Cycles, Window Size, Notes to play, etc.

#### **Text Widget (1 instance)**
- **`console_output`** (in `debug_frame`, Rows 20+)
  - Scrollable text area with black background
  - Displays debug messages and status updates
  - White monospace font for readability

#### **LabelFrame Widget (1 instance)**
- **`debug_frame`** - Container for console output with title "Debug Output"

---

## 2. Modal Dialog Windows

### `ColorSelectWindow` (tk.Toplevel)
- Purpose: Select/edit colors for automata visualization
- Widgets:
  - Entry boxes for color values (HEX format)
  - Preview canvases showing current colors
  - Confirm button
- Color validation: Requires valid HEX format (#RRGGBB)

### `NotesSelectWindow` (tk.Toplevel)
- Purpose: Select/mutate notes for a chord
- Widgets:
  - Grid of checkboxes (8 octaves × 12 notes = 96 checkboxes)
  - Each checkbox represents one semitone in an octave range (-36 to +59 from base pitch)
  - Column headers showing octave numbers (2-9)
  - Note names as checkbox labels
  - Confirm button

---

## 3. LAYOUT AND GEOMETRY MANAGEMENT

### Grid System (Tkinter's grid geometry manager)

The main window uses a **6-column, 20+ row** grid layout:

```
Row Structure:
┌─────────────────────────────────────────────────────────────┐
│ Row 0-4: Seed Canvas                                        ││ Create Button (col 5)        │
│                              │                               │          │
│ Row 5: Board Size Scale                                         │
├─────────────────────────────────────────────────────────────┤│
│ Row 6: Board Size Label                                          │          │
├─────────────────────────────────────────────────────────────┤│
│ Row 7-8: File Select Area                                        │Chord Mode/Notes     │
│                        │                               │   to Play         │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 9-10: Progression & Key Selection Areas                       │          │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 11: Update Rule Selector                                      │          │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 12: Window Size (enabled by Normalize Length checkbox)        │          │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 13: Cycles Entry                                               │          │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 14: BPM Entry                                                   │          │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 15: Note Length Min/Max                                         │Play Notes    │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 17: Note Length Step                                             │          │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 18: Notes to Play Slider                                        │          │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 19: Notes to Play Label                                          │          │
├─────────────────────────────────────────────────────────────┤│          │
│ Row 20+: Debug Console                                               │          │
└─────────────────────────────────────────────────────────────┴┴──────────┘
```

### Grid Configuration:
- `sticky="nsew"` on most widgets for flexible resizing
- Column 5 is reserved for the Create/Reset/Randomize button column
- Columns 0-2 contain input controls (entries, scales, menus)
- Rows configured with `weight=1` for responsive scaling

---

## 4. EVENT HANDLERS AND CALLBACKS

### Main Application Callbacks:

| Event Source | Callback Method | Description |
|--------------|-----------------|-------------|
| Seed size scale change | `reset_seed()` | Rebuilds grid with new size |
| Click on seed cell | `on_object_click(row, col)` | Toggles cell state/color |
| Update rule dropdown | `enable_extra_options()` | Updates related controls |
| Key mode dropdown | `enable_multi_key()` | Shows/hides progression/key entries |
| Normalize Length checkbox | `enable_window()` | Enables/disables window size entry |
| Progression entry change | `update_progression()` | Parses comma-separated list |
| Key value trace | `update_key()` | Regenerates chord notes |
| Chord count entry trace | `update_multi_key()` | Adjusts key array length |
| Progression dropdown change | `update_key()` | Updates progression logic |
| Create button | `create()` | Main execution loop |
| Reset button | `reset()` | Clears grid and recreates |
| Randomize button | `randomize()` | Randomizes seed pattern |
| Select Notes button | Opens `NotesSelectWindow` | Modal for note selection |
| Select Colors button | `select_colors()` | Modal for color selection |
| Select Sound button | Opens file dialog | WAV file picker |

### Visualizer Window Callbacks:
- `update(seed, current_note)` - Updates visualization on each cell position

---

## 5. STATE MANAGEMENT

### Application State (`MainApplication` instance):

```python
self.seed_size = 6                    # Board dimension
self.seed = np.zeros((seed_size, seed_size))  # Binary grid state
self.key = [[-5, -1, 2, 7, 14, 19]]   # Base chord (semitone offsets)
self.bpm = "300"                      # Beats per minute
self.note_length_min = "1000"        # Min note duration (ms)
self.note_length_max = "2000"        # Max note duration (ms)
self.note_length_step = "500"        # Random generation step
self.to_play_scale_val = 6           # Number of concurrent notes
self.cycles_entry_val = 10           # Animation cycles
self.colors = ["grey", "#2579E7"]   # Cell colors
self.length_check_val = 0            # Normalize length flag
self.play_check_val = 1              # Playback enabled flag
self.update_type = "Conways"         # Current update rule
self.one_d_rule = "30"               # 1D rule number
self.file = "pizzicatoc4.wav"        # Audio file path
self.progression = [0]               # Chord progression indices
self.key_option_val = "Single Chord" # Key generation mode
```

### Audio State (`SoundAutomata` instance):
```python
self.game_board = seed             # Current automata state
self.size = board_dimension        # Grid dimensions
self.current_note = 0              # Active note row
self.current_key = 0               # Active chord index
self.mixer = PyAudioMixer          # Audio playback mixer
self.initialized = False           # Audio init flag
self.note_array = []               # Loaded notes per semitone
```

---

## 6. AUDIO PLAYBACK FUNCTIONALITY

### Audio System Architecture:

#### **Components:**
1. **PyAudioMixer** - Manages audio stream output
2. **PyAudioNote** - Represents individual playable notes
3. **paulstretch module** - Time-stretches base sound for pitch shifting

#### **Playback Flow:**

```
User clicks "Create" button
    │
    ▼
SoundAutomata.__init__()
    ├─ Initialize PyAudioMixer (if enabled)
    └─ Load base sound file
    
MainApplication.create()
    │
    ├─ Generate notes via Paulstretch (pitch-shifted variants)
    │
    ├─ Loop through cycles and grid cells:
    │     │
    │     ├─ Update visualizer (Tkinter canvas)
    │     ├─ Wait for BPM timing interval
    │     ├─ Identify active cells in automata
    │     ├─ Play notes via PyAudioNote.play()
    │     └─ Apply cellular automata update rule
    │
    └─ Cleanup audio resources on exit
```

#### **PyAudio Integration:**
- Uses `pyaudio.PyAudio` instead of deprecated `pygame.mixer`
- Audio stream: 44100 Hz, stereo, 16-bit
- Notes are pre-generated WAV files based on base sound
- Real-time mixing via stream.write() for concurrent playback

---

## 7. CELLULAR AUTOMATA UPDATE RULES

The app supports these update algorithms:

| Rule | Description | Visual Effect |
|------|-------------|---------------|
| **Conways** | Conway's Game of Life | Organic growth patterns |
| **Up/Down/Left/Right** | Slide pattern in direction | Directional flow effect |
| **1D** | Wolfram 1D cellular automata (rule 0-255) | Complex stripe/fill patterns |
| **Brian's Brain** | 3-state automaton with death rule | Expanding wavefronts |
| **Seeds** | Seed propagation | Spore-like expansion |
| **Langton's Ant** | 2D ant walking rules | Glider-like emergent behavior |
| **No Update** | Static display | No visual change |

---

## 8. TEXTUAL PORT CONSIDERATIONS

### Components to Port:

#### **Canvas Elements → Splits/Static Widgets:**
- Seed grid: Replace with `Splits` widget (6x6 interactive grid)
- Visualizer: Same as above with dynamic updates via `call_after`
- Color canvases: Use `static` widgets with background colors

#### **Modal Windows → Modal Compositions:**
- `ColorSelectWindow`: New Textual modal for color picking (use `ColorPicker` widget or custom)
- `NotesSelectWindow`: Complex modal with 96 checkboxes - use multiple `Checkbox` widgets in a grid

#### **State Management → Reactive State:**
- Use Textual's reactive variables (`self.$seed_size`, `self.$bpm`, etc.)
- Bind to events using `$on('key_down')`, `$on('click')` patterns
- Replace Tkinter callbacks with Textual event handlers

#### **Audio Playback:**
- Keep PyAudio logic (it's framework-agnostic)
- Separate audio subsystem from UI concerns
- Use `loop.call_later()` for BPM timing instead of `time.sleep()`

---

## 9. SUMMARY OF FUNCTIONAL REQUIREMENTS

| Feature | Implementation Approach in Textual |
|---------|-------------------------------------|
| **Seed grid** | Interactive `Splits` component with click handlers |
| **Visualizer** | Dynamic `Splits` updating on cell state changes |
| **Audio playback** | PyAudioMixer class (minimal changes needed) |
| **BPM timing** | `loop.call_later(60/bpm, ...)` for periodic triggers |
| **Note generation** | Paulstretch module (independent of UI framework) |
| **Modal dialogs** | Textual modals or inline compositions |
| **Console output** | `RichText` or custom widget with scroll support |
| **Color picking** | Custom component or use existing `colorsys` logic |
| **State persistence** | Reactive variables + JSON serialization option |

---

*Generated for porting SoundAutomata from Tkinter to Textual while maintaining all functionality.*
