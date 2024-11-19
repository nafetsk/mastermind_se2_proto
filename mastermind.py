from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Static, Input
from textual.binding import Binding
from random import choices
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Button, Static, Input, Header
from rich.console import RenderableType
from textual import log
from rich.text import Text


class MenuScreen(Screen):
    def compose(self) -> ComposeResult:

        yield Container(
            Static("MENÜ", id="title"),
            Button("NEUES SPIEL", id="new-game", variant="primary"),
            Button("EINSTELLUNGEN", id="settings", variant="primary"),
            Button("EXIT", id="exit", variant="primary"),
            id="menu-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new-game":
            self.app.push_screen(ModeScreen())
        elif event.button.id == "settings":
            self.app.push_screen(SettingsScreen())
        elif event.button.id == "exit":
            self.app.exit()


class ModeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("Spielart auswählen!", id="title"),
            Button("Rater", id="rater", variant="primary"),
            Button("Kodierer", id="kodierer", variant="primary"),
            Button("Back", id="back", variant="primary"),
            id="menu-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "rater":
            self.app.push_screen(RaterScreen())
        elif event.button.id == "kodierer":
            self.app.push_screen(KodiererScreen())
        elif event.button.id == "back":
            self.app.pop_screen()


class ColorPeg(Static):
    """A widget representing a single colored peg."""

    def __init__(self, color: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.update_color()  # Hintergrundfarbe direkt setzen

    def update_color(self):
        """Update the background color of the peg based on its color attribute."""
        color_map = {
            "R": "#ff0000",  # Red
            "G": "#00ff00",  # Green
            "B": "#0000ff",  # Blue
            "Y": "#ffff00",  # Yellow
            "W": "#ffffff",  # White
            "O": "#ffa500",  # Orange
        }
        color_code = color_map.get(self.color, "#363646")
        # Hintergrundfarbe mit self.styles setzen
        self.styles.background = color_code

    def render(self) -> RenderableType:
        return Text("  ")  # Platz für den Peg sicherstellen


class FeedbackPeg(Static):
    """A widget representing a single feedback peg."""

    def __init__(self, color: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.update_color()  # Set the background color directly

    def update_color(self):
        color_map = {
            "B": "#000000",  # Black for correct color and position
            "W": "#ffffff",  # White for correct color but wrong position
        }
        color_code = color_map.get(self.color, "#363646")
        self.styles.background = color_code

    def render(self) -> RenderableType:
        return Text("  ")  # Platz für den Peg sicherstellen


class RaterScreen(Screen):
    COLORS = ["R", "G", "B", "Y", "W", "O"]
    MAX_TRIES = 10

    BINDINGS = [
        Binding("escape", "back_to_menu", "Back to Menu"),
        Binding("enter", "submit_guess", "Submit Guess"),
    ]

    CSS = """
    Screen {
        background: #2b2b3b;
        layers: base overlay;
        align: center middle;  /* Center everything in the screen */
    }

    #game-container {
        width: 100%;
        height: 100%;
        align: center middle;  /* Center its contents */
    }

    #board {
        width: 50%;
        height: 80%;  /* Changed from 70% to auto for better content fitting */
        min-height: 30;  /* Minimum height to ensure visibility */
        border: heavy $accent;
        background: #363646;
        align: center middle;
    }

    .guess-row {
        height: 3;
        layout: horizontal;
        align: center middle;
        padding: 1;
        margin-bottom: 1;
    }

    .peg {
        width: 4;
        height: 3;
        content-align: center middle;
        border: round $accent;
        margin-right: 1;
        background: #FFFFFF;
    }

    .feedback-peg {
        width: 2;
        height: 3;
        content-align: center middle;
        margin-right: 2;
        background: #2b2b3b;
        border: round $accent;
    }

    #input-container {
        layout: horizontal;
        height: 8;
        margin-top: 1;
        background: #464656;
        padding: 1;
        align: center middle;
        width: 50%;  /* Match board width */
    }

    Input {
        margin: 1;
        width: 30;
    }

    Input:focus {
        border: double $accent;
    }

    #submit-button {
        margin: 1;
        width: 10;
    }

    .color-R { background: #ff0000; }
    .color-G { background: #00ff00; }
    .color-B { background: #0000ff; }
    .color-Y { background: #ffff00; }
    .color-W { background: #ffffff; }
    .color-O { background: #ffa500; }
    """

    def __init__(self):
        super().__init__()
        self.secret_code = choices(self.COLORS, k=5)
        self.current_try = 0
        log(f"Secret code: {self.secret_code}")  # For debugging

    def compose(self) -> ComposeResult:
        
        with Vertical(id="game-container"):
            with Vertical(id="board"):
                for row in range(self.MAX_TRIES):
                    with Horizontal(id=f"row-{row}"):
                        with Horizontal(id=f"feedback-{row}"):
                            for feedback_peg in range(5):
                                yield FeedbackPeg(
                                    classes="feedback-peg",
                                    id=f"feedback-{row}-{feedback_peg}",
                                )
                        for peg in range(5):
                            yield ColorPeg(classes="peg", id=f"peg-{row}-{peg}")

            # Input field and submit button at the bottom
            with Horizontal(id="input-container"):
                yield Input(
                    placeholder="Enter 5 colors (R,G,B,Y,W,O)", id="guess-input"
                )
                yield Button("Submit", id="submit-button", variant="primary")

    def on_mount(self) -> None:
        """Focus the input field when the screen is mounted."""
        self.query_one("#guess-input").focus()

    def action_back_to_menu(self) -> None:
        self.app.pop_screen()

    def action_submit_guess(self) -> None:
        """Handle Enter key press."""
        self._handle_input()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        log("Input submitted")
        self._handle_input()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "submit-button":
            self._handle_input()

    def _handle_input(self) -> None:
        """Process the input and update the game state."""
        input_widget = self.query_one("#guess-input", Input)
        guess = input_widget.value.upper().strip()

        # Validate input
        if len(guess) != 5 or not all(c in self.COLORS for c in guess):
            self.notify(
                "Invalid input! Use 5 colors from: R,G,B,Y,W,O", severity="error"
            )
            input_widget.value = ""  # Clear invalid input
            return

        # Update pegs display
        row = self.MAX_TRIES - 1 - self.current_try
        for i, color in enumerate(guess):
            peg = self.query_one(f"#peg-{row}-{i}", ColorPeg)
            peg.color = color
            peg.update_color()  # Aktualisiere die Hintergrundfarbe des Widgets
            peg.refresh()
            log(f"Changing Color of: {peg.id} with color: {peg.color}")

            # Generate feedback
        feedback = self._generate_feedback(guess)
        for i, color in enumerate(feedback):
            feedback_peg = self.query_one(f"#feedback-{row}-{i}", FeedbackPeg)
            feedback_peg.color = color
            feedback_peg.update_color()
            feedback_peg.refresh()
            log(
                f"Changing Color of: {feedback_peg.id} with color: {feedback_peg.color}"
            )

        # Clear the input field for the next guess
        input_widget.value = ""

        # Check if the guess is correct
        if guess == self.secret_code:
            self.notify("Congratulations! You've guessed the code!", severity="success")
            self.app.pop_screen()
        else:
            self.current_try += 1
            if self.current_try >= self.MAX_TRIES:
                self.notify(
                    f"Game Over! The correct code was: {self.secret_code}",
                    severity="error",
                )
                self.app.pop_screen()

    def _generate_feedback(self, guess: str) -> list:
        """Generate feedback for the given guess."""
        feedback = []
        secret_code_copy = list(self.secret_code)
        guess_copy = list(guess)

        # First pass: Check for correct color and position
        for i in range(5):
            if guess_copy[i] == secret_code_copy[i]:
                feedback.append("B")
                secret_code_copy[i] = guess_copy[i] = None

        # Second pass: Check for correct color but wrong position
        for i in range(5):
            if guess_copy[i] and guess_copy[i] in secret_code_copy:
                feedback.append("W")
                secret_code_copy[secret_code_copy.index(guess_copy[i])] = None

        return feedback


class MastermindApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    
    #menu-container {
        width: 40;
        height: 20;
        border: heavy $accent;
        padding: 1 2;
        background: #2b2b3b;
    }
    
    #title {
        color: $text;
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    
    Button {
        width: 100%;
        margin-bottom: 1;
    }
    """

    BINDINGS = [Binding("q", "quit", "Quit the game", show=False)]

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())

    def action_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = MastermindApp()
    app.run()
