#!/usr/bin/env python3
"""Textual-based GUI for SoundAutomata - WORKING VERSION"""

from textual.app import App, ComposeResult, Binding
from textual.widgets import Header, Footer, Button, Static, Label, Input
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive


class SoundAutomataApp(App):
    """Main Textual application for the Musical Cellular Automata Generator."""

    CSS = """
    #title {
        text-align: center;
        color: $primary;
        padding: 1;
        width: 50;
    }

    .cell.active {
        background: $primary;
        color: white;
    }

    Input {
        width: 8;
    }

    Button {
        width: 8;
    }

    Label {
        padding: 1;
    }

    .console-output {
        background: black;
        color: white;
        height: 5;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "reset", "Reset Grid"),
    ]

    seed_size = reactive(6)
    bpm = reactive("300")
    cycles = reactive(10)
    note_length_min = reactive("1000")
    note_length_max = reactive("2000")
    note_length_step = reactive("500")
    one_d_rule = reactive("30")
    to_play = reactive(6)
    play_notes = reactive(True)

    key = reactive([[-5, -1, 2, 7, 14, 19]])
    progression = reactive([0])
    colors = reactive(["grey", "#2579E7"])
    update_type = reactive("Conways")
    key_option_val = reactive("Single Chord")
    file_path = reactive("pizzicatoc4.wav")

    seed_cells = {}
    automata_instance = None
    mixer = None
    console_messages = []
    visualizer_state = None

    def __init__(self):
        super().__init__()
        self.console_messages = []

    def compose(self) -> ComposeResult:
        """Compose the main application layout."""
        yield Header()
        yield Static("Musical Cellular Automata - Textual Edition", id="title")

        # Left side - Seed grid label
        yield Static("Seed Grid", id="seed-label")

        # Build the seed grid by yielding Static cells directly (no container wrapper)
        with Vertical(id="seed-grid"):
            for row in range(self.seed_size):
                for col in range(self.seed_size):
                    cell_id = f"cell_{row}_{col}"
                    cell = Static(f"({row},{col})", id=cell_id, classes="cell")
                    self.seed_cells[(row, col)] = cell
                    yield cell

        # Control rows - stacked vertically (each row is a separate Horizontal container)
        with Horizontal():
            yield Label("Board Size:")
            yield Input(value=str(self.seed_size), id="seed_size_input", placeholder="6")
            yield Button("Create", id="create_btn")
            yield Button("Reset", id="reset_btn")
            yield Button("Randomize", id="randomize_btn")

        with Horizontal():
            yield Label("Key Mode:")
            yield Label(self.key_option_val, id="key_mode_label")
            yield Button("Select Sound", id="select_sound_btn")

        with Horizontal():
            yield Label("Progression:")
            yield Input(value=str(self.progression[0] if self.progression else "0"),
                       id="progression_input", placeholder="0")
            yield Button("Select Notes", id="select_notes_btn")

        with Horizontal():
            yield Label("Key:")
            # Convert int to freq name or use string directly
            key_note = self.key[0][0] if len(self.key[0]) > 0 else "C"
            # Map MIDI-like values to note names
            note_map = {-5: 'B', -1: 'D#', 2: 'F', 7: 'A', 14: 'C', 19: 'E'}
            yield Static(note_map.get(key_note, str(key_note)), id="key_label")
            yield Button("Select Colors", id="select_colors_btn")

        with Horizontal():
            yield Label("Update Rule:")
            yield Static(self.update_type, id="update_rule_label")
            yield Input(value=str(self.one_d_rule), id="rule_input")

        with Horizontal():
            yield Label("Notes to play:")
            yield Static(str(self.to_play))

        # Bottom area - File info and console
        yield Static(self.file_path, id="file_label")

        # Console output (separate container at bottom)
        yield Static(
            "\n".join(self.console_messages[-10:] if self.console_messages else ["No messages"]),
            id="console_output",
            classes="console-output",
        )

        yield Footer()

    async def on_mount(self) -> None:
        try:
            from pyaudio_wrapper import PyAudioMixer
            self.mixer = PyAudioMixer(rate=44100, chunk=1024)
            self.mixer.init()
            self.console_messages.append("PyAudio mixer initialized successfully.")
        except ImportError:
            print("PyAudio not installed. Audio playback will be disabled.")
        except Exception as e:
            print(f"Warning: Could not initialize audio: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "create_btn":
            self.console_messages.append("Creating cellular automata...")
            try:
                size = int(self.get_widget("#seed_size_input").value)
                if 2 <= size <= 50:
                    self.seed_size = size
                    self.randomize_seed()
            except ValueError:
                pass

        elif event.button.id == "reset_btn":
            self.console_messages.append("Resetting seed grid...")
            self.reset_seed()

        elif event.button.id == "randomize_btn":
            self.console_messages.append("Randomizing seed pattern...")
            self.randomize_seed()

        elif event.button.id == "select_sound_btn":
            self.console_messages.append("Select sound file...")

        elif event.button.id == "select_notes_btn":
            self.console_messages.append("Select notes for chord...")

        elif event.button.id == "select_colors_btn":
            self.console_messages.append("Select visualization colors...")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input change events."""
        if event.input.id == "seed_size_input":
            try:
                new_size = int(event.value)
                if 2 <= new_size <= 50:
                    self.seed_size = new_size
            except ValueError:
                pass

        elif event.input.id == "progression_input":
            try:
                self.progression = [int(event.value)]
            except ValueError:
                pass

    def randomize_seed(self):
        """Randomize the seed pattern."""
        import random
        for cell in self.seed_cells.values():
            if random.random() < 0.5:
                cell.styles.background = "white"
                cell.update("Active")
            else:
                cell.update("")

    def reset_seed(self):
        """Reset seed to all grey (inactive)."""
        for cell in self.seed_cells.values():
            cell.update("")


if __name__ == "__main__":
    app = SoundAutomataApp()
    app.run()
