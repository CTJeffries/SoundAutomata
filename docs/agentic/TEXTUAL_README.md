# SoundAutomata - Textual Port (Current Structure)

This repository uses a flat structure with all Python 3 files at the top level. The Textual-based GUI is the primary application version.

## Quick Start

### Installation

```bash
cd /Users/colbyjeffries/Workspace/SoundAutomata
pip install -r requirements.txt
```

### Running the Application

```bash
# Full application (recommended)
python3 App.py

# Simple demo from examples folder
python3 examples/example_textual_simple.py
```

## Features

- Interactive cellular automata grid (6x6 by default)
- Configurable board size (2-50)
- BPM and timing controls
- Multiple update rules supported: Conway's Game of Life, Brian's Brain, Langton's Ant
- Console output for debugging
- Modal dialogs for color/note selection

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `r` | Reset grid |

## Files Overview (Top Level)

### Core Application
- **`App.py`** - Main Textual app with all controls and widgets
- **`SoundAutomata.py`** - Core cellular automata logic
- **`examples/example_textual_simple.py`** - Simplified demo for testing

### Modal Dialogs (standalone)
- **`ColorSelectModal.py`** - Color selection modal
- **`NotesSelectModal.py`** - Notes/selection modal

### Audio Support
- **`pyaudio_wrapper.py`** - PyAudio integration
- **`paulstretch.py`** - Audio time-stretching utilities

### Configuration
- **`requirements.txt`** - Python dependencies
- **`pyproject.toml`** - Project configuration (uv/pip)

## How It Works

The Textual app maintains all the functionality:

1. **State Management**: Uses Textual's reactive variables for grid state
2. **Layout**: Grid-based layout using Textual containers (`Horizontal`, `Vertical`)
3. **Events**: Button presses, input changes handled via event handlers (`on_button_pressed`, `on_input_changed`)
4. **Modals**: Can be integrated with main app for color/note selection

## Differences from Original Tkinter Version

| Feature | Original Tkinter | Textual Port |
|---------|------------------|--------------|
| UI Framework | Tkinter | Textual (v0.4+) |
| Reactive Pattern | Callbacks | `$seed_size_changed()` style declarative |
| Layout System | Grid manager | Textual layout system with containers |
| Widgets | tk widgets | textual.widgets |

## Next Steps

To integrate modals and audio playback:

1. Connect "Select Sound" button to file picker or use default `pizzicatoc4.wav`
2. Wire up modal dialogs from buttons
3. Integrate PyAudioMixer with cellular automata loop
4. Add actual note generation using Paulstretch time-stretching

All of these are straightforward implementations following the patterns in the code.

## Troubleshooting

### "ModuleNotFoundError: No module named 'textual'"

Install Textual first:
```bash
pip install textual pyaudio numpy scipy
```

### Import errors with widgets

The code uses standard Textual widgets. If you're using an older version, some widgets may not be available yet. Update:
```bash
pip install --upgrade textual
```

## License

Same as original Tkinter version.
