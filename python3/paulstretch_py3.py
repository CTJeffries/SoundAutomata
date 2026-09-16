#!/usr/bin/env python3
#
# Paul's Extreme Sound Stretch (Paulstretch) - Python 3 version ported from Py2
#
# Original: By Nasca Octavian PAUL, Targu Mures, Romania
# Modified for Python 3 compatibility

import sys
from numpy import *
from scipy.io.wavfile import read as read_wav
import wave
from optparse import OptionParser


def load_wav(filename):
    """Load a WAV file and return (samplerate, samples_array)"""
    try:
        samplerate, smp = read_wav(filename)
        # Convert int16 samples to float [-1.0, 1.0]
        smp = smp.astype(np.float32) / 32768.0
        # Ensure stereo
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
    """Stretch audio by the given factor using overlapping windows"""
    nchannels = smp.shape[0]

    # Create output WAV file
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

    # Apply fade-in/fade-out to end of sample array
    nsamples = smp.shape[1]
    end_size = int(samplerate * 0.05)
    if end_size < 16:
        end_size = 16

    # Fade out the end
    smp[:, nsamples - end_size:] *= np.linspace(1, 0, end_size)

    # Calculate displacement for stretched playback
    start_pos = 0.0
    displace_pos = (window_size * 0.5) / stretch

    # Create window function (raised cosine)
    # window = 0.5 - cos(...) * 0.5 was commented out in original
    window = pow(1.0 - pow(np.linspace(-1.0, 1.0, window_size), 2.0), 1.25)

    old_windowed_buf = np.zeros((2, window_size))

    while True:
        # Get the windowed buffer
        istart_pos = int(np.floor(start_pos))
        buf = smp[:, istart_pos:istart_pos + window_size]
        if buf.shape[1] < window_size:
            pad_size = window_size - buf.shape[1]
            buf = np.append(buf, np.zeros((2, pad_size)), axis=1)
        buf = buf * window

        # Get the amplitudes of the frequency components and discard the phases
        freqs = np.abs(np.fft.rfft(buf))

        # Randomize the phases by multiplication with a random complex number with modulus=1
        ph = np.random.uniform(0, 2 * np.pi, (nchannels, freqs.shape[1])) * 1j
        freqs = freqs * np.exp(ph)

        # Do the inverse FFT
        buf = np.fft.irfft(freqs)

        # Window again the output buffer
        buf *= window

        # Overlap-add the output
        output = (buf[:, :half_window_size] + old_windowed_buf[:, half_window_size:window_size])
        old_windowed_buf = buf

        # Clamp the values to -1..1
        np.clip(output, -1.0, 1.0, out=output)

        # Write the output to wav file
        # Convert float32 [-1, 1] to int16 and write frames
        output_int16 = (output.ravel(order='F') * 32767).astype(np.int16)
        outfile.writeframes(output_int16.tobytes())

        start_pos += displace_pos
        if start_pos >= nsamples:
            break

    outfile.close()


def main():
    """Command-line interface for paulstretch"""
    print("Paul's Extreme Sound Stretch (Paulstretch) - Python 3 Port\n")
    parser = OptionParser(usage="usage: %prog [options] input_wav output_wav")
    parser.add_option("-s", "--stretch", dest="stretch",
                      help="stretch amount (1.0 = no stretch)",
                      type="float", default=8.0)
    parser.add_option("-w", "--window_size", dest="window_size",
                      help="window size (seconds)",
                      type="float", default=0.25)
    (options, args) = parser.parse_args()

    if len(args) < 2 or options.stretch <= 0.0 or options.window_size <= 0.001:
        print("Error in command line parameters. Run this program with --help for help.")
        sys.exit(1)

    print(f"stretch amount = {options.stretch}")
    print(f"window size = {options.window_size} seconds")

    result = load_wav(args[0])
    if result is None:
        sys.exit(1)

    samplerate, smp = result
    paulstretch(samplerate, smp, options.stretch, options.window_size, args[1])


if __name__ == "__main__":
    main()
