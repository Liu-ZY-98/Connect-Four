#McCall Pyle 17034279 and Zhiyuan Liu 25105882
import socket
import connectfour
import connectfour_common_functions
from collections import namedtuple


ServerConnection = namedtuple(
    'ServerConnection',
    ['socket', 'input', 'output'])

class ConnectionProtocolError(Exception):
    pass

_SHOW_DEBUG_TRACE = False

WELCOME = 1


def connect(host: str, port: int) -> ServerConnection:
    '''
    tries to connect to the server
    fails if it cannot connect in time or connect refuses
    '''
    
    try:
        connectfour_socket = socket.socket()
        connectfour_socket.connect((host, port))

        connectfour_input = connectfour_socket.makefile('r')
        connectfour_output = connectfour_socket.makefile('w')

        return ServerConnection(
            socket = connectfour_socket,
            input = connectfour_input,
            output = connectfour_output)
    except TimeoutError:
        print('Unable to connect to server in time')
        return None
        
            
    except ConnectionRefusedError:
        print('Server refused connection')
        return None
        
            




def hello(connection: ServerConnection, username: str) -> None:
    #sends the intial hello to the server
    _write_line(connection, 'I32CFSP_HELLO ' + username)

    response = _read_line(connection)

    if response.startswith('WELCOME'):
        print('Welcome ' + username)
    else:
        raise ConnectionProtocolError

def start_game(connection: ServerConnection) -> connectfour.GameState:
    #tells the server to start the game
    _write_line(connection, 'AI_GAME')

    response = _read_line(connection)

    if response == 'READY':
        return connectfour.new_game()
    else:
        raise ConnectionProtocolError

def player_move(connection: ServerConnection, move: str,) -> None:
    #sends the player move to the server
    try:
        if move[:2] == 'd ' and type(int(move[2:])) == int:
            _write_line(connection,'DROP ' + move[2:])
            
        elif move[:2] == 'p ' and type(int(move[2:])) == int:
            _write_line(connection,'POP ' + move[2:])
    except ValueError:
        _write_line(connection,'DROP 43')

def server_response(connection: ServerConnection) -> str:
    #returns the server move if it is a move, or its response if it is not a move
    response = _read_line(connection)

    if response == 'OKAY':
        move = _read_line(connection)
        server_move = _server_move(connection, move)
        return server_move
    elif response == 'INVALID':
        return response
    elif response == 'READY':
        return response
    elif response.startswith('WINNER'):
        return response
    else:
        raise ConnectionProtocolError

def _server_move(connection: ServerConnection,
                 move: str) -> connectfour.GameState:
    #converts the server move to the same form as the users move
    if move[:4] == 'DROP':
        return 'd' + move[4:]
    elif move[:3] == 'POP':
        return 'p' + move[3:]
              
def _read_line(connection: ServerConnection) -> str:
    #reads a line from the server
    line = connection.input.readline()[:-1]

    if _SHOW_DEBUG_TRACE:
        print('RCVD: ' + line)

    return line

def _write_line(connection: ServerConnection, line: str) -> None:
    #writes a line to the server
    connection.output.write(line + '\r\n')
    connection.output.flush()

    if _SHOW_DEBUG_TRACE:
        print('SENT: ' + line)

def close_connection(connection: ServerConnection) -> None:
    #closes the connection with the server
    connection.input.close()
    connection.output.close()
    connection.socket.close()

def invalid_response(connection: ServerConnection, response: str) -> bool:
    #ends the connection if the server sends something it should not
    if response[: 2] != 'd ' and  response[: 2] != 'p ' :
        print(response)
        close_connection(connection)
        return True
                 
    else:
         try:
            if int(response[-1]) > 7 or int(response[-1]) < 0:
                close_conection(connection)
                return True
                
         except ValueError:
             close_conection(connection)
             return True





