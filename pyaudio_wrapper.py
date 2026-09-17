#!/usr/bin/env python3
"""
PyAudio Wrapper for SoundAutomata

Provides audio playback functionality using PyAudio instead of pygame.mixer.
Includes classes and functions for loading/saving WAV files, playing notes,
and managing audio initialization/cleanup.
"""

import wave
import numpy as np
import pyaudio


def load_wav(filename: str) -> tuple:
    """Load a WAV file and return (samplerate, samples_array).

    Args:
        filename: Path to the WAV file

    Returns:
        Tuple of (samplerate, samples_array) where samples_array is
        a numpy array with shape (channels, samples) containing float32
        data normalized to [-1.0, 1.0]

    Raises:
        Exception: If the file cannot be loaded
    """
    try:
        wavfile = wave.open(filename, 'rb')
        sample_width = wavfile.getsampwidth()

        if sample_width == 1:
            dtype = np.int8
        elif sample_width == 2:
            dtype = np.int16
        else:
            dtype = np.int16

        frames = wavfile.readframes(wavfile.getnframes())
        smp = np.frombuffer(frames, dtype=dtype).astype(np.float32) / 32768.0

        # Handle mono -> stereo if needed
        if smp.ndim == 1:
            smp = np.column_stack((smp, np.zeros_like(smp)))

        samplerate = wavfile.getframerate()
        wavfile.close()
        return (samplerate, smp.T)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return (None, None)


def save_wav(filename: str, samplerate: int, samples_array: np.ndarray):
    """Save audio data to a WAV file.

    Args:
        filename: Output file path
        samplerate: Sample rate in Hz
        samples_array: Audio samples as numpy array (channels, samples)
    """
    try:
        outfile = wave.open(filename, 'wb')
        outfile.setsampwidth(2)  # 16-bit
        outfile.setframerate(samplerate)
        outfile.setnchannels(samples_array.shape[0])

        samples_int16 = (samples_array * 32767).astype(np.int16)
        outfile.writeframes(samples_int16.tobytes())
        outfile.close()
    except Exception as e:
        print(f"Error saving {filename}: {e}")


class PyAudioNote:
    """Represents a playable audio note."""

    def __init__(self, filename):
        """Initialize a note from a WAV file.

        Args:
            filename: Path to the WAV file for this note
        """
        self.filename = filename
        self.samples = None
        self.samplerate = None
        self.volume = 1.0
        self.pitch = 0

        if self.load():
            self._update_from_samples()

    def load(self):
        """Load the note from file."""
        samplerate, smp = load_wav(self.filename)
        if samplerate is None:
            return False
        self.samplerate = samplerate
        self.samples = smp
        self._update_from_samples()
        return True

    def _update_from_samples(self):
        """Extract note properties from loaded samples."""
        if self.samples is None:
            return
        # Pitch can be derived from frequency content
        if self.samples.shape[1] > 0:
            # Assume C4 (261.63 Hz) as reference pitch for now
            self.pitch = int(self.samples.shape[1])

    def set_volume(self, volume):
        """Set the volume of this note.

        Args:
            volume: Volume level between 0.0 and 1.0
        """
        self.volume = max(0.0, min(1.0, volume))

    def play(self):
        """Play this note."""
        if self.samples is None:
            return False

        # Apply volume and convert to int16 bytes
        data = (self.samples * self.volume * 32767).astype(np.int16)
        return True

    def get_samples(self):
        """Get the raw audio samples."""
        return self.samples

    def get_samplerate(self):
        """Get the sample rate."""
        return self.samplerate


