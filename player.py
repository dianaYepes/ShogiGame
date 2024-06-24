from piece import Notes, Governance, Relay, Shield, Drive, Preview, PromotedGovernance, PromotedNotes, PromotedPreview, PromotedRelay
from board import Board
from utils import convert_string_pos
class Player:
    """
    Class that represents the player in Shogi
    """
    #for simplicity, we make the piece keys uppercase since the piece.names are also in uppercase
    #mappings for string pieces to objects
    mappings = {'N': Notes,
                'G': Governance,
                'S': Shield,
                'D': Drive,
                'R': Relay,
                'P': Preview,
                '+N': PromotedNotes,
                '+R': PromotedRelay,
                '+P': PromotedPreview,
                '+G': PromotedGovernance
                }
    
    def __init__(self, role, gamemode='file'):
        self.name = role
        self.pieces = {}
        self.captured = []
        self.numMoves = 0

        #we initialize player pieces in interactive mode
        if role == 'UPPER' and gamemode=='-i':
            self.pieces = {
                'N':[Notes((0,4))],
                'G':[Governance((1,4))],
                'R':[Relay((2,4))],
                'S':[Shield((3,4))],
                'D':[Drive((4,4))],
                'P':[Preview((4,3))]
            }

        elif role=='lower' and gamemode=='-i':
            self.pieces = {
            'n': [Notes((4, 0))],
            'g': [Governance((3, 0))],
            'r': [Relay((2, 0))],
            's': [Shield((1, 0))],
            'd': [Drive((0, 0))],
            'p': [Preview((0,1))]
        }

    #create piece and return
    def create_piece(self, piecename, pos):
        piece = self.mappings.get(piecename.upper())(pos)
        return piece

    #Add piece to player collection
    def add_piece(self, piece, key):
        if key not in self.pieces:
            self.pieces[key] = []
        self.pieces[key].append(piece)
    
    #Get peice from your collection using position
    def get_piece(self,key,pos):
        for i in range(len(self.pieces[key])):
            if self.pieces[key][i].pos == pos:
                return self.pieces[key][i]

    #Remove piece from collection
    def remove_piece(self, key, pos):
        key = key.strip()
        for i in range(len(self.pieces[key])):
            if self.pieces[key][i].pos == pos:
                return self.pieces[key].pop(i)

    #Add a piece to your captured collection which you can later drop
    def add_captured(self, piece):
        if len(piece.name)==2:
            piece = self.create_piece(piece.name[1],(0,0))
        self.captured.append(piece)





    #Check if you are in check by generating enemy moves
    def is_in_check(self,board,enemy):
        #get Drive position
        boxdPos = self.pieces.get('D')[0].pos if self.name == 'UPPER' else self.pieces.get('d')[0].pos
        enemyMoves = []
        #generate enemy moves and see if Drive position is included
        for piece_key in enemy.pieces:
            for piece in enemy.pieces[piece_key]:
                piece.generate_moves(board,enemyMoves,[])
        return any(boxdPos == pair[1] for pair in enemyMoves)

    #simulate a move on the board for checking if piece remains in check after move
    def simulate_move(self,letter,board,posto,posfrom,enemy):
        temp = board._board[posto[0]][posto[1]]
        boardPiece = board._board[posfrom[0]][posfrom[1]]
        board.updateBoard(posto, letter)
        board.updateBoard(posfrom, '__')
        res = self.is_in_check(board,enemy)
        board.updateBoard(posto,temp)
        board.updateBoard(posfrom, boardPiece)
        return res

    #get a list of valid drops to get out of check
    def get_safe_drops(self,board,enemy):
        safe_drops = []
        piece_drops = []
        standIn = 'R' if self.name == 'UPPER' else 'r'
        for i in range(len(board._board)):
            for j in range(len(board._board[i])):
                if board._board[i][j]=='__':
                    board.updateBoard((i,j),standIn)
                    check = self.is_in_check(board,enemy)
                    if not check:
                        safe_drops.append((i,j))
                    board.updateBoard((i,j),'__')
        for i in self.captured:
            for j in safe_drops:
                if i.name == 'P':
                    p = 'P' if self.name=='UPPER' else 'p'
                    prom_zone = 0 if self.name=='UPPER' else 4
                    if j[1] != prom_zone:
                        if p in self.pieces and self.pieces[p]:
                            for i in self.pieces[p]:
                                if i.pos[0] != j[0]:
                                    piece_drops.append((i.name.lower(),j))
                        else:
                            piece_drops.append((i.name.lower(),j))
                else:
                    piece_drops.append((i.name.lower(),j))
        return piece_drops


    #generate safe moves if in check
    def get_safe_moves(self,board,enemy):
        drive = self.pieces.get('D')[0] if self.name == 'UPPER' else self.pieces.get('d')[0]
        allmoves = []
        safemoves = []
        #generate list of possible moves for own pieces
        for piece_key in self.pieces:
            for piece in self.pieces[piece_key]:
                piece.generate_moves(board,allmoves,[])
        #for those moves, simulate each move and check if we are still in check
        for i in allmoves:
            #for all pieces we can simulate by putting a stand in on the board since the piece need only be in the way, unless its Drive
            #for Drive we need to actually change position since is_in_check function uses it to verify if still in check
            isDrive = False
            if i[0] == drive.pos:
                drive.pos = i[1]
                isDrive = True
            #stand in to update board since we only need a piece to be in the way
            standIn = 'R' if self.name == 'UPPER' else 'r'
            #verify if we are still in check with updated board, and append safe moves list
            check = self.simulate_move(standIn,board,i[1],i[0],enemy)
            if not check:
                safemoves.append(i)
            if isDrive:
                drive.pos = i[0]
        #generate safe drops
        drops = self.get_safe_drops(board, enemy)
        for i in drops:
            safemoves.append(i)
        return safemoves    






    #if preview is being moved to promotion zone it MUST be promoted, otherwise illegal move
    def check_promotion_preview(self,piece,posTo,action):
        y = 0 if self.name == 'UPPER' else 4
        if piece.name == 'P' and posTo[1] == y:
            if len(action)!=4:
                return False
        return True
    
    #method to create promoted piece.  We cannot use regular mappings as we are transforming a normal piece
    def create_piece_promote(self,pieceName,new):
        #create promoted version of original pieces
        if pieceName == 'P':
                new = PromotedPreview((10,10))
                key = new.name if self.name == 'UPPER' else new.name.lower()
                self.add_piece(new,key)
        elif pieceName == 'R':
                new = PromotedRelay((10,10))
                key = new.name if self.name == 'UPPER' else new.name.lower()
                self.add_piece(new,key)
        elif pieceName == 'N':
                new = PromotedNotes((10,10))
                key = new.name if self.name == 'UPPER' else new.name.lower()
                self.add_piece(new,key)
        elif pieceName == 'G':
                new = PromotedGovernance((10,10))
                key = new.name if self.name == 'UPPER' else new.name.lower()
                self.add_piece(new,key)
        return new
        
    #validate piece can be promoted and promote piece
    def promoting_piece(self,piece,posTo,posFrom,board):
        new = None
        #check that in piece is in promotion zone or leaving zone
        y = 0 if self.name == 'UPPER' else 4
        if posTo[1]==y or posFrom[1]==y:
           #cannot promote drive or shield
           if not isinstance(piece, (Drive, Shield)):
                new = True
                self.remove_piece(board._board[posFrom[0]][posFrom[1]],posFrom)
                new = self.create_piece_promote(piece.name,new)
        return new

    #Verify move is valid and perform your move
    def perform_action_move(self,action,board,enemy,safeMoves):
        pos_from = convert_string_pos(action[1])
        pos_to = convert_string_pos(action[2])
        #check that given positions are valid
        if pos_from is None or pos_to is None:
            return False
        #verify that piece being moved is owned by player and exists
        try:
            letter = board._board[pos_from[0]][pos_from[1]].strip()
            piece = self.get_piece(letter,pos_from)
        except Exception:
            return False
        
        #verify piece is being moved to a valid position using generate moves
        validate = []
        piece.generate_moves(board, validate, safeMoves)
        if (pos_from, pos_to) not in validate:
                return False
        #verify we dont move into check
        if piece.name == 'D' or piece.name == 'd':
            piece.pos = pos_to
        check = self.simulate_move(letter,board,pos_to,pos_from,enemy)
        if check:
            print('fail')
            return False
        
        #if we are promoting, call function to generate new promoted piece, and check if we need to force preview promote
        if len(action) == 4 or not self.check_promotion_preview(piece, pos_to, action):
            piece = self.promoting_piece(piece, pos_to, pos_from, board)
            if piece is None:
                return False
        #check if we are moving to a position where enemy piece is at, and capture it
        if board._board[pos_to[0]][pos_to[1]] != '__':
            captured = enemy.remove_piece(board._board[pos_to[0]][pos_to[1]],pos_to)
            self.add_captured(captured)
        #update the piece position and board
        piece.pos = pos_to
        board._board[pos_to[0]][pos_to[1]] = piece.name if self.name == 'UPPER' else piece.name.lower()
        board.updateBoard(pos_from, '__')
        return True






    #validate Preview piece constraints if it is being dropped
    def drop_preview_validation(self, piece, posTo, board, enemy):
        #check that preview piece is not beng dropped in promotion zone
        prom_zone = 0 if self.name=='UPPER' else 4
        if posTo[1] == prom_zone:
            return False
        #check you dont drop preview in column where other preview you have exists
        for i in self.pieces:
            if i == 'P' or i=='p':
                for j in self.pieces[i]:
                    checkPos = j.pos
                    if checkPos[0] == posTo[0]:
                        return False
        #check that dropping preview piece does not result in immediate enemy checkmate
        temp = board._board[posTo[0]][posTo[1]]
        p = 'P' if self.name=='UPPER' else 'p'
        tempPiece = self.create_piece('P',posTo)
        self.add_piece(tempPiece,p)
        board.updateBoard(posTo, p)
        if enemy.is_in_check(board,self):
            safeMoves = enemy.get_safe_moves(board,self)
            board.updateBoard(posTo, temp)
            if len(safeMoves) == 0:
                return False
        self.remove_piece(p,posTo)
        board.updateBoard(posTo, temp)
        return True

    #Perform your drop
    def perform_action_drop(self,action,board,enemy,safeMoves):
        #verify drop piece is lowercase/valid
        if action[1] not in ('n','s','g','r','p','+p','+r','+n','+g'):
            return False
        #verify drop location is in board bounds
        dropAt = convert_string_pos(action[2])
        if dropAt == None:
            return False
        #verify square to drop piece in is empty:
        if board._board[dropAt[0]][dropAt[1]] != '__':
            return False
        #verify the piece actually exists in your captured collection
        exists = False
        ind = 0
        for i in range(len(self.captured)):
            if self.captured[i].name.lower() == action[1]:
                ind = i
                exists = True
        if not exists:
            return False
        piece = self.captured[ind]
        #validate Preview constraints if the dropped piece is a Preview Piece
        if piece.name == 'P':
            if not self.drop_preview_validation(piece,dropAt,board,enemy):
                return False
        #drop and update board
        piece = self.captured.pop(ind)
        piece.pos = dropAt
        key = piece.name if self.name == 'UPPER' else piece.name.lower()
        self.add_piece(piece,key)
        board._board[dropAt[0]][dropAt[1]] = key
        return True





    #Call corresponding action move
    def perform_action(self,action,board,enemy,safeMoves):
        if action[0] == 'move':
            return(self.perform_action_move(action,board,enemy,safeMoves))
        else:
            return(self.perform_action_drop(action,board,enemy,safeMoves))



                    







        

