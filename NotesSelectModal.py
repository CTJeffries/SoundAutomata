#!/usr/bin/env python3
"""
Notes Selection Modal for SoundAutomata Textual Edition

This modal allows users to select notes for a chord.
Uses only standard Textual widgets available in recent versions.
Shows simplified version for demonstration.
"""

from textual.app import App, ComposeResult
from textual.widgets import Button, Checkbox, Static, Label
from textual.containers import Vertical, Horizontal


class NotesSelectModal(App):
    """Modal dialog for selecting notes in a chord."""

    # Note names for each semitone
    NOTE_NAMES = [
        "C", "C#/Df", "D", "D#/Ef", "E", "F", "F#/Gf",
        "G", "G#/Af", "A", "A#/Bf", "B"
    ]

    # Octave labels (relative)
    OCTAVE_LABELS = ["-3", "-2", "-1", "0", "1", "2", "3", "4"]

    CSS = """
    Screen {
        dock: center;
        align: center middle;
        layout: vertical;
    }

    .title {
        text-align: center;
        font-weight: bold;
        padding: 1;
    }

    Checkbox {
        width: auto;
    }

    .octave-label {
        width: 4;
        text-align: right;
    }

    .button-container {
        justify-content: center;
        margin-top: 1;
    }

    Footer {
        display: none;
    }
    """

    DEFAULT_CSS = ""

    def __init__(self, chord_notes=None):
        super().__init__()
        # If no notes provided, default to all selected in octave 0
        self.selected_notes = set(chord_notes) if chord_notes else {0}

    def compose(self) -> ComposeResult:
        """Compose the modal layout with checkboxes for notes."""
        yield Header()
        yield Static("Select Notes", id="title")

        # Display chord index (demo purposes)
        chord_num = len(self.selected_notes) if self.selected_notes else 0
        yield Static(f"Chord #{chord_num}", id="subtitle")

        # Create rows for each octave
        with Vertical():
            for octave_idx, octave_label in enumerate(self.OCTAVE_LABELS):
                row = Horizontal()

                # Octave label
                label = Label(str(octave_label), id=f"octave_{octave_idx}")
                row.mount(label)

                # Create checkboxes for notes in this octave
                base_offset = -36 + (octave_idx * 12)
                for semitone in range(12):
                    note_idx = base_offset + semitone
                    checkbox = Checkbox(
                        text=self.NOTE_NAMES[semitone % 12],
                        value=note_idx in self.selected_notes,
                        id=f"checkbox_{octave_idx}_{semitone}",
                    )
                    row.mount(checkbox)

                yield row

        # Confirm and Cancel buttons
        yield Horizontal(
            children=[
                Button("Cancel", id="cancel_btn"),
                Button("Confirm", id="confirm_btn"),
            ],
            classes=["button-container"],
        )

        yield VerticalSpacer(1)

    def _on_checkbox_changed(self, event):
        """Handle checkbox change."""
        if event.checkbox.id.startswith("checkbox_"):
            # Extract octave and semitone from id like "checkbox_0_5"
            parts = event.checkbox.id.split("_")
            if len(parts) == 3:
                octave = int(parts[1])
                semitone = int(parts[2])

                note_offset = -36 + (octave * 12)
                absolute_note = note_offset + semitone

                if event.changed and event.value:
                    self.selected_notes.add(absolute_note)
                else:
                    self.selected_notes.discard(absolute_note)

    @property
    def selected_notes_set(self):
        """Get sorted list of selected notes."""
        return sorted(list(self.selected_notes))

    async def confirm_button_pressed(self):
        """Handle confirm button press."""
        # Validate selection - at least one note required
        if not self.selected_notes_set:
            print("Error: At least one note must be selected")
            return

        # Print selected notes (this would be sent back to parent app)
        print(f"Selected notes for chord: {self.selected_notes_set}")

        await self.exit()

    async def cancel_button_pressed(self):
        """Handle cancel button press."""
        await self.exit()


if __name__ == "__main__":
    # Demo modal with some selected notes
    modal = NotesSelectModal([0, 12, 24])  # Example: C4, C5, C6
    modal.run()
