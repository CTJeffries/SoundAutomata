# SoundAutomata - Musical Cellular Automata Generator 🎵

## Python 3 Port (with uv package management)

This is a modern **Python 3** port of the original academic music generation project, now managed with [uv](https://github.com/astral-sh/uv) for fast dependency installation.

[**Get Started with Python 3** →](README_PYTHON3.md)

## What It Does

SoundAutomata generates music using **cellular automata** - mathematical patterns that evolve over time. Each "alive" cell in a 2D grid triggers musical notes, creating generative compositions based on classic rules like:

- Conway's Game of Life
- Brian's Brain  
- Langton's Ant
- Seeds
- And more!

## Quick Start (Python 3)

```bash
# Install uv if needed: https://docs.astral.sh/uv/getting-started/installation/

cd /Users/colbyjeffries/Workspace/SoundAutomata
uv sync              # Install dependencies
uv run python run_app.py   # Run the GUI application
```

See [README_PYTHON3.md](README_PYTHON3.md) for complete installation instructions.

## Project Files

- **pyproject.toml** - uv project configuration with numpy, scipy, pygame-ce
- **paulstretch_py3.py** - Audio stretching utility  
- **SoundAutomata_py3.py** - Core cellular automata logic
- **AutomataApp_py3.py** - Tkinter GUI application
- **run_app.py** - Simplified entry point

## License

Released under the [GNU GPL v3](LICENSE) license. See the accompanying paper for academic details.

---

*Making Music with Cellular Automata - Academic Research Project*

**See [MIGRATION_NOTES.md](MIGRATION_NOTES.md) for technical details about the Python 3 port.**
