# SoundAutomata - Musical Cellular Automata Generator

A musical visualization and sound synthesis project using cellular automata. This project now maintains separate directories for Python 2 and Python 3 implementations.

## Directory Structure

```
SoundAutomata/
├── App.py                      # PRIMARY: Textual GUI application
├── SoundAutomata.py            # Core cellular automata logic
├── ColorSelectModal.py         # Color selection modal
├── NotesSelectModal.py         # Chord/notes selection modal
├── pyaudio_wrapper.py          # PyAudio mixer abstraction
├── paulstretch.py              # Time-stretching audio processing
├── examples/                   # Textual GUI demo files
├── python3/                    # Python 2 version (legacy, now unused)
│   └── uv.lock                 # Dependency lock file
├── python2/                    # Original Python 2 version (deprecated)
│   ├── AutomataApp.py
│   ├── SoundAutomata.py
│   ├── paulstretch.py
│   └── README.md               # Python 2 specific documentation
├── docs/                       # Documentation (top level, shared between versions)
│   ├── LICENSE                 # Project license
│   ├── MIGRATION_NOTES.md      # Guide for Python 2 to Python 3 migration
│   ├── PORT_COMPLETE.md        # Port completion status
│   ├── pyproject.toml          # Python project configuration
│   └── README.md               # This file
└── pizzicatoc4.wav             # Default sound file (shared resource)
```

## Getting Started with Textual Version (PRIMARY - Recommended)

1. Navigate to the project directory:
   ```bash
   cd SoundAutomata
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run the application:
   ```bash
   python3 App.py
   ```

## Getting Started with Python 2 Version (Legacy)

1. Navigate to the `python2/` directory:
   ```bash
   cd python2
   ```

2. Run the application (requires Python 2.x and pygame installed):
   ```bash
   python AutomataApp.py
   ```

## Documentation Files

| File | Description |
|------|-------------|
| [README.md](./README.md) | Main project documentation |
| [MIGRATION_NOTES.md](./MIGRATION_NOTES.md) | Python 2 to 3 migration guide |
| [PORT_COMPLETE.md](./PORT_COMPLETE.md) | Port completion status |

## License

See the [LICENSE](./LICENSE) file.

