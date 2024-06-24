def parseTestCase(path):
    """
    Utility function to help parse test cases.
    :param path: Path to test case file.
    """
    f = open(path)
    line = f.readline()
    initialBoardState = []
    while line != '\n':
        piece, position = line.strip().split(' ')
        initialBoardState.append(dict(piece=piece, position=position))
        line = f.readline()
    line = f.readline().strip()
    upperCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline().strip()
    lowerCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline()
    line = f.readline()
    moves = []
    while line != '':
        moves.append(line.strip())
        line = f.readline()

    return dict(initialPieces=initialBoardState, upperCaptures=upperCaptures, lowerCaptures=lowerCaptures, moves=moves)


def convert_string_pos(stringPos):
    alpha = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    try:
        ind1 = alpha[stringPos[0]]
    except KeyError:
        return None
    try:
        ind2 = int(stringPos[1]) - 1
    except ValueError:
        return None 
    if ind2 not in range(0,5):
        return None
    return (ind1, ind2)
    

def convert_tuple_pos(indices):
    alpha = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}
    letter = alpha.get(indices[0])
    number = str(indices[1] + 1)
    return letter + number


def validate_input(move):
    if len(move) not in (3,4):
        return False
    if len(move)==4:
        if move[0]!='move' and move[3]!= 'promote':
            return False
    if len(move) ==3:
        if move[0] not in ('drop','move'):
            return False
    return True


def convert_moves(safemoves):
    converted_moves = []
    for move in safemoves:
        if not isinstance(move[0], tuple):
            converted_moves.append((move[0], convert_tuple_pos(move[1])))
        else:
            converted_moves.append((convert_tuple_pos(move[0]), convert_tuple_pos(move[1])))
    converted_moves = sorted(converted_moves, key=lambda x: (len(x[0]), x[0]))
        
    return converted_moves


def format_filemode_string(result, upper_captured, lower_captured, playername, enemyname, action, board,checkString='', endProgram = True):
    res = ''
    res += playername + ' player action: ' + action + '\n'
    res += str(board) + '\n\n'
    res += 'Captures UPPER: ' + ' '.join([piece.name for piece in upper_captured]) + '\n'
    res += 'Captures lower: ' + ' '.join([piece.name.lower() for piece in lower_captured]) + '\n\n'
    if checkString!= '':
        res+=checkString
    if result=='Illegal move.':
        res += enemyname + ' player wins.  ' + result
    elif result == 'Checkmate':
        if endProgram==False:
            res += playername + ' player wins.  ' + result + '.'
        else:
            res += enemyname + ' player wins.  ' + result + '.'
    elif result == 'Tie':
            res += 'Tie game.  Too many moves.'
    else:
        res += result + '>'
    return res



    

        
