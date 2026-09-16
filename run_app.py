#!/usr/bin/env python3
"""
Entry point script for running SoundAutomata Python 3 port.
Can be executed directly with: uv run python run_app.py
"""

from AutomataApp_py3 import MainApplication
import tkinter as tk
import sys

def main():
    """Main entry point - runs the GUI application."""
    try:
        root = tk.Tk()
        app = MainApplication(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting SoundAutomata: {e}")
        print("\nTroubleshooting:")
        print("- Ensure tkinter is installed (usually comes with Python 3)")
        print("- Check your audio system is working")
        sys.exit(1)

if __name__ == "__main__":
    main()
