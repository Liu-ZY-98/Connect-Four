#McCall Pyle 17034279 and Zhiyuan Liu 25105882
import connectfour

def print_board(gamestate: connectfour.GameState ) -> None:
    #prints the game board
    for board_column_number in range(connectfour.BOARD_COLUMNS):
        print(board_column_number +1, end= '  ')
    print()
    for row in range(connectfour.BOARD_ROWS):
        for col in gamestate.board:
            if col[row] == 0:
                print('.', end = '  ')
            elif col[row] == 1:
                print('R', end = '  ')
            else:
                print('Y', end = '  ')       
        print()


def move(gamestate: connectfour.GameState,
         move: str) -> connectfour.GameState or bool:
    #updates the gamestate according to the move, or fails if given wrong input
    try:
            if move[: 2] == 'd ':
                return connectfour.drop(gamestate, int(move[2:]) -1)
            elif move[: 2] == 'p ':
                return connectfour.pop(gamestate, int(move[2:]) -1)
            else:
                print('Invalid move')
                
                return gamestate
          
           
    except connectfour.GameOverError:
        print('Game Over')
    except connectfour.InvalidMoveError:
        print('Invalid Move')
        return gamestate
    except ValueError:
        print('Invalid input')
        
        return False
    except AttributeError:
        print('Invalid input')
        return gamestate







