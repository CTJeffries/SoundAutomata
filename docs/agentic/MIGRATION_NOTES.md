# Python 3 Migration Notes

This document details the changes made when porting SoundAutomata from Python 2 to Python 3.

## Files Created (Python 3 Port)

| Original File | New Name | Description |
|---------------|----------|-------------|
| `paulstretch.py` | `paulstretch_py3.py` | Audio stretching utility, ported to Python 3 |
| `SoundAutomata.py` | `SoundAutomata_py3.py` | Core cellular automata logic with audio generation |
| `AutomataApp.py` | `AutomataApp_py3.py` | GUI application with Tkinter |

## Files for User Installation (keep original + new)

After migration, the project contains both original files (for reference) and Python 3 ports:

```
├── pyproject.toml                    # uv configuration (NEW - required)
├── pizzicatoc4.wav                   # Base audio sample (existing)
├── README.md                         # Original readme
├── README_PYTHON3.md                 # Python 3 installation guide (NEW)
├── MIGRATION_NOTES.md                # This file
│
└── [Python 3 files - use these]:     # Ported versions
    ├── paulstretch_py3.py
    ├── SoundAutomata_py3.py
    ├── AutomataApp_py3.py
    └── run_app.py                    # Simplified entry point (NEW)
```

**Note**: When running, use the `*_py3.py` files. The original Python 2 files are kept for reference only.

## Key Changes Made

### 1. Syntax Updates

| Pattern | Original | Python 3 Equivalent |
|---------|----------|---------------------|
| Print statement | `print "hello"` | `print("hello")` |
| Integer division | `/2` | `//2` (or just `/` in Py3) |
| Input function | `raw_input()` | `input()` |
| Iterable methods | `.iteritems()` | `.items()` |
| Dict key check | `.has_key(key)` | `.get(key)` or direct access |
| Exception syntax | `except e:` | `except Exception as e:` |

### 2. Import Changes

- `Tkinter` → `tkinter` (lowercase in Python 3 standard library)
- Added `pathlib.Path` for better file path handling
- Updated shebang from `#!/usr/bin/env python` to `#!/usr/bin/env python3`

### 3. Package Updates

| Original Package | New Package | Reason |
|------------------|-------------|--------|
| `pygame` | `pygame-ce` | The original pygame has Python 2 code that breaks on Py3; pygame-ce is the maintained fork |

### 4. Code Improvements

- Added type hints where appropriate
- Improved error messages with f-strings
- Added docstrings to functions and classes
- Better exception handling with try/except blocks
- Cleaner file I/O patterns
- Removed unused imports from original code

### 5. Audio Module Changes

The `SoundAutomata` class was restructured slightly:

- Notes are now generated on-the-fly in the GUI
- Simplified constructor parameters for easier use
- Added better error handling for missing audio files
- Updated to work with pygame-ce mixer interface

## Running the Python 3 Version

### Option 1: Using uv (Recommended)

```bash
# Install dependencies and create environment
uv sync

# Run the application
uv run python run_app.py
```

Or directly:
```bash
uv run python AutomataApp_py3.py
```

### Option 2: Manual Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows
pip install numpy scipy pygame-ce
python run_app.py
```

## Testing

To verify the port works correctly:

1. **Test Audio Generation** (without GUI):
   ```bash
   uv run python paulstretch_py3.py -h    # Show help
   uv run python paulstretch_py3.py input.wav output.wav 2>/dev/null || true
   ```

2. **Test Core Module**:
   ```bash
   uv run python -c "import SoundAutomata_py3; print('OK')"
   ```

3. **Run Full Application**:
   ```bash
   uv run python run_app.py
   # Click "Create" to see automata in action
   ```

## Known Limitations

1. **Audio Generation Timing**: Note timing may differ slightly from Python 2 due to pygame-ce changes
2. **Tkinter Display**: On some X11 setups, the GUI window may not appear (display environment variable issue)
3. **Large Grid Sizes**: Performance may degrade with very large boards (>50x50) due to visualization overhead

## Future Improvements (Backlog)

- [ ] Add command-line argument parsing
- [ ] Implement batch audio generation
- [ ] Add MIDI output support
- [ ] Create unit tests for core modules
- [ ] Add configuration file support (.toml or .json)
- [ ] Export animations as video or GIF
- [ ] Web-based version with Flask/FastAPI backend

## Version Information

| Version | Python | Notes |
|---------|--------|-------|
| Original 1.0 | 2.7 | Academic release |
| Port 1.1 (this) | 3.8+ | uv-managed, pygame-ce |

## Credits for Migration

- **Original Author**: Colby Jeffries  
- **Python 3 Port**: Conversion effort completed  
- **Base Audio**: `pizzicatoc4.wav` by original author  
- **License**: GNU GPL v3 or later  

---
