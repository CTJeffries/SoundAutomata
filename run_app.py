#!/usr/bin/env python3
"""
SoundAutomata Main Entry Point (PyAudio Version)

Run this script to start the Musical Cellular Automata application.
Requires: pip install pyaudio numpy scipy pygame
"""

import sys
import os

# Add python3 directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
python3_dir = os.path.join(script_dir, 'python3')
sys.path.insert(0, python3_dir)

def main():
    """Main entry point for the application."""
    import tkinter as tk

    try:
        from AutomataApp_py3 import MainApplication
    except ImportError as e:
        print(f"Error importing AutomataApp_py3: {e}")
        print("\nPlease ensure all dependencies are installed:")
        print("  pip install pyaudio numpy scipy pygame")
        return False

    # Create and run the application
    root = tk.Tk()
    root.title("Musical Cellular Automata - PyAudio Version")
    root.geometry("900x700")

    app = MainApplication(root)
    app.grid(row=0, column=0, sticky="nsew")

    # Configure tkinter to run mainloop
    try:
        from pyaudio import PyAudio
        print("PyAudio is available. Audio playback enabled.")
    except ImportError:
        print("Warning: PyAudio not found. Audio playback will be disabled.")

    root.mainloop()

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
