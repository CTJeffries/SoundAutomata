# SoundAutomata Documentation Index

## Quick Links

| Document | Location | Description |
|----------|----------|-------------|
| [README](./README.md) | docs/README.md | Main project documentation |
| [Python 3 README](../python3/README_PYTHON3.md) | python3/README_PYTHON3.md | Python 3 port guide |
| [Python 2 README](../python2/README.md) | python2/README.md | Python 2 version info |

## Documentation Files

- **docs/README.md** - Main project documentation and getting started guide
- **docs/MIGRATION_NOTES.md** - Complete migration notes from Python 2 to Python 3
- **docs/PORT_COMPLETE.md** - Port completion status and checklist
- **docs/LICENSE** - Project license
- **docs/pyproject.toml** - Example configuration file

## Source Directories

- **python2/** - Original Python 2 implementation (deprecated, maintained for reference)
- **python3/** - Actively maintained Python 3 port

## Running the Application

### Python 3 Version (Recommended)

```bash
cd python3
uv run python run_app.py
```

### Python 2 Version

```bash
cd python2
python AutomataApp.py
```

### Troubleshooting

See [docs/MIGRATION_NOTES.md](./MIGRATION_NOTES.md) for common issues and solutions.

## Repository Structure

```
SoundAutomata/
├── .gitignore           # Git ignore rules
├── LICENSE              # Project license (also in docs/)
├── Paper.pdf            # Academic paper about the project
├── pizzicatoc4.wav      # Default sound sample file
├── requirements.txt     # Python dependencies for development
├── README.md            # This documentation root (in docs/ as well)
│
├── docs/                # Shared documentation folder
│   ├── LICENSE         # License copy
│   ├── MIGRATION_NOTES.md  # Migration guide
│   ├── PORT_COMPLETE.md  # Port status
│   ├── pyproject.toml   # Example config
│   └── README.md        # Main documentation
│
├── python2/             # Python 2 source code (deprecated)
│   ├── AutomataApp.py
│   ├── SoundAutomata.py
│   ├── paulstretch.py
│   └── README.md
│
└── python3/             # Python 3 source code
    ├── AutomataApp_py3.py
    ├── SoundAutomata_py3.py
    ├── paulstretch_py3.py
    ├── run_app.py
    ├── pyproject.toml
    └── README_PYTHON3.md
```
