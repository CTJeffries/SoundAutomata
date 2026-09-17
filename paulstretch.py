#!/usr/bin/env python3
#
# Paul's Extreme Sound Stretch (Paulstretch) - Python 3 version with PyAudio compatibility
#
# Original: By Nasca Octavian PAUL, Targu Mures, Romania
# Modified for PyAudio format compatibility

import sys
import numpy as np
from scipy.io.wavfile import read as read_wav
import wave


def load_wav(filename):
    """Load a WAV file and return (samplerate, samples_array).

    Returns float32 data normalized to [-1.0, 1.0] for PyAudio compatibility.
    """
    try:
        samplerate, smp = read_wav(filename)
        # Convert int16 samples to float [-1.0, 1.0] - PyAudio standard
        smp = smp.astype(np.float32) / 32768.0
        # Ensure stereo (PyAudio typically expects stereo)
        if smp.ndim == 1:
            smp = np.tile(smp, (2, 1))
        return (samplerate, smp.transpose())
    except Exception as e:
        print(f"Error loading wav: {filename}")
        print(f"Details: {e}")
        return None


def optimize_windowsize(n):
    """Find the smallest integer greater than n that is not divisible by 2, 3, or 5"""
    orig_n = n
    while True:
        temp_n = n
        while temp_n % 2 == 0:
            temp_n //= 2
        while temp_n % 3 == 0:
            temp_n //= 3
        while temp_n % 5 == 0:
            temp_n //= 5

        if temp_n < 2:
            break
        orig_n += 1
        n = orig_n
    return orig_n


def paulstretch(samplerate, smp, stretch, window_size_seconds, outfilename):
    """Stretch audio by the given factor using overlapping windows.

    Args:
        samplerate: Sample rate in Hz (typically 44100)
        smp: Audio samples as float32 array with shape (channels, samples)
        stretch: Stretch factor (1.0 = no stretch, >1 = faster, <1 = slower)
        window_size_seconds: Window size for the stretching algorithm
        outfilename: Output WAV file path

    Returns:
        None. Writes output to outfilename.
    """
    nchannels = smp.shape[0]

    # Create output WAV file (16-bit PCM for compatibility)
    outfile = wave.open(outfilename, "wb")
    outfile.setsampwidth(2)  # 16-bit
    outfile.setframerate(samplerate)
    outfile.setnchannels(nchannels)

    # Calculate window size in samples
    window_size = int(window_size_seconds * samplerate)
    if window_size < 16:
        window_size = 16
    window_size = optimize_windowsize(window_size)
    window_size = int(window_size // 2) * 2
    half_window_size = int(window_size // 2)

    # Apply fade-in/fade-out to end of sample array (prevents clicks)
    nsamples = smp.shape[1]
    end_size = int(samplerate * 0.05)
    if end_size < 16:
        end_size = 16

    # Fade out the end smoothly
    smp[:, nsamples - end_size:] *= np.linspace(1, 0, end_size)

    # Calculate displacement for stretched playback
    start_pos = 0.0
    displace_pos = (window_size * 0.5) / stretch

    # Create raised cosine window function
    window = pow(1.0 - pow(np.linspace(-1.0, 1.0, window_size), 2.0), 1.25)

    old_windowed_buf = np.zeros((nchannels, window_size))

    while True:
        # Get the current windowed buffer
        istart_pos = int(np.floor(start_pos))
        buf = smp[:, istart_pos:istart_pos + window_size]

        # Handle case where remaining samples are less than window size
        if buf.shape[1] < window_size:
            pad_size = window_size - buf.shape[1]
            buf = np.append(buf, np.zeros((nchannels, pad_size)), axis=1)

        # Apply window function
        buf = buf * window

        # Get the amplitudes of the frequency components
        freqs = np.abs(np.fft.rfft(buf))

        # Randomize the phases by multiplication with a random complex number
        ph = np.random.uniform(0, 2 * np.pi, (nchannels, freqs.shape[1])) * 1j
        freqs = freqs * np.exp(ph)

        # Do the inverse FFT to get time-domain signal
        buf = np.fft.irfft(freqs)

        # Window again the output buffer to prevent spectral artifacts
        buf *= window

        # Overlap-add: add current half-window output to previous half-window
        output = (buf[:, :half_window_size] + old_windowed_buf[:, half_window_size:window_size])

        # Clamp values to valid range [-1, 1] to prevent clipping
        np.clip(output, -1.0, 1.0, out=output)

        # Write the output to WAV file
        # Convert float32 [-1, 1] to int16 and write frames
        output_int16 = (output.ravel(order='F') * 32767).astype(np.int16)
        outfile.writeframes(output_int16.tobytes())

        start_pos += displace_pos

        # Exit when we've processed all samples
        if start_pos >= nsamples:
            break

    outfile.close()


def main():
    """Command-line interface for paulstretch"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Paul's Extreme Sound Stretch - Audio time-stretching utility"
    )
    parser.add_argument("input_wav", help="Input WAV file")
    parser.add_argument("output_wav", help="Output stretched WAV file")
    parser.add_argument("-s", "--stretch", dest="stretch",
                        default=1.0, type=float, help="Stretch amount (1.0 = no stretch)")
    parser.add_argument("-w", "--window_size", dest="window_size",
                        default=0.25, type=float, help="Window size in seconds")

    args = parser.parse_args()

    if args.stretch <= 0.0 or args.window_size <= 0.001:
        print("Error: Invalid parameters. Run with --help for usage.")
        sys.exit(1)

    print(f"Stretch amount = {args.stretch}")
    print(f"Window size = {args.window_size} seconds")

    result = load_wav(args.input_wav)
    if result is None:
        sys.exit(1)

    samplerate, smp = result
    paulstretch(samplerate, smp, args.stretch, args.window_size, args.output_wav)
    print(f"Successfully wrote stretched audio to: {args.output_wav}")


if __name__ == "__main__":
    main()
