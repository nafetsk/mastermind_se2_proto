import random
import json

class Code:
    def __init__(self, length=5, colors=None):
        self.colors = colors or [1, 2, 3, 4, 5, 6]  # Default colors
        self.length = length
        self.code = []

    def generate_random(self):
        self.code = [random.choice(self.colors) for _ in range(self.length)]

    def validate_code(self, code):
        return len(code) == self.length and all(c in self.colors for c in code)



class Board:
    def __init__(self):
        self.guesses = []
        self.feedbacks = []
        
    @property
    def rounds(self):
        return len(self.guesses)

    def add_round(self, guess, feedback=None):
        self.guesses.append(guess)
        self.feedbacks.append(feedback)

    def add_guess(self, guess):
        self.guesses.append(guess)
        self.feedbacks.append(None)

    def add_feedback(self, feedback):
        self.feedbacks[-1] = feedback

    def display(self):
        print("\n--- Game Board ---")
        for i in range(self.rounds):
            guess_str = ' '.join(map(str, self.guesses[i]))
            feedback = self.feedbacks[i]
            if feedback:
                print(f"Round {i + 1}: Guess: {guess_str}, Feedback: {feedback[0]} Black, {feedback[1]} White")
            else:
                print(f"Round {i + 1}: Guess: {guess_str}, Feedback: None")
        print("------------------\n")
    


class Player:
    pass


class Coder(Player):
    def create_feedback(self, guess, secret_code):
        """
        Wenn der Computer Coder ist, gibt er korrektes Feedback für den aktuellen guess zurück.
        """
        black = sum(1 for g, c in zip(guess, secret_code) if g == c)
        white = sum(min(secret_code.count(c), guess.count(c)) for c in set(guess)) - black
        return black, white

class Guesser(Player):
    def make_guess(self, board):
        """
        Wenn der Computer Guesser ist, wird ein zufälliger Code generiert.
        später soll das abhängig von den Feedbacks und der Historie sein.
        """
        # Simple random guessing strategy
        possible_colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        guess = [random.choice(possible_colors) for _ in range(5)]
        return guess


class Game:
    def __init__(self, game_mode=None, computer_player=None, board=None, secret_code=None):
        self.game_mode = game_mode
        self.computer_player = computer_player
        self.board = board
        self.secret_code = secret_code
        self.is_game_over = False


    def play_round_human_guesser(self, guess):
        """Der Mensch spielt als Guesser
        menschlicher Guess wird übergeben und zurück kommt ein neues Board sammt dem Feedback des Computers
        """

        self.board.add_round(guess, self.computer_player.create_feedback(guess, self.secret_code))
        self.check_game_over()
        return self.board

    def computer_guess(self):
        """Der Computer generiert einen Guess
        """
        guess = self.computer_player.make_guess(self.board)
        self.board.add_guess(guess)

    def play_round_human_coder(self, human_feedback):
        """Der Mensch spielt als Coder
        Es muss zuvor ein Computer Guess gemacht werden, damit der Mensch Feedback geben kann
        """
        self.board.add_feedback(human_feedback)
        return self.board
    
    def check_game_over(self):
        """Spiel ist vorbei, wenn der letzte Guess korrekt war oder die maximale Anzahl an Runden erreicht wurde
        """
        if self.board.guesses[-1] == self.secret_code or self.board.rounds == 10:
            self.is_game_over = True
            print("Game over!")

    def display_board(self):
        self.board.display()

    def save_game(self):
        """Spiel wird gespeichert indem play_mode, board und secret_code in einer Datei gespeichert werden
        """
        game_state = {
            'game_mode': self.game_mode,
            'board': {
                'guesses': self.board.guesses,
                'feedbacks': self.board.feedbacks,
                'rounds': self.board.rounds
            },
            'secret_code': self.secret_code,
        }

        with open('game_state.json', 'w') as file:
            json.dump(game_state, file, indent=4)

    def load_game(self):
        """Spiel wird geladen
        """
        with open('game_state.json', 'r') as file:
            game_state = json.load(file)

        self.game_mode = game_state['game_mode']
        self.board = Board()
        self.board.guesses = game_state['board']['guesses']
        self.board.feedbacks = game_state['board']['feedbacks']
        self.secret_code = game_state['secret_code']
        


