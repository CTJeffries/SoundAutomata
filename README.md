# Colby Jeffries - Musical Cellular Automata

## About

This is a project to generate audio using cellular automata. The project uses the Python programming language, tkinter for the GUI, and pyaudio for audio playback.

## Project Structure

```
SoundAutomata/
├── python3/                     # Modern Python 3 version (with PyAudio)
│   ├── SoundAutomata_py3.py     # Main sound generation class
│   ├── AutomataApp_py3.py       # GUI application with Tkinter
│   ├── pyaudio_wrapper.py       # PyAudio implementation
│   └── paulstretch_py3.py       # Audio time-stretching utility
├── python2/                     # Legacy Python 2 version (deprecated)
├── pizzicatoc4.wav              # Base sound file
├── MIGRATION_SUMMARY.md         # Migration details
└── README.md                    # This file
```

## Installation

### Dependencies

- Python 3.8+
- pip
- [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/) (audio playback)
- [numpy](https://numpy.org/) (scientific computing)
- [scipy](https://www.scipy.org/) (signal processing)

### Installation Steps

1. **Install dependencies:**
   ```bash
   pip install -r python3/requirements.txt
   ```

2. **On macOS** (if pyaudio installation fails):
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

3. **On Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pyaudio libportaudio0 libportaudio2-dev
   ```

## Usage

### Running the Application

```bash
cd python3
python3 AutomataApp_py3.py
```

### Command Line

For direct audio generation without GUI:
```bash
python3 SoundAutomata_py3.py
```

## Features

- Generate musical notes from a base sound sample
- Multiple cellular automata rules (Conway's Game of Life, Brian's Brain, Langton's Ant, etc.)
- Configurable note playback timing (BPM control)
- Visual representation of the automata grid
- Support for multiple chords and progressions

## Audio Playback (PyAudio)

This project now uses **PyAudio** instead of `pygame` for audio playback. PyAudio provides:

- Better performance and consistent timing
- GUI-friendly non-blocking operations
- No channel limits (unlike pygame's 64-channel limitation)
- Cross-platform compatibility

### Audio Setup

The application automatically initializes PyAudio on startup. If initialization fails, the app will continue running without audio playback.

## Project History

This project was originally developed in Python 2 using pygame for audio. It has been modernized to:

1. Use PyAudio for improved audio playback
2. Run on Python 3 with modern libraries
3. Maintain compatibility with Tkinter GUI framework

## License

This project is open source and available for educational purposes.

## Author

Colby Jeffries

## See Also

- [PyAudio Documentation](https://people.csail.mit.edu/hubert/pyaudio/)
- [numpy documentation](https://numpy.org/doc/)
- [scipy documentation](https://docs.scipy.org/doc/scipy/)
