#McCall Pyle 17034279 and Zhiyuan Liu 25105882
import connectfour_client
import connectfour
import connectfour_common_functions
import socket


def _run_user_interface() -> None:
    #runs the user interface and starts the game 
    try:
        _show_welcome_banner()
        server = _ask_for_server()
        port = _ask_for_port()
        
        connection = connectfour_client.connect(server, port)
        
        if connection != None:
            username = _ask_for_username()
            gamestate = _starting_the_game(connection, username)
            gamestate = _first_move(connection, gamestate)
            _server_dialogue(connection, gamestate)

           
        
    except socket.gaierror:
        print('Server or port does not exist')

    

def _server_connection(
    server: str, port: int) -> connectfour_client.ServerConnection:
    #tries to connect to the connectfour server
        
    try:
        connection = connectfour_client.connect(server, port)
        return connection
    except socket.gaierror:
         print('Server or port does not exist')

def _first_move(connection: connectfour_client.ServerConnection,
               gamestate: connectfour.GameState) -> None:
    #handles the first move of the user
    _user_interface(gamestate)
    new_gamestate = _user_move(gamestate, connection)
    response = connectfour_client.server_response(connection)
    while True:
        
        if response == 'READY':
            _user_interface(gamestate)
            new_gamestate = _user_move(gamestate, connection)
            response = connectfour_client.server_response(connection)
            if new_gamestate == False:
                pass
        
            else:
                if gamestate == new_gamestate:
                    pass
                
                else:
                    gamestate = new_gamestate
                    gamestate = connectfour_common_functions.move(new_gamestate,
                                                          response)
                    return gamestate
        elif response != 'INVALID':
            gamestate = connectfour_common_functions.move(new_gamestate,
                                                          response)
            return gamestate
        elif response == 'INVALID':
            response = connectfour_client.server_response(connection)
            
        

            
        
        
def _server_dialogue(connection: connectfour_client.ServerConnection,
               gamestate: connectfour.GameState) -> None:
    #handles the dialogue between the user and the server
    
     

     while True:
         response = connectfour_client.server_response(connection)
             
         if response == 'READY':
             
             while True:
                _user_interface(gamestate)
                new_gamestate = _user_move(gamestate, connection)

                if new_gamestate == False:
                    
                    pass
                    
                else:
                    if gamestate == new_gamestate:
                        pass
               
                    else:
                        gamestate = new_gamestate
                       
                        break      
         elif response.startswith('WINNER'):
             winner(gamestate, response)
             connectfour_client.close_connection(connection)
             break

         elif response == 'INVALID':
             
             pass
         else:
             if connectfour_client.invalid_response(connection, response) == True:
                 break
             
             gamestate = connectfour_common_functions.move(gamestate, response)


    
             
    

def _starting_the_game(connection: connectfour_client.ServerConnection,
                       username: str) -> connectfour.GameState:
    #starts the game
    connectfour_client.hello(connection, username)
    return connectfour_client.start_game(connection)
 

def _ask_for_server() -> str: 
    #asks user for the server name, continues to ask if nothing is entered
    while True:
        server = input('Server: ').strip()

        if len(server) > 0:
            return server
        else:
            print('The server is blank, please input a server')


def _ask_for_port() -> int:
    #asks user for the port number, continues to ask if response is not a number
    while True: 
        port = input('Port: ').strip()
        
        try:
            port = int(port)
            
            if port < 0 or port > 65535:
                print('Port must be between 0 and 65535')
            else:
                return port
        except ValueError:
            print('Port must be an integer')
            
        

def _ask_for_username() -> str:
    #asks user for the username
    while True:
        username = input('Username: ').strip()

        if len(username) > 0:
            return username
        else:
            print('The username is blank, please enter a username')

def _show_welcome_banner() -> None:
    #shows a welcome banner to the user
    print('Welcome to Connect four')
    print()
    print('Please enter the server name')
    print()

def _user_interface(gamestate: connectfour.GameState) -> None:
    #prints red turn and the controls for the user

    print('Red turn')
    print('Please enter d followed by a space and the column number to drop a piece')
    print('or p to pop a piece')
        
        
    connectfour_common_functions.print_board(gamestate)

def _user_move(gamestate: connectfour.GameState, connection:
               connectfour_client.ServerConnection) -> connectfour.GameState:
    #asks for user input and sends it to the server, and returns the gamestate
   
        move = input()
        user_move = connectfour_common_functions.move(gamestate, move)
        
        connectfour_client.player_move(connection, move)
        
        return user_move
        
def winner(gamestate: connectfour.GameState, winner: str) -> None:
    #checks to see a winner has been determined
    if winner.endswith('YELLOW'):
        connectfour_common_functions.print_board(gamestate)
        print('The winner is Yellow!')
    elif winner.ednswith('RED'):
        connectfour_common_functions.print_board(gamestate)
        print('The winner is Red!')
        

    
if __name__ == '__main__':
    _run_user_interface()






