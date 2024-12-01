from business_logic import Board, Coder, Guesser, Game


def test_play_round_human_guesser_correct_guess():
    secret_code = [1, 2, 3, 4, 5]
    board = Board()
    coder = Coder()
    game = Game(game_mode="guesser", computer_player=coder, board=board, secret_code=secret_code)

    guess = [1, 2, 3, 4, 5]
    game.play_round_human_guesser(guess)
    assert game.is_game_over
    assert board.guesses[-1] == guess
    assert board.feedbacks[-1] == (5, 0)


def test_play_round_human_guesser_incorrect_guess():
    secret_code = [1, 2, 3, 4, 5]
    board = Board()
    coder = Coder()
    game = Game(game_mode="guesser", computer_player=coder, board=board, secret_code=secret_code)

    guess = [1, 1, 1, 1, 1]
    game.play_round_human_guesser(guess)
    assert not game.is_game_over
    assert board.guesses[-1] == guess
    assert board.feedbacks[-1] == (1, 0)

def test_play_round_human_coder():
    secret_code = [1, 2, 3, 4, 5]
    board = Board()
    guesser = Guesser()
    game = Game(game_mode="coder", computer_player=guesser, board=board, secret_code=secret_code)

    guess = [1, 1, 1, 1, 1]
    game.board.add_guess(guess)
    feedback = (1, 0)
    game.play_round_human_coder(feedback)
    assert board.feedbacks[-1] == feedback

def test_check_game_over():
    secret_code = [1, 2, 3, 4, 5]
    board = Board()
    coder = Coder()
    game = Game(game_mode="guesser", computer_player=coder, board=board, secret_code=secret_code)

    guess = [1, 2, 3, 4, 5]
    game.play_round_human_guesser(guess)
    assert game.is_game_over

def test_save_and_load_game():
    secret_code = [1, 2, 3, 4, 5]
    board = Board()
    coder = Coder()
    game = Game(game_mode="guesser", computer_player=coder, board=board, secret_code=secret_code)

    guess = [1, 2, 3, 4, 5]
    game.play_round_human_guesser(guess)
    game.save_game()

    new_game = Game()
    new_game.load_game()
    assert new_game.game_mode == game.game_mode
    assert new_game.board.guesses == game.board.guesses
    assert new_game.board.feedbacks == game.board.feedbacks
    assert new_game.secret_code == game.secret_code