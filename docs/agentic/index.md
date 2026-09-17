# SoundAutomata Documentation Index

## Quick Links

| Document | Location | Description |
|----------|----------|-------------|
| [README](../docs/README.md) | docs/README.md | Main project documentation |
| [Python 2 README](../python2/README.md) | python2/README.md | Python 2 version info |

## Documentation Files

- **docs/README.md** - Main project documentation and getting started guide
- **docs/MIGRATION_NOTES.md** - Complete migration notes from Python 2 to Python 3
- **docs/PORT_COMPLETE.md** - Port completion status and checklist
- **docs/LICENSE** - Project license
- **docs/pyproject.toml** - Example configuration file

## Source Directories

- **python2/** - Original Python 2 implementation (deprecated, maintained for reference)
- **python3/** - Legacy folder (no longer used)
- **examples/** - Textual GUI demo files (top level)

## Running the Application

### Textual Version (PRIMARY - Recommended)

```bash
python3 App.py
```

### Python 2 Version (Legacy)

```bash
cd python2
python AutomataApp.py
```

### Troubleshooting

See [docs/MIGRATION_NOTES.md](./MIGRATION_NOTES.md) for common issues and solutions.

## Repository Structure

```
SoundAutomata/
├── .gitignore                 # Git ignore rules
├── LICENSE                    # Project license (also in docs/)
├── Paper.pdf                  # Academic paper about the project
├── pizzicatoc4.wav            # Default sound sample file
├── requirements.txt           # Python dependencies for development
├── README.md                  # Main documentation root
│
├── App.py                     # PRIMARY: Textual GUI application
├── SoundAutomata.py           # Core cellular automata logic
├── ColorSelectModal.py        # Color selection modal
├── NotesSelectModal.py        # Chord/notes selection modal
├── pyaudio_wrapper.py         # PyAudio mixer abstraction
├── paulstretch.py             # Time-stretching audio processing
└── examples/                  # Textual GUI demo files

├── python2/                   # Python 2 source code (deprecated)
│   ├── AutomataApp.py
│   ├── SoundAutomata.py
│   ├── paulstretch.py
│   └── README.md
│
└── python3/                   # Legacy folder (renamed from python3/)
    └── uv.lock                # Dependency lock file

└── docs/                      # Shared documentation folder
    ├── LICENSE               # License copy
    ├── MIGRATION_NOTES.md    # Migration guide
    ├── PORT_COMPLETE.md      # Port status
    ├── pyproject.toml        # Example config
    └── README.md             # Main documentation
```
