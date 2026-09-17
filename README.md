# Colby Jeffries - Musical Cellular Automata

## About

This project generates musical audio using cellular automata rules. It uses Python 3, Textual (v0.4+) for the GUI, and PyAudio for real-time audio playback with time-stretching support.

## Project Structure

```
SoundAutomata/
├── App.py                         # PRIMARY: Textual GUI application
├── SoundAutomata.py               # Core cellular automata logic
├── ColorSelectModal.py            # Color selection modal
├── NotesSelectModal.py            # Chord/notes selection modal  
├── pyaudio_wrapper.py             # PyAudio mixer abstraction
├── paulstretch.py                 # Time-stretching audio processing
├── examples/                      # Textual GUI demo files
├── python3/                       # Python 2 version (legacy)
├── docs/                          # Documentation
├── pizzicatoc4.wav               # Default audio file
└── requirements.txt               # Python dependencies
```

## Quick Start

### Installation

1. **Navigate to the project:**
   ```bash
   cd SoundAutomata
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

   **Dependencies:**
   - Python 3.8+
   - [Textual](https://textual.textualize.io/) (v0.4+) - GUI framework
   - [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/) - Audio playback
   - numpy, scipy

3. **Audio setup:**
   - macOS: `brew install portaudio` (uv will handle pyaudio installation)
   - Ubuntu/Debian: `sudo apt-get install python3-pyaudio libportaudio0 libportaudio2-dev`

### Running the Application

**Textual version (PRIMARY):**
```bash
python3 App.py
```

## Features

- **Real-time audio playback** with PyAudio and time-stretching
- **Cellular automata rules**: Conway's Game of Life, Brian's Brain, Langton's Ant, etc.
- **Multi-note/chord support** with configurable progressions
- **Visual grid** for seed pattern creation and evolution viewing
- **Modal dialogs** for color and note selection

## Audio System

The audio system uses PyAudio with a custom mixer wrapper that supports:

- Real-time playback without blocking the GUI thread
- Time-stretching using PaulStretch algorithm
- Dynamic sample rate handling
- Efficient buffer management

See `pyaudio_wrapper.py` and `paulstretch.py` for implementation details.

## License

This project is open source and available for educational purposes.

## See Also

- [Textual Documentation](https://textual.textualize.io/)
- [PyAudio Documentation](https://people.csail.mit.edu/hubert/pyaudio/)
- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Documentation](https://docs.scipy.org/doc/scipy/)
- [PaulStretch Time-Stretching](https://github.com/danibvie/paulstretch)

## Author

Colby Jeffries 🎵
