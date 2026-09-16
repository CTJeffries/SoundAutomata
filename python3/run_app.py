#!/usr/bin/env python3
"""
Entry point script for running SoundAutomata Python 3 port.

Usage: python run_app.py

This script initializes the Tkinter GUI for the Musical Cellular Automata Generator.
"""

from AutomataApp import MainApplication
import tkinter as tk
import sys

def main():
    """Main entry point - runs the GUI application."""
    try:
        root = tk.Tk()
        root.title("Musical Cellular Automata")

        # Configure grid geometry manager for root
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        app = MainApplication(root)
        app.grid(row=0, column=0, sticky="nsew")

        # Update idletasks to propagate grid layout to root window
        root.update_idletasks()

        root.mainloop()
    except Exception as e:
        print(f"Error starting SoundAutomata: {e}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        if "NSException" in str(e) or "SDLApplication" in str(e):
            print("- You're using Python 3.14+ which has pygame compatibility issues.")
            print("Solution: Run with Python 3.12 instead:")
            print('  /usr/local/opt/python@3.12/bin/python3 run_app.py')
        else:
            print("- Ensure tkinter is installed (usually comes with Python 3)")
            print("- Check your audio system is working")
        sys.exit(1)

if __name__ == "__main__":
    main()
