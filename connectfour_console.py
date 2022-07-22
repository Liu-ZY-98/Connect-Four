import connectfour
import connectfour_common_functions

def user_interface(gamestate: connectfour.GameState) -> None:
        #prints the user interface
        if gamestate.turn == 1:
            print('Red turn')
        elif gamestate.turn == 2:
            print('Yellow turn')
        print('Please enter d followed by a space and the column number to drop a piece, or p to pop a piece')
        connectfour_common_functions.print_board(gamestate)


def main_function() -> None:
    #starts a game and asks the users for their input, ends when a winner is decided 
    gamestate = connectfour.new_game()
    while True:
                    
        user_interface(gamestate)
        move = input()
        new_gamestate = connectfour_common_functions.move(gamestate, move)

        if new_gamestate == False:
            pass
        else:
            gamestate = new_gamestate
        
        try:
            if connectfour.winner(gamestate) == 1:
                connectfour_common_functions.print_board(gamestate)
                print('winner is RED')
                break
            elif connectfour.winner(gamestate) == 2:
                connectfour_common_functions.print_board(gamestate)
                print('winner is YELLOW')
                break
        except AttributeError:
            pass 

if __name__ == '__main__':
    main_function()
    
    












