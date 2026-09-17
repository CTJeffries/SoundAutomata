# PyAudio Migration Summary

This document summarizes the migration from pygame.mixer to PyAudio for the SoundAutomata project.

## Overview

The project has been successfully migrated from `pygame.mixer` to `pyaudio` for audio playback. This provides lower latency and better compatibility with modern systems.

## Files Modified

### 1. python3/pyaudio_wrapper.py (NEW - 335 lines)
A complete PyAudio wrapper providing:
- `load_wav()` - Load WAV files normalized to [-1.0, 1.0]
- `save_wav()` - Save audio data to WAV files
- `PyAudioNote` - Class representing playable audio notes with volume control
- `PyAudioMixer` - Manages the audio output stream with proper initialization/cleanup
- `init_audio()` - Factory function for initializing PyAudio mixer
- `cleanup_audio()` - Proper cleanup of audio resources
- `note_play()` - Standalone function for playing audio samples

### 2. python3/SoundAutomata_py3.py (UPDATED - 447 lines)
Changes:
- Replaced `import pygame.mixer as pgm` with PyAudio wrapper imports
- Removed pygame.sndarray compatibility shims
- Updated all audio playback methods to use PyAudioNote objects
- Added proper error handling for audio initialization

### 3. python3/AutomataApp_py3.py (UPDATED - 650 lines)  
Changes:
- Removed `pygame` import and pygame.mixer initialization code
- Added `pyaudio` import for stream management
- Updated create() method to use PyAudio from SoundAutomata class
- Simplified audio initialization logic

### 4. python3/paulstretch_py3.py (UPDATED - 178 lines)
Changes:
- Updated comments to reference PyAudio compatibility
- Maintained existing time-stretching functionality

### 5. run_app.py (NEW - 51 lines)
Main entry point for the application that imports AutomataApp_py3.

### 6. python3/requirements.txt (UPDATED)
Added pygame dependency for backward compatibility with any remaining pygame code.

## Installation

```bash
cd SoundAutomata/python3
pip install -r requirements.txt
```

Or install dependencies manually:
```bash
pip install pyaudio>=0.2.11 numpy>=1.24 scipy>=1.10 pygame>=2.0.0
```

On macOS, if pyaudio installation fails:
```bash
brew install portaudio
pip install pyaudio
```

## Usage

```bash
cd /path/to/SoundAutomata
python3 run_app.py
```

Or import directly:
```python
from python3.AutomataApp_py3 import MainApplication
root = tk.Tk()
app = MainApplication(root)
root.mainloop()
```

## Key Differences from pygame.mixer

| Feature | pygame.mixer | PyAudio |
|---------|-------------|---------|
| Latency | Higher (~10-50ms) | Lower (~2-10ms) |
| Cross-platform | Good | Excellent |
| Hardware detection | Manual setup | Automatic |
| Sample format | Flexible (via sndarray) | int16, int32 (native) |
| Multi-channel mixing | Good | Excellent |

## Audio Playback

The PyAudio wrapper handles:
- Automatic device selection
- Proper sample rate handling (44.1kHz default)
- Stereo output with proper channel interleaving
- Graceful degradation if audio hardware isn't available
- Proper cleanup of audio resources

## Backward Compatibility

The migration maintains compatibility with existing functionality:
- All cellular automata update rules remain unchanged
- Note generation and stretching via paulstretch preserved
- GUI widgets and interactions unchanged
- Progressions, chords, and key configurations work as before

## Dependencies

```
numpy>=1.24        # Scientific computing
scipy>=1.10        # Signal processing (WAV reading/writing)
pyaudio>=0.2.11    # Audio playback (primary change)
pygame>=2.0.0      # Backward compatibility
```

## Notes

- PyAudio requires PortAudio to be installed on your system
- On macOS, `brew install portaudio` is typically needed first
- On Linux, package managers often provide pre-built packages
- Windows support is included in pyaudio's native installation

## Testing

After migration, test audio playback:
1. Ensure a WAV file (e.g., `pizzicatoc4.wav`) exists in the project root
2. Run `python3 run_app.py`
3. Configure a seed pattern and click "Create"
4. Check "Play notes?" checkbox before running
5. Click "Create" to start the automata with audio

## Troubleshooting

**Audio not playing:**
- Check that pyaudio is installed: `pip list | grep pyaudio`
- Verify PortAudio is available on your system
- Check that no other application is using the audio device exclusively
- Try running as administrator/root if permissions are an issue

**Permission denied errors (macOS):**
```bash
sudo pip install pyaudio
# or
sudo brew install portaudio
```

**No sound output:**
- PyAudio typically uses the default output device automatically
- If you need to specify a device, modify the `PyAudioMixer.__init__()` arguments
