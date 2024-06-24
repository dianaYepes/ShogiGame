import sys
from utils import parseTestCase, validate_input, convert_string_pos, format_filemode_string, convert_moves
from board import Board
from player import Player

def main():

##simple helper function for file mode for checking if pieces are in check.  It returns a tuple depeding on check or checkmate
    def check_helper(playerTurn,playerOpposite,board):
        check = playerTurn.is_in_check(board,playerOpposite)
        safeMoves = []
        if check:
            safeMoves = playerTurn.get_safe_moves(game_board,playerOpposite)
            if len(safeMoves) == 0:
                return 'Checkmate'
            else:
                return safeMoves
        else:
            return None
            

######################################################## file mode
    if sys.argv[1] == '-f':
        data = parseTestCase(sys.argv[2])
        initial_pieces, moves = data['initialPieces'], data['moves']
        upper_captures, lower_captures = data['upperCaptures'], data['lowerCaptures']
        game_board = Board()
        upp = Player('UPPER')
        low = Player('lower')
        for i in initial_pieces:
            piece = i['piece']
            pos = convert_string_pos(i['position'])
            if piece.islower():
                created_piece= low.create_piece(piece,pos)
                low.add_piece(created_piece,created_piece.name.lower() )
                game_board._board[pos[0]][pos[1]] = created_piece.name.lower()
            else:
                created_piece = upp.create_piece(piece, pos)
                upp.add_piece(created_piece, created_piece.name)
                game_board._board[pos[0]][pos[1]] = created_piece.name
        for i in upper_captures:
            upp.add_captured(upp.create_piece(i,(0,0)))
        for i in lower_captures:
            low.add_captured(low.create_piece(i,(0,0)))

            
        playerTurn = low
        playerOpposite = upp
        programEnd = False
        for i in moves:
            if playerTurn.numMoves<200 or playerOpposite.numMoves<200:
                in_check = check_helper(playerTurn,playerOpposite,game_board)
                safeMoves = []
                if in_check != None:
                    if in_check =='Checkmate':
                        string_board = game_board._stringifyBoard()
                        res = format_filemode_string(in_check,upp.captured,low.captured,playerTurn.name,playerOpposite.name,i,string_board)
                        print(res)
                        programEnd = True
                        break
                    else:
                        safeMoves = in_check
                if playerTurn.perform_action(i.split(' '),game_board,playerOpposite,safeMoves):
                    playerTurn.numMoves += 1
                    playerTurn = upp if playerTurn.name == 'lower' else low
                    playerOpposite = upp if playerOpposite.name == 'lower' else low
                else:
                    string_board = game_board._stringifyBoard()
                    res = format_filemode_string('Illegal move.',upp.captured,low.captured,playerTurn.name,playerOpposite.name,i,string_board)
                    print(res)
                    programEnd = True
                    break
        string_board = game_board._stringifyBoard()
        if not programEnd:
            in_check = check_helper(playerTurn,playerOpposite,game_board)
            result = playerTurn.name
            check_string = ''
            if in_check != None:
                if in_check == 'Checkmate':
                    result = in_check
                else:
                    safe_moves = convert_moves(in_check)
                    check_string = f"{playerTurn.name} player is in check!\nAvailable moves:\n"
                    for move in safe_moves:
                        if len(move[0])==2:
                            check_string += f"move {move[0]} {move[1]}\n"
                        else:
                            check_string += f"drop {move[0]} {move[1]}\n"
            elif playerOpposite.numMoves>=200 and playerOpposite.numMoves >=200:
                result = 'Tie'
            res = format_filemode_string(result, upp.captured, low.captured, playerOpposite.name, playerTurn.name , i, string_board, check_string, programEnd)
            print(res)
        

######################################################## interactive mode
    elif sys.argv[1] == '-i':
        game = Board(sys.argv[1])
        upper = Player('UPPER', sys.argv[1])
        lower = Player('lower', sys.argv[1])
        playerTurn = lower
        playerOpposite = upper
        invalidOrCheckmate = False

        while upper.numMoves<200:
            print(game._stringifyBoard()+'\n')
            print('Captures UPPER:'+ ' '.join([piece.name for piece in upper.captured]))
            print('Captures lower:'+ ' '.join([piece.name.lower() for piece in lower.captured])+'\n')
            check = playerTurn.is_in_check(game,playerOpposite)
            safeMoves = []
            if check:
                safeMoves = playerTurn.get_safe_moves(game,playerOpposite)
                if len(safeMoves) == 0:
                    print(playerOpposite.name, ' player wins. Checkmate')
                    invalidOrCheckmate = True
                    break
                else:
                    converted_moves = convert_moves(safeMoves)
                    print(playerTurn.name +' player is in check!\nAvailable moves:')
                    for move in converted_moves:
                        if len(move[0])==2:
                            print('move ' +move[0]+ ' ' + move[1])
                        else:
                            print('drop ' +move[0]+ ' ' + move[1])  
            playerMove = input(playerTurn.name + '>').split(' ')
            if validate_input(playerMove):
                if playerTurn.perform_action(playerMove,game,playerOpposite,safeMoves):
                    playerTurn.numMoves += 1 ## if valid end turn and increase numMoves count
                    playerTurn = upper if playerTurn.name == 'lower' else lower
                    playerOpposite = upper if playerOpposite.name == 'lower' else lower
                else:
                    print(playerOpposite.name,' player wins. Illegal move.')
                    invalidOrCheckmate = True
                    break
            else:
                print(playerOpposite.name,' player wins. Illegal move.')
                invalidOrCheckmate = True
                break
        if not invalidOrCheckmate:
            print('Tie game. Too many moves.')
            

if __name__ == "__main__":
    main()