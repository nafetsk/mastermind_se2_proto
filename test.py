from business_logic import Code, Board, Coder, Guesser, Game

# Mensch spielt als Guesser
board = Board()
secret_code = Code().generate_random()
#print("Secret Code:", secret_code.code)
computer_player = Coder()
game = Game("guesser", computer_player, board, [2,3,4,5,6])
game.display_board()

game.play_round_human_guesser([3,3,4,5,6])
game.display_board()
print("Game over? :", game.is_game_over)
game.play_round_human_guesser([2,3,4,5,6])
game.display_board()
print("Game over? :", game.is_game_over)

# Mensch spielt als Coder

board = Board()
secret_code = Code()
computer_player = Guesser()
game2 = Game("coder", computer_player, board, [2,3,4,5,6])
game2.display_board()

game2.computer_guess()
game2.display_board()
game2.play_round_human_coder([1,2])
game2.display_board()
game2.computer_guess()
game2.display_board()
game2.play_round_human_coder([2,3])
game2.display_board()
game2.save_game()

print("-----GAME 3-----")
game3 = Game()
game3.load_game()
game3.display_board()


guess = "12345"
guess = [int(i) for i in guess]
print(guess)
