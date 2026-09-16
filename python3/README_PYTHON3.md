# SoundAutomata - Python 3 Port

This directory contains the actively maintained Python 3 port of the Musical Cellular Automata Generator.

## Prerequisites

- Python 3.8+ (Python 3.14+ may have pygame compatibility issues)
- Optional: Python 3.12 recommended for best stability on macOS

## Installation & Running

### Recommended Method (uv):

```bash
cd python3
uv run python run_app.py
```

### Alternative Methods:

**Using pip:**
```bash
cd python3
pip install -r requirements.txt
python run_app.py
```

**Running without installing dependencies:**
```bash
cd python3
uv sync && uv run python run_app.py
```

### If you experience pygame compatibility issues (Python 3.14+):

```bash
/usr/local/opt/python@3.12/bin/python3 run_app.py
```

## Features

- Cellular automata visualization with sound synthesis
- Multiple rule sets: Conway's Game of Life, Brian's Brain, Langton's Ant
- Chord progression generation
- Real-time audio playback
- Customizable colors and note selection

## Files

- `run_app.py` - Entry point for the GUI application
- `AutomataApp_py3.py` - Main application with Tkinter interface
- `SoundAutomata_py3.py` - Cellular automata logic and sound generation
- `paulstretch_py3.py` - Audio stretching utilities
- `pyproject.toml` - Project dependencies (uv/pip)

## Troubleshooting

**Windows/Mac Display Issues:**
If the window appears but shows nothing or shows errors, try:

1. Verify pygame is properly installed:
   ```bash
   uv pip list | grep pygame-ce
   ```

2. Check for SDL errors in console output - these indicate version incompatibilities

3. Consider using Python 3.12 instead of 3.14 on macOS:
   ```bash
   /usr/local/opt/python@3.12/bin/python3 run_app.py
   ```

**Audio Issues:**
If audio doesn't play:
- Check that your system's audio is working
- Ensure pygame mixer can initialize (may need admin privileges)

## See Also

- [MIGRATION_NOTES.md](../docs/MIGRATION_NOTES.md) - Python 2 to 3 migration guide
- [PORT_COMPLETE.md](../docs/PORT_COMPLETE.md) - Port completion status
