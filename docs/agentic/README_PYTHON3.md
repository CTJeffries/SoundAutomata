# SoundAutomata - Python 3 Port (Current Structure)

This repository now uses a flat structure with Python 3 files at the top level. The Textual-based GUI is the primary version.

## Prerequisites

- Python 3.8+ (Python 3.14+ may have pygame compatibility issues)
- Optional: Python 3.12 recommended for best stability on macOS

## Installation & Running

### Recommended Method:

```bash
python3 App.py
```

### Using pip:

```bash
pip install -r requirements.txt
python3 App.py
```

## Features

- Real-time audio playback with PyAudio and time-stretching
- Cellular automata rules: Conway's Game of Life, Brian's Brain, Langton's Ant
- Multi-note/chord support with configurable progressions
- Visual grid for seed pattern creation and evolution viewing
- Modal dialogs for color and note selection

## Files (Top Level)

- `App.py` - PRIMARY: Textual GUI application
- `SoundAutomata.py` - Core cellular automata logic and sound generation
- `ColorSelectModal.py` - Color selection modal
- `NotesSelectModal.py` - Chord/notes selection modal
- `pyaudio_wrapper.py` - PyAudio mixer abstraction
- `paulstretch.py` - Audio stretching utilities (time-stretching)
- `examples/` - Textual GUI demo files
- `requirements.txt` - Python dependencies

## Legacy Folder

- `python3/` - Legacy folder, no longer used (contains only uv.lock)

## Troubleshooting

### Display Issues:
If the window appears but shows nothing or shows errors:

1. Verify pygame is properly installed:
   ```bash
   pip list | grep pygame-ce
   ```

2. Consider using Python 3.12 instead of 3.14 on macOS:
   ```bash
   /usr/local/opt/python@3.12/bin/python3 App.py
   ```

### Audio Issues:
If audio doesn't play:
- Check that your system's audio is working
- Ensure pygame mixer can initialize (may need admin privileges)

## See Also

- [Main README.md](../README.md) - Getting started guide
- [docs/MIGRATION_NOTES.md](../docs/MIGRATION_NOTES.md) - Migration information
- [docs/PORT_COMPLETE.md](../docs/PORT_COMPLETE.md) - Port status
- [Textual Documentation](https://textual.textualize.io/)
