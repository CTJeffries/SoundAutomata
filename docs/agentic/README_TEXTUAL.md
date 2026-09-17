# SoundAutomata - Textual Edition

This is a port of the Tkinter-based Musical Cellular Automata Generator to the Textual framework. It maintains all the original functionality while using Textual's reactive UI patterns.

## Features

- Interactive cellular automata visualization grid
- Real-time audio playback using PyAudio
- Multiple update rules (Conway's Game of Life, 1D automata, etc.)
- Chord progression support
- Modal dialogs for color and note selection
- Console output for debugging

## Installation

```bash
# Install dependencies
uv sync  # Or: pip install -r requirements.txt

# This includes textual>=0.4.0 automatically
```

## Running the Application

```bash
python3 python3/App_textual.py
```

Or using uv:
```bash
uv run python3 python3/App_textual.py
```

## Controls

- **Board Size** - Input field to set grid dimensions (2-50)
- **BPM** - Beats per minute for timing
- **Cycles** - Number of animation cycles
- **Note Duration** - Min/max duration in milliseconds
- **Key Mode** - Single/Multiple/Generated chords
- **Update Rule** - Cellular automata update algorithm

## Buttons

- **Create** - Initialize and start the cellular automata
- **Reset** - Clear grid
- **Randomize** - Random seed pattern
- **Select Sound** - Choose audio file (placeholder modal)
- **Select Notes** - Choose chord notes (placeholder modal)
- **Select Colors** - Choose visualization colors (placeholder modal)

## Keyboard Shortcuts

- `q` - Quit application
- `r` - Reset grid

## Differences from Tkinter Version

| Feature | Tkinter Original | Textual Port |
|---------|------------------|--------------|
| UI Framework | Tkinter | Textual |
| Reactive State | Callbacks | Reactive variables |
| Layout | Grid geometry manager | Textual layout system |
| Modals | Toplevel windows | Modal compositions |
| Console | Text widget | Static widget |

## Notes

- Audio playback uses PyAudio (same as Tkinter version)
- Sound files must be in the directory or selected via modal
- All update rules from original are supported
- Grid visualization matches original behavior

## Troubleshooting

### PyAudio not found
```bash
pip install pyaudio
```

### Missing sound file
Place a WAV file named `pizzicatoc4.wav` in the directory, or use the "Select Sound" button to specify a path.

### Audio doesn't work
Make sure your audio system is available and PyAudio is properly installed.

## License

Same as original Tkinter version.
