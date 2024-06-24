class Piece(object):
    """
    Class that represents a Shogi piece
    Here all pieces borrow methods from Piece parent and all have generate_moves method
    """

    def __init__(self,pos):
        self.pos = pos
    
    def is_within_board(self, pos):
        # Check if the position is within bounds of board
        x, y = pos
        return 0 <= x < 5 and 0 <= y < 5
    
    def invert_pos_upper(self,posToInvert):
        curr_y = self.pos[1]
        diff = curr_y - posToInvert[1]
        inverted_y = curr_y + diff
        return(posToInvert[0],inverted_y)
    
    def is_valid_move(self, newpos, board, incheck):
        curr_x, curr_y = self.pos
        new_x, new_y = newpos
        if len(incheck)!=0:
            if (self.pos,newpos) not in incheck:
                return(False,None)
            else:
                return (True, board._board[new_x][new_y])
        # Check if the new position is within the bounds of the board
        if not self.is_within_board(newpos):
            return (False, None)
        # Check if there's any piece of your own on the new position
        if board._board[new_x][new_y] != '__' and board._board[new_x][new_y].isupper() == board._board[curr_x][curr_y].isupper():
            return (False, None)
        return(True,board._board[new_x][new_y])
    


class Drive(Piece):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = 'D'       
    
    def generate_moves(self, board, moves, safeMoves, pos = None):
        our_pos = pos if pos is not None else self.pos
        curr_x, curr_y = pos if pos is not None else self.pos
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0, 0):
                    new_x, new_y = curr_x + x, curr_y + y
                    valid = self.is_valid_move((new_x,new_y), board, safeMoves)
                    if valid[0]:
                        moves.append((our_pos,(new_x,new_y)))

    

class Notes(Piece):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = 'N'

    def generate_moves(self, board, moves, safeMoves, pos = None):
        our_pos = pos if pos is not None else self.pos
        curr_x, curr_y = pos if pos is not None else self.pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Up, Down
        for dx, dy in directions:
            new_x, new_y = curr_x + dx, curr_y + dy
            while self.is_within_board((new_x, new_y)):
                valid = self.is_valid_move((new_x, new_y), board, safeMoves)
                if valid[0]:  # If the move is valid and the position is empty
                    moves.append((our_pos,(new_x, new_y)))
                    if valid[1] != '__':
                        break
                    new_x += dx
                    new_y += dy
                else:
                    break


class Governance(Piece):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = 'G'
        
    def generate_moves(self, board, moves, safeMoves, pos = None):
        our_pos = pos if pos is not None else self.pos
        curr_x, curr_y = pos if pos is not None else self.pos
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0, 0) and abs(x) == abs(y):
                    new_x, new_y = curr_x + x, curr_y + y
                    while self.is_within_board((new_x, new_y)):
                        valid = self.is_valid_move((new_x, new_y), board, safeMoves)
                        if valid[0]:
                            moves.append((our_pos,(new_x, new_y)))
                            if valid[1] != '__':
                                break
                            new_x += x
                            new_y += y
                            
                        else:
                            break
        

class Shield(Piece):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = 'S'

    def generate_moves(self, board, moves, safeMoves, pos = None):
        our_pos = pos if pos is not None else self.pos
        curr_x, curr_y = pos if pos is not None else self.pos
        upper = False
        if board._board[curr_x][curr_y].strip().isupper():
            upper = True
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0, 0) and (x, y) not in [(1, -1), (-1, -1)]:
                    new_x, new_y = curr_x + x, curr_y + y
                    if upper:
                        new_x,new_y = self.invert_pos_upper((new_x,new_y))
                    valid = self.is_valid_move((new_x, new_y), board, safeMoves)
                    if valid[0]:
                        moves.append((our_pos,(new_x, new_y)))

class Relay(Piece):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = 'R'

    def generate_moves(self, board, moves,safeMoves, pos = None):
        our_pos = pos if pos is not None else self.pos
        curr_x, curr_y = pos if pos is not None else self.pos
        upper = False
        if board._board[self.pos[0]][self.pos[1]].strip().isupper():
            upper = True
        for x in range(-1, 2):
            for y in range(-1, 2):
                # Skip squares next to and directly behind the current position
                if x == 0 and y == 0 or (x == 0 and y == -1) or (y == 0):
                    continue
                new_x, new_y = curr_x + x, curr_y + y
                if upper:
                    new_x,new_y = self.invert_pos_upper((new_x,new_y))
                valid = self.is_valid_move((new_x,new_y), board, safeMoves)
                if valid[0]:
                    moves.append((our_pos,(new_x,new_y)))

        
class Preview(Piece):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = 'P'
        
    def generate_moves(self,board,moves,safeMoves, pos = None):
        our_pos = pos if pos is not None else self.pos
        curr_x, curr_y = pos if pos is not None else self.pos
        newpos = (curr_x,curr_y+1)
        if board._board[self.pos[0]][self.pos[1]].strip().isupper():
            newpos = self.invert_pos_upper(newpos)
        valid = self.is_valid_move(newpos,board,safeMoves)
        if valid[0]:
            moves.append((our_pos,newpos))



class PromotedGovernance(Governance,Drive):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = '+G'

    def generate_moves(self, board, moves, safeMove, pos = None):
        our_pos = pos if pos is not None else self.pos
        # Call generate_moves method of Drive and Governance
        super().generate_moves(board, moves, safeMove, our_pos)  
        super(Governance, self).generate_moves(board, moves, safeMove,our_pos)


    
class PromotedNotes(Notes,Drive):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = '+N'
        
    def generate_moves(self, board, moves, safeMoves, pos =None):
        our_pos = pos if pos is not None else self.pos
        # Call generate_moves method of Drive and Notes
        super().generate_moves(board, moves, safeMoves,our_pos)  
        super(Notes, self).generate_moves(board, moves, safeMoves,our_pos)


class PromotedRelay(Shield):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = '+R'

    def generate_moves(self, board, moves, safeMoves, pos = None):
        our_pos = pos if pos is not None else self.pos
        # Call generate_moves method of Shield
        super().generate_moves(board, moves, safeMoves,our_pos)  


class PromotedPreview(Shield):

    def __init__(self, pos):
        super().__init__(pos)
        self.name = '+P'

    def generate_moves(self, board, moves, safeMoves, pos = None):
        our_pos = pos if pos is not None else self.pos
        # Call generate_moves method of Shield
        super().generate_moves(board, moves, safeMoves, our_pos)

    