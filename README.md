### Overview
This program is a variant of Japanese chess (Shogi) played on a 5x5 board between two players. This is a simplified version of this game. The pieces from the original game have been modified.

## Game Rules

### Objective

The game has two players, **lower** and **UPPER**. Each player aims to capture their opponent's main piece (Drive).

### The Players

The  **lower** player starts on the bottom side of the board, and their pieces are represented by lower-case characters.

The **UPPER** player starts on the top side of the board, and their
pieces are represented by upper-case characters.

The  **lower** player always moves first.

### The Pieces

Each player starts with six pieces, each with different movement capabilities.

The Drive piece, king in the original game, can move one square in any direction:


The Notes piece, rook in the original game, can move any number of squares along rows or columns (orthogonal directions):

The Governance piece, bishop in the original game, can move any number of squares along diagonal directions:


The Shield piece, gold general in the original game, can move one square in any direction except its backward diagonals:

The piece, silver general in the original game, can move one square in any direction except sideways or directly backward:

A Preview piece, pawn in the original game, can move one space forward:


### The Board

The board is a grid of 5 rows by 5 columns. We will call each location on the board a *square*.


This is the grid representation of the starting board state:
```
5 | N| G| R| S| D|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | p|__|__|__|__|
1 | d| s| r| g| n|
    a  b  c  d  e
```

We read the board via a combination of the letters on the x-axis and numbers on the y-axis. For instance, piece *p* is at location *a2* while piece *P* is at location *e4*.

### Capturing

A player can capture an opponent's piece by moving their piece onto the same square as an opponent's piece. The captured piece leaves the board, and can be later dropped onto the board by the player who captured it (more on this under *Drops* below). A player cannot capture their own pieces (this is an illegal move).

### Promotion

A piece may (but does not have to) be **promoted** when it moves into, within, or out of the **promotion zone**.

The promotion zone is the row of the board furthest from each player's starting position:
* For the lower player, the promotion zone is the top row of the board.
* For the UPPER player, the promotion zone is the bottom row of the board.

A piece that has been promoted should gain a plus symbol "+" before its letter showing on the board.

Pieces promote as follows:
* The Drive piece cannot be promoted.
* The Shield piece cannot be promoted.
* The Relay piece (+r/+R) moves the same way as the Shield piece.
* The Promoted Governance (+g/+G) piece can move like the Governance piece or the Drive piece.
* The Promoted Notes piece (+n/+N) can move like the Notes piece or the Drive piece.
* The Promoted Preview piece (+p/+P) moves like the Shield piece.

*Note: The Preview pieces **must** be promoted once they reach the furthest row (otherwise they would not have any legal moves on the next turn).*

### Drops

Pieces that a player has captured can be dropped back onto the board under the capturing player's control. Dropping a piece takes your entire turn.

You cannot drop a piece onto a square that contains another piece.

All dropped pieces must start unpromoted (even if they were captured as promoted pieces and/or are dropped into the promotion zone).

The Preview piece may not be dropped into the promotion zone or onto a square that results in an immediate checkmate.
* Note: other pieces *can* be dropped into the promotion zone or onto a square that results in an immediate checkmate.

Two unpromoted Preview pieces may not lie in the same column when they belong to the same player (e.g. If you already have a Preview piece in the third column, you cannot drop another Preview piece into that column).

### Game End

#### Move Limit

For simplicity, the game ends in a tie once each player has made 200 moves. When a game ends in a tie, output the message "Tie game.  Too many moves." instead of the move prompt.

#### Checkmate

When a player is in a position where their Drive piece could be captured on their opponent's next move, they are in **check**.
That player **must** make a move to get out of check by doing one of the following:
* remove their Drive piece from danger
* capture the piece that threatens their Drive piece
* put another piece between the Drive piece and the piece that threatens it

If a player has no moves that they could make to avoid capture, they are in **checkmate** and lose the game.

When a player wins via checkmate, output the message "<UPPER/lower> player wins.  Checkmate." instead of the move prompt.

#### Illegal Moves

If a player makes a move that is not legal, the game ends immediately and the other player wins. When a player loses via an illegal move, output the message "<UPPER/lower> player wins.  Illegal move." instead of the move prompt.

## Game Interface

Program accepts command line flags to determine which mode to play in:
```
$ python3 boxshogi -i
```
In **interactive mode**, two players enter keyboard commands to play moves against each other.

```
$ python3 boxshogi -f <filePath>
```
In **file mode**, the specified file is read to determine the game state and which moves to make.

#### Move Format

The **lower** player would then enter a move using the following formats:

**move <from> <to> [promote]**
To move a piece, enter `move` followed by the location of the piece to be moved, the location to move to, and (optionally) the word `promote` if the piece should be promoted at the end of the turn.
* `move a2 a3` moves the piece at square a2 to square a3.
* `move a4 a5 promote` moves the piece at square a4 to square a5 and promotes it at the end of the turn.

**drop <piece> <to>**
To drop a piece, enter `drop` followed by the lowercase character representing the piece to drop and the location to drop the piece.  Pieces are always lower-case, no matter which player is performing the drop.
* `drop s c3` drops a captured Shield piece at square c3.
* `drop g a1` drops a captured Governance piece at square a1.

Once a player enters their move, your program should display the move made, update the game state, and proceed to the next turn. For example:
```
lower> move b1 b2
lower player action: move b1 b2
5 | N| G| R| S| D|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | p| s|__|__|__|
1 | d|__| r| g| n|
    a  b  c  d  e

Captures UPPER:
Captures lower:

UPPER> move a5 a2
UPPER player action: move a5 a2
5 |__| G| R| S| D|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | N| s|__|__|__|
1 | d|__| r| g| n|
    a  b  c  d  e

Captures UPPER: P
Captures lower:

lower>
```