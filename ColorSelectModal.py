#!/usr/bin/env python3
"""
Color Selection Modal for SoundAutomata Textual Edition

This modal allows users to select and customize the colors used in the visualizer.
Uses only standard Textual widgets available in recent versions.
"""

from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Label, Input
from textual.containers import Vertical, Horizontal, Center


class ColorSelectModal(App):
    """Modal dialog for selecting visualization colors."""

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

    .color-preview {
        width: 30;
        height: 20;
        border: thick $primary;
        margin-bottom: 1;
    }

    .color-entry {
        width: 25;
        margin-top: 1;
    }

    .label-text {
        text-align: center;
        margin-top: 1;
    }

    .button-container {
        justify-content: center;
        margin-top: 1;
    }

    Footer {
        display: none;
    }
    """

    def __init__(self, colors):
        super().__init__()
        self.colors = colors if isinstance(colors, list) else ["grey", "#2579E7"]
        self.console_messages = []

    def compose(self) -> ComposeResult:
        """Compose the modal layout."""
        yield Header()
        yield Static("Select Colors", id="title")
        yield VerticalSpacer(1)

        # Display current colors with previews
        for i, color in enumerate(self.colors):
            # Create color preview box (static text background)
            preview_id = f"preview_{i}"
            entry_id = f"entry_{i}"

            # Preview showing the selected color name/Hex
            yield Static(color if isinstance(color, str) else "",
                        id=preview_id,
                        classes=["color-preview"])

            # Color input field for editing
            yield Input(
                value=color if isinstance(color, str) else "#000000",
                placeholder=f"#{i+1} color",
                id=entry_id,
                classes=["color-entry"],
            )

            yield Label(f"Color {i+1}", id=f"label_{i}", classes=["label-text"])

        # Confirm and Cancel buttons
        yield Horizontal(
            children=[
                Button("Cancel", id="cancel_btn"),
                Button("Confirm", id="confirm_btn"),
            ],
            classes=["button-container"],
        )

        yield VerticalSpacer(1)

    async def confirm_button_pressed(self):
        """Handle confirm button press."""
        new_colors = []

        for i, entry_id in enumerate(
            [f"entry_{i}" for i in range(len(self.colors))]
        ):
            value = self.query_one(entry_id, Input).value.strip()

            # Validate HEX color format
            if value:
                if value.startswith("#") and len(value) in (7, 9):
                    try:
                        int(value[1:], 16)
                        new_colors.append(value)
                    except ValueError:
                        self.console_messages.append(
                            f"Invalid color format for color {i+1}"
                        )
                        new_colors.append(self.colors[i])
                else:
                    # Try as RGB/RGBA without hash
                    try:
                        int(value, 16)
                        new_colors.append(f"#{value}")
                    except ValueError:
                        self.console_messages.append(
                            f"Invalid color format for color {i+1}"
                        )
                        new_colors.append(self.colors[i])
            else:
                new_colors.append(self.colors[i])

        if self.colors != new_colors:
            print(f"Colors updated: {new_colors}")

        await self.exit()

    async def cancel_button_pressed(self):
        """Handle cancel button press."""
        await self.exit()


if __name__ == "__main__":
    modal = ColorSelectModal(["grey", "#2579E7"])
    modal.run()
