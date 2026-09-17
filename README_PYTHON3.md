# SoundAutomata - Python 3 Version with PyAudio

## Overview

This is the Python 3 port of the Musical Cellular Automata project, using **PyAudio** for audio playback instead of pygame.

## Quick Start

### Installation

```bash
cd python3
pip install -r requirements.txt
python3 AutomataApp_py3.py
```

## PyAudio Migration Notes

### What Changed from Python 2 Version?

- **Audio Library**: Migrated from `pygame.mixer` to `pyaudio`
- **Better Performance**: Non-blocking audio operations in GUI context
- **No Channel Limits**: Can play more simultaneous sounds than pygame (which was limited to 64 channels)

### Usage Changes

The API is identical to the Python 2 version. The main difference is under the hood:

**Old (pygame.mixer):**
```python
import pygame.mixer as pgm
pgm.init()
sound = pgm.Sound("note.wav")
sound.play()
```

**New (PyAudio):**
```python
from pyaudio_wrapper import SimplePyAudio
player = SimplePyAudio()
player.play(samples)
```

But you don't need to change your code! The SoundAutomata class abstracts this away.

### Troubleshooting Audio Issues

If audio doesn't play:

1. **Check if PyAudio is installed:**
   ```bash
   python3 -c "import pyaudio; print(pyaudio.__version__)"
   ```

2. **On macOS, ensure PortAudio is installed:**
   ```bash
   brew install portaudio
   pip install --upgrade pyaudio
   ```

3. **Restart the application** after installing dependencies

4. **Check system audio settings** - ensure output device is set correctly

## Directory Structure

```
python3/
├── AutomataApp_py3.py       # Main GUI application (PyAudio)
├── SoundAutomata_py3.py     # Sound generation (PyAudio playback)
├── pyaudio_wrapper.py       # Simplified PyAudio implementation
├── paulstretch_py3.py       # Audio time-stretching (PyAudio format)
└── requirements.txt         # Python 3 dependencies
```

## API Reference

### SoundAutomata Class

```python
sound = SoundAutomata(
    parent=app,                    # Tkinter app reference
    seed=grid,                     # Initial grid state
    sound="pizzicatoc4.wav",      # Base sound file
    key=[chord_notes],            # Notes to play
    length_adjusted=False,         # Pre-generate notes?
    window_size=0.5               # Time-stretch window size
)

# Initialize audio (usually done automatically in create())
sound.init_audio()

# Play is handled automatically when cellular automata evolves
```

### Application Events

- **Create**: Initializes PyAudio and generates note files if needed
- **Play Check**: Enable/disable audio playback toggle
- **BPM Control**: Set playback speed (beats per minute)
- **Note Length Min/Max**: Range for randomized note durations
- **Cycles**: Number of automata iterations

## Performance Notes

### Why PyAudio Over pygame?

1. **Lower Latency**: PyAudio typically provides more consistent timing
2. **Better GUI Integration**: Non-blocking calls work well with Tkinter event loop
3. **Higher Channel Count**: Can play unlimited simultaneous sounds (pygame limited to 64)
4. **Cross-platform**: Consistent behavior on Windows, macOS, and Linux

### Audio Thread Safety

The PyAudio implementation handles thread safety by:
- Using a single shared audio stream
- Non-blocking playback calls that return immediately
- Proper cleanup in `__del__` method

## Advanced Usage

### Direct Audio Playback (without GUI)

```python
from SoundAutomata_py3 import SoundAutomata
from pyaudio_wrapper import SimplePyAudio

# Create player
player = SimplePyAudio()
samplerate, samples = load_wav("pizzicatoc4.wav")

# Play stretched audio
stretched = speedx(samples, factor)
player.play(stretched)
```

### Customizing Audio Output

Modify `pyaudio_wrapper.py` to:
- Change sample rate (default 44100 Hz)
- Adjust buffer size for latency control
- Use different output devices

## Dependencies

See `python3/requirements.txt` for full list.

## License

Open source educational project.
