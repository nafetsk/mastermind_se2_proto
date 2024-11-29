import unittest
from business_logic import Game, Board, Coder, Guesser, Code

class TestGame(unittest.TestCase):

    def setUp(self):
        self.secret_code = [1, 2, 3, 4, 5]
        self.board = Board()
        self.coder = Coder()
        self.guesser = Guesser()
        self.game = Game(game_mode="human_guesser", computer_player=self.coder, board=self.board, secret_code=self.secret_code)

    def test_play_round_human_guesser_correct_guess(self):
        guess = [1, 2, 3, 4, 5]
        self.game.play_round_human_guesser(guess)
        self.assertTrue(self.game.is_game_over)
        self.assertEqual(self.board.guesses[-1], guess)
        self.assertEqual(self.board.feedbacks[-1], (5, 0))

    def test_play_round_human_guesser_incorrect_guess(self):
        guess = [1, 1, 1, 1, 1]
        self.game.play_round_human_guesser(guess)
        self.assertFalse(self.game.is_game_over)
        self.assertEqual(self.board.guesses[-1], guess)
        self.assertEqual(self.board.feedbacks[-1], (1, 0))

    def test_play_round_human_coder(self):
        self.game = Game(game_mode="human_coder", computer_player=self.guesser, board=self.board, secret_code=self.secret_code)
        guess = [1, 1, 1, 1, 1]
        self.game.board.add_guess(guess)
        feedback = (1, 0)
        self.game.play_round_human_coder(feedback)
        self.assertEqual(self.board.feedbacks[-1], feedback)

    def test_check_game_over(self):
        guess = [1, 2, 3, 4, 5]
        self.game.play_round_human_guesser(guess)
        self.assertTrue(self.game.is_game_over)

    def test_save_and_load_game(self):
        guess = [1, 2, 3, 4, 5]
        self.game.play_round_human_guesser(guess)
        self.game.save_game()

        new_game = Game()
        new_game.load_game()
        self.assertEqual(new_game.game_mode, self.game.game_mode)
        self.assertEqual(new_game.board.guesses, self.game.board.guesses)
        self.assertEqual(new_game.board.feedbacks, self.game.board.feedbacks)
        self.assertEqual(new_game.secret_code, self.game.secret_code)

if __name__ == "__main__":
    unittest.main()