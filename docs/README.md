# SoundAutomata - Musical Cellular Automata Generator

A musical visualization and sound synthesis project using cellular automata. This project now maintains separate directories for Python 2 and Python 3 implementations.

## Directory Structure

```
SoundAutomata/
├── docs/                 # Documentation (top level, shared between both versions)
│   ├── LICENSE          # Project license
│   ├── MIGRATION_NOTES.md  # Guide for Python 2 to Python 3 migration
│   ├── PORT_COMPLETE.md    # Port completion status
│   ├── pyproject.toml     # Python project configuration
│   └── README.md         # This file
├── python2/              # Original Python 2 version
│   ├── AutomataApp.py
│   ├── SoundAutomata.py
│   ├── paulstretch.py
│   └── README.md         # Python 2 specific documentation
├── python3/              # Python 3 port
│   ├── AutomataApp_py3.py
│   ├── SoundAutomata_py3.py
│   ├── paulstretch_py3.py
│   ├── run_app.py        # Entry point for Python 3 version
│   ├── pyproject.toml    # Python dependencies (uv/pip)
│   ├── README_PYTHON3.md # Python 3 specific documentation
│   └── __pycache__/      # Python bytecode cache (ignored by .gitignore)
└── pizzicatoc4.wav       # Default sound file (shared resource)
```

## Getting Started with Python 3 Version

1. Navigate to the `python3/` directory:
   ```bash
   cd python3
   ```

2. Run the application:
   ```bash
   uv run python run_app.py
   ```

   Or if you have issues with Python 3.14+ and pygame compatibility:
   ```bash
   /usr/local/opt/python@3.12/bin/python3 run_app.py
   ```

## Getting Started with Python 2 Version

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

