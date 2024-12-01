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
from settings import Settings
from controller import GameController


class MenuScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Container(
            Static(self.app.settings.get_text("menu_title"), id="title"),
            Button(self.app.settings.get_text("new_game"), id="new-game", variant="primary"),
            Button(self.app.settings.get_text("load_game"), id="load-game", variant="primary"),
            Button(self.app.settings.get_text("settings"), id="settings", variant="primary"),
            Button(self.app.settings.get_text("exit"), id="exit", variant="primary"),
            id="menu-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new-game":
            self.app.push_screen(ModeScreen())
        elif event.button.id == "settings":
            self.app.push_screen(SettingsScreen())
        elif event.button.id == "load-game":
            self.app.push_screen(GameScreen(load_game=True))
        elif event.button.id == "exit":
            self.app.exit()


class ModeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static(self.app.settings.get_text("select_mode"), id="title"),
            Button(self.app.settings.get_text("guesser"), id="guesser", variant="primary"),
            Button(self.app.settings.get_text("coder"), id="coder", variant="primary"),
            Button(self.app.settings.get_text("back"), id="back", variant="primary"),
            id="menu-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "guesser":
            self.app.push_screen(GameScreen(game_mode="guesser"))
        elif event.button.id == "coder":
            self.app.push_screen(GameScreen(game_mode="coder"))
        elif event.button.id == "back":
            self.app.pop_screen()

class SettingsScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Container(
            Static(self.app.settings.get_text("choose_language"), id="title"),
            Button(self.app.settings.get_text("english"), id="en", variant="primary"),
            Button(self.app.settings.get_text("german"), id="de", variant="primary"),
            Button(self.app.settings.get_text("back"), id="back", variant="primary"),
            id="menu-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "en":
            self.app.settings.set_language("en")
            self.app.push_screen(MenuScreen())
        elif event.button.id == "de":
            self.app.settings.set_language("de")
            self.app.push_screen(MenuScreen())
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
            1: "#ff0000",  # Red
            2: "#00ff00",  # Green
            3: "#ffff00",  # Yellow
            4: "#0000ff",  # Blue
            5: "#ffa500",  # Orange
            6: "#8b4513",  # Brown
            7: "#ffffff",  # White
            8: "#000000",  # Black
            
        }
        color_code = color_map.get(self.color, "#363646")
        # Hintergrundfarbe mit self.styles setzen
        self.styles.background = color_code

    def render(self) -> RenderableType:
        return Text("  ")  # Platz für den Peg sicherstellen


class GameScreen(Screen):

    BINDINGS = [
        Binding("escape", "save_and_back_to_menu", "Back to Menu"),
        Binding("enter", "submit_guess", "Submit Guess"),
    ]

    def __init__(self, game_mode: str = None, load_game: bool = False):
        super().__init__()
        if load_game:
            self.game_controller = GameController()
            self.game_controller.load_game()
            self.game_mode = self.game_controller.get_game_mode()
        else:
            self.game_mode = game_mode
            self.game_controller = GameController()
            self.game_controller.start_new_game(game_mode)
        
        print("game_mode: ", game_mode)
        
    def compose(self) -> ComposeResult:
        with Vertical(id="game-container"):
            if self.game_mode == "coder":
                with Horizontal(id="secret-code-container"):
                    secret_code = self.game_controller.get_secret_code()
                    print("Rendering Secret Code:", secret_code)
                    for index, color in enumerate(secret_code):
                        yield ColorPeg(classes="peg", color=color, id=f"secret-peg-{index}")
            with Vertical(id="board"):
                for row in range(self.app.settings.MAX_ROUNDS):
                    with Horizontal(id=f"row-{row}"):
                        with Horizontal(id=f"feedback-{row}"):
                            for feedback_peg in range(5):
                                yield ColorPeg(
                                    classes="feedback-peg",
                                    id=f"feedback-{row}-{feedback_peg}",
                                )
                        for peg in range(5):
                            yield ColorPeg(classes="peg", id=f"peg-{row}-{peg}")

            # Input field and submit button at the bottom
            with Horizontal(id="input-container"):
                yield Input(
                    placeholder=self.app.settings.get_text("enter_colors"), id="guess-input"
                )
                yield Button(self.app.settings.get_text("submit"), id="submit-button", variant="primary")
                if self.game_mode == "guesser":
                    yield Static(self.app.settings.get_text("color_encoding_guesser"), id="color_encoding")
                else:
                    yield Static(self.app.settings.get_text("color_encoding_coder"), id="color_encoding")

    def on_mount(self) -> None:
        """Focus the input field when the screen is mounted."""
        self._update_board(self.game_controller.get_board())
        self.query_one("#guess-input").focus()


    def action_save_and_back_to_menu(self) -> None:
        """Save the game and go back to the menu."""
        self.game_controller.save_game()
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
        input_widget = self.query_one("#guess-input", Input)
        human_input = input_widget.value

        print("human_input: ",human_input)

        self._update_board(self.game_controller.get_board())

        try:
            self.game_controller.play_round(human_input)
        except ValueError:
            self.notify(
                self.app.settings.get_text("invalid_input"), severity="error"
            )
            input_widget.value = ""
            return

        self._update_board(self.game_controller.get_board())
        print(self.game_controller.current_game.display_board())

        input_widget.value = ""

        if self.game_controller.get_game_over():
            self.notify(self.app.settings.get_text("congratulations"), severity="success")
            self.app.pop_screen()

    def _update_board(self, board):
        for i, (guess, feedback) in enumerate(zip(board.guesses, board.feedbacks)):
            row = self.app.settings.MAX_ROUNDS - 1 - i
            for j, color in enumerate(guess):
                peg = self.query_one(f"#peg-{row}-{j}", ColorPeg)
                peg.color = color
                peg.update_color()
                peg.refresh()
            if feedback:
                black_pegs, white_pegs = feedback
                for j in range(black_pegs):
                    feedback_peg = self.query_one(f"#feedback-{row}-{j}", ColorPeg)
                    feedback_peg.color = 8
                    feedback_peg.update_color()
                    feedback_peg.refresh()
                for j in range(black_pegs, black_pegs + white_pegs):
                    feedback_peg = self.query_one(f"#feedback-{row}-{j}", ColorPeg)
                    feedback_peg.color = 7
                    feedback_peg.update_color()
                    feedback_peg.refresh()


class MastermindApp(App):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    CSS_PATH = "tcss/mastermind.tcss"

    BINDINGS = [Binding("q", "quit", "Quit the game", show=False)]

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())

    def action_quit(self) -> None:
        self.exit()

