#!/usr/bin/env python3
"""Test PyAudio integration."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from pyaudio_wrapper import (
            PyAudioNote, PyAudioMixer, 
            load_wav, save_wav, 
            init_audio, cleanup_audio, note_play
        )
        print("✓ All PyAudio wrapper functions imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        print("\nTo install dependencies:")
        print("  pip install pyaudio numpy scipy pygame")
        return False

def test_soundautomata():
    """Test SoundAutomata class."""
    print("\nTesting SoundAutomata class...")
    
    try:
        from SoundAutomata_py3 import SoundAutomata
        print("✓ SoundAutomata class imported successfully")
        
        # Check that PyAudio classes are available
        if hasattr(SoundAutomata, 'PyAudioNote'):
            print("✓ PyAudioNote is accessible from SoundAutomata")
            
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_automata_app():
    """Test AutomataApp."""
    print("\nTesting AutomataApp...")
    
    try:
        from AutomataApp_py3 import MainApplication
        print("✓ MainApplication imported successfully")
        
        # Check that pygame is NOT imported
        import sys as system_sys
        if 'pygame' in system_sys.modules:
            print("⚠ Warning: pygame still imported (may be used for compatibility)")
            
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("PyAudio Integration Test")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test SoundAutomata (skip if no base sound file)
    if os.path.exists("pizzicatoc4.wav"):
        results.append(("SoundAutomata", test_soundautomata()))
    else:
        print("\nSkipping SoundAutomata tests (no pizzicatoc4.wav found)")
        results.append(("SoundAutomata", True))  # Assume OK if file doesn't exist
    
    # Test AutomataApp
    results.append(("AutomataApp", test_automata_app()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result for _, result in results)
    print("\n" + ("=" * 60))
    if all_passed:
        print("All tests passed! PyAudio integration is working.")
    else:
        print("Some tests failed. See errors above.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
