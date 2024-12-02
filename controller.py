from settings import Settings
from business_logic import Board, Coder, Guesser, Game
import random

class GameController():
    def __init__(self):
        self.settings = Settings()
        self.current_game = None
        self.game_mode = None

    def start_new_game(self, game_mode):
        if game_mode == "guesser":
            self.current_game = Game(game_mode, Coder(), Board(), self.generate_random_code())
            self.game_mode = game_mode
        elif game_mode == "coder":
            self.current_game = Game(game_mode, Guesser(), Board(), self.generate_random_code())
            self.game_mode = game_mode
            # Wenn man als Coder spielt, muss der Computer zuerst raten
            self.current_game.computer_guess()
        else:
            raise ValueError("Invalid game mode")
        

    def play_round(self, human_input):
        human_input = [int(i) for i in human_input]
        if self.game_mode == "guesser" and self.validate_guess(human_input):
            # Human Input ist ein Guess
            self.current_game.play_round_human_guesser(human_input)
        elif self.game_mode == "coder" and self.validate_feedback(human_input):
            # Human Input ist ein Feedback
            black = sum(1 for g in human_input if g == 8)
            white = sum(1 for g in human_input if g == 7)
            self.current_game.play_round_human_coder((black, white))
            self.current_game.computer_guess()
        else:
            raise ValueError("Invalid input")

    def validate_guess(self, guess):
        if len(guess) != self.settings.CODE_LENGTH:
            return False
        for color in guess:
            if color not in self.settings.COLORS:
                return False
        return True
    
    def validate_feedback(self, feedback):
        if len(feedback) != self.settings.CODE_LENGTH:
            return False
        for color in feedback:
            if color not in [7, 8, 0]:
                return False
        return True

    def get_board(self):
        return self.current_game.board

    def get_game_over(self):
        # TODO Differentiate between win and lose
        return self.current_game.is_game_over
    
    def generate_random_code(self):
        return [random.choice(self.settings.COLORS) for _ in range(self.settings.CODE_LENGTH)]
    
    def get_secret_code(self):
        return self.current_game.secret_code
    
    def save_game(self):
        self.current_game.save_game()

    def load_game(self):
        self.current_game = Game()
        self.current_game.load_game()

        self.game_mode = self.current_game.game_mode

    def get_game_mode(self):
        return self.game_mode