class PyAudioMixer:
    """Manages audio output stream for multiple notes."""

    def __init__(self, rate=44100, chunk=1024):
        """Initialize the mixer.

        Args:
            rate: Sample rate in Hz
            chunk: Number of frames per buffer
        """
        self.rate = rate
        self.chunk = chunk
        self.audio = None
        self.stream = None
        self.initialized = False

        try:
            self.audio = pyaudio.PyAudio()
            # Try to use the default output device
            try:
                default_device = self.audio.get_default_output_device_index()
            except Exception:
                default_device = 0

            # Open output stream
            self.stream = self.audio.open(
                format=self._get_format(),
                channels=2,
                rate=rate,
                output=True,
                exclusive=False,
                output_device_index=default_device
            )
            self.stream.start_stream()
            self.initialized = True
        except ImportError:
            print("PyAudio not available. Audio playback disabled.")
            self.audio = None
            self.stream = None
        except Exception as e:
            print(f"Error initializing PyAudio mixer: {e}")
            self.audio = None
            self.stream = None

    def _get_format(self):
        """Get appropriate PyAudio format based on sample width."""
        try:
            if self.audio.get_sample_size(16) == 2:
                return pyaudio.paInt16
            return pyaudio.paInt32
        except:
            return pyaudio.paInt16

    def init(self):
        """Attempt to initialize the mixer (useful if called multiple times)."""
        if self.audio is None:
            try:
                self.audio = pyaudio.PyAudio()
            except ImportError:
                print("PyAudio not available. Audio playback disabled.")
                return False
            try:
                default_device = self.audio.get_default_output_device_index()
            except Exception:
                default_device = 0

            self.stream = self.audio.open(
                format=self._get_format(),
                channels=2,
                rate=self.rate,
                output=True,
                exclusive=False,
                output_device_index=default_device
            )
            self.stream.start_stream()
            self.initialized = True
            return True
        return True

    def get_init(self):
        """Check if the mixer is initialized."""
        return self.initialized

    def play_note(self, note_obj, delay=0.0, duration=None):
        """Play a note with optional delay.

        Args:
            note_obj: A PyAudioNote object to play
            delay: Delay in seconds before playing the note
            duration: Maximum duration of playback (for cleanup)

        Returns:
            True if the note was queued for playback
        """
        if self.stream is None or self.audio is None:
            return False

        if note_obj is None or note_obj.samples is None:
            return False

        # Apply volume and convert to int16 bytes
        data = (note_obj.samples * note_obj.volume * 32767).astype(np.int16)
        self.stream.write(data.tobytes())

        # Estimate duration based on sample count
        if duration is None:
            duration = len(note_obj.samples[0]) / self.rate * 1.5  # Add headroom
        else:
            duration = min(duration, len(note_obj.samples[0]) / self.rate)

        return True

    def cleanup(self):
        """Cleanup audio resources."""
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass

        if self.audio:
            try:
                self.audio.terminate()
            except:
                pass


def init_audio():
    """Initialize audio for playback.

    Returns:
        PyAudioMixer instance or None if initialization failed
    """
    try:
        mixer = PyAudioMixer(rate=44100, chunk=1024)
        if mixer.init():
            print("PyAudio mixer initialized successfully.")
            return mixer
        else:
            print("Warning: Could not initialize audio. Audio playback will be disabled.")
            return None
    except Exception as e:
        print(f"Error initializing audio: {e}")
        print("Audio playback will be disabled.")
        return None


def cleanup_audio(mixer=None):
    """Cleanup audio resources.

    Args:
        mixer: Optional PyAudioMixer instance to cleanup
    """
    if mixer is None:
        try:
            import pyaudio
            # Try to create and immediately terminate a PyAudio instance
            audio = pyaudio.PyAudio()
            audio.terminate()
        except:
            pass
    else:
        mixer.cleanup()


def note_play(samples, volume=1.0):
    """Play audio samples directly (standalone function).

    Args:
        samples: Audio samples as numpy array or bytes
        volume: Volume level between 0.0 and 1.0

    Returns:
        True if playback was attempted successfully
    """
    try:
        # Initialize mixer if needed
        global _GLOBAL_MIXER
        if _GLOBAL_MIXER is None:
            _GLOBAL_MIXER = PyAudioMixer()
            _GLOBAL_MIXER.init()

        if _GLOBAL_MIXER.stream is None:
            return False

        # Convert to int16 bytes and play
        data = (samples * volume * 32767).astype(np.int16)
        _GLOBAL_MIXER.stream.write(data.tobytes())
        return True
    except Exception as e:
        print(f"Playback error: {e}")
        return False


# Global mixer instance for standalone note_play function
_GLOBAL_MIXER = None
