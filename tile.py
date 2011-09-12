from copy import copy
from random import randint
from random import random

INFINITY = 1000000

class Position:
    def __init__(self, Size = 3):
        self.PuzzleSize = Size
        self.State = []
        for tile in range(1, self.PuzzleSize ** 2):
            self.State.append(tile)
        self.State.append(0)
        self.StateCopy = copy(self.State)
        self.BlankRow, self.BlankCol = self.PuzzleSize - 1, self.PuzzleSize - 1
        self.Solution = ""
        self.EvaluationFunction = self.EvaluateManhattan

    def SetPosition(self, pos):
        if len(pos) == self.PuzzleSize ** 2:
            self.State = copy(pos)
            self.StateCopy = copy(self.State)
            b = self.State.index(0)
            self.BlankRow, self.BlankCol = b / self.PuzzleSize, b % self.PuzzleSize
            self.Solution = ""

    def GetPosition(self):
        return copy(self.State)

    def ResetPosition(self):
        self.SetPosition(self.StateCopy)

    def InvertPosition(self):
        # converts to Korf's representation and back
        for ix, el in enumerate(self.State):
            if el == 0: continue
            self.State[ix] = self.PuzzleSize ** 2 - el
        self.State.reverse()
        self.StateCopy = copy(self.State)
        b = self.State.index(0)
        self.BlankRow, self.BlankCol = b / self.PuzzleSize, b % self.PuzzleSize
        self.Solution = ""

    def ID(self):
        # too long a representation for large puzzles
        # to do: zobrist hashing
        id = ""
        for tile in self.State:
            id = id + str(tile) + ","
        return id[:-1]

    def PrintPosition(self):
        for r in range(self.PuzzleSize):
            for c in range(self.PuzzleSize):
                print self.State[r * self.PuzzleSize + c], "\t",
            print

    def ExecuteSequence(self, sequence, record = False):
        for m in sequence:
            self.Move(m)
        if record: self.Solution += sequence

    def UndoSequence(self, sequence):
        for m in reversed(sequence):
            self.UndoMove(m)        

    def Move(self, (move, cost)):
        b = self.BlankRow * self.PuzzleSize + self.BlankCol
        if move == 'U':
            self.State[b], self.State[b - self.PuzzleSize] = self.State[b - self.PuzzleSize], 0
            self.BlankRow -= 1
        elif move == 'D':
            self.State[b], self.State[b + self.PuzzleSize] = self.State[b + self.PuzzleSize], 0
            self.BlankRow += 1
        elif move == 'L':
            self.State[b], self.State[b - 1] = self.State[b - 1], 0
            self.BlankCol -= 1
        elif move == 'R':
            self.State[b], self.State[b + 1] = self.State[b + 1], 0
            self.BlankCol += 1

    def UndoMove(self, (move, cost)):
        b = self.BlankRow * self.PuzzleSize + self.BlankCol
        if move == 'D':
            self.State[b], self.State[b - self.PuzzleSize] = self.State[b - self.PuzzleSize], 0
            self.BlankRow -= 1
        elif move == 'U':
            self.State[b], self.State[b + self.PuzzleSize] = self.State[b + self.PuzzleSize], 0
            self.BlankRow += 1
        elif move == 'R':
            self.State[b], self.State[b - 1] = self.State[b - 1], 0
            self.BlankCol -= 1
        elif move == 'L':
            self.State[b], self.State[b + 1] = self.State[b + 1], 0
            self.BlankCol += 1
    
    def Solved(self):
        # tiles are checked in inverse order because it's more likely
        # that tiles at the end are not in correct place (thus achieving speed-up)
        for ix in range(len(self.State) - 2, -1, -1):
            if self.State[ix] != ix + 1:
                return False
        return True

    def EvaluateManhattan(self):
        # heuristic is Manhattan score
        e = 0
        for gx in range(self.PuzzleSize ** 2 - 1):
            sx = self.State.index(gx + 1)
            e += abs(gx % self.PuzzleSize - sx % self.PuzzleSize)   # delta X
            e += abs(gx / self.PuzzleSize - sx / self.PuzzleSize)   # delta Y
        return e

    def Evaluate2(self):
        # this evaluation function is not admissible
        return self.EvaluateManhattan() * 2 + randint(0,4)

    def EvaluateGranular(self):
        # this evaluation function is very granular, presents problems for IDA*
        return max(0, self.EvaluateManhattan() - sum([x * 10 ** (-ix-2) for ix, x in enumerate(self.State)]))

    def GenerateMoves(self):
        # all moves have cost equal to 1
        moves = []
        if self.BlankCol != 0: moves.append( ('L', 1) )
        if self.BlankCol != self.PuzzleSize - 1: moves.append( ('R', 1) )
        if self.BlankRow != 0: moves.append( ('U', 1) )
        if self.BlankRow != self.PuzzleSize - 1: moves.append( ('D', 1) )
        return moves

    def Scramble(self, nmoves = 1000):
        # add a random number of moves to stop the odd/even effect
        # (this is also done if the user selects a number of moves that is a factor of 100)
        if nmoves % 100 == 0: nmoves += randint(-25, 25)
        for m in range(nmoves):
            moves = self.GenerateMoves()
            self.Move(moves[randint(0, len(moves) - 1)])
        self.StateCopy = copy(self.State)

    def Evaluate(self):
        return self.EvaluationFunction()

    def SwitchHeuristic(self):
        if self.EvaluationFunction == self.EvaluateManhattan:
            self.EvaluationFunction = self.SolvePuzzle
            print "Switched to pessimistic heuristic."
        else:
            self.EvaluationFunction = self.EvaluateManhattan
            print "Switched to optimistic heuristic."            

    def ExecuteSequenceOld(self, sequence, record = False):
        # for use with SolvePuzzle function (moves have no costs in older version!)
        for m in sequence:
            self.Move( (m, 1) )
        if record: self.Solution += sequence
    
    def UndoSequenceOld(self, sequence):
        # for use with SolvePuzzle function (moves have no costs in older version!)
        for m in reversed(sequence):
            self.UndoMove( (m, 1) )        

    def Minimin(self, depth, alpha):
        # certified
        if self.Solved():
            return -(INFINITY + depth)
        
        Eval = self.Evaluate()
        if depth == 0:
            if Eval < alpha[-1]: alpha.append(Eval)
            return Eval
        else:
            if Eval - depth >= alpha[-1]: return INFINITY

        Best = INFINITY
        for move in self.GenerateMoves():
            self.Move(move)
            Eval = self.Minimin(depth - 1, alpha)
            if Eval < Best: Best = Eval
            self.UndoMove(move)
        return Best + 1

    def BlankToCol(self, c):
        # gets the blank tile to specified column (horizontal alignment)
        while self.BlankCol < c: self.ExecuteSequenceOld("R", True)
        while self.BlankCol > c: self.ExecuteSequenceOld("L", True)

    def BlankToRow(self, r):
        # gets the blank tile to specified row (vertical alignment)
        while self.BlankRow < r: self.ExecuteSequenceOld("D", True)
        while self.BlankRow > r: self.ExecuteSequenceOld("U", True)

    def SolveTileHF(self, dest, t):
        # solves the tile: horizontal alignment first (HF), then moving the tile up
        # tile t to the square indexed dest
        # this routine preserves the partial solution of the first row (row N actually)

        # calculate vertical and horizontal offset of tile t from dest
        # probably can be optimized: (perhaps use slicing to) search only within subpuzzle
        tx = self.State.index(t)
        tc = tx % self.PuzzleSize           # t's column index
        tr = tx / self.PuzzleSize           # t's row index
        dc = dest % self.PuzzleSize - tc    # delta columns dc
        dr = dest / self.PuzzleSize - tr    # delta rows dr

        if dc == 0 and dr == 0: return      # tile t is already at square dest

        # preveri ali je tile t levo ali desno od dest in pripelji blank na ustrezno mesto
        # ce je ze na pravem mestu pripelji blank nad tile t (ce ni tudi vertikalno na vrhu == N)
        if dc == 0:
            # tile t already horizontally aligned (but not vertically), bring blank directly above it
            if self.BlankRow < tr or self.BlankCol > tc:
                # the easiest case, blank is either above or to the right of t
                self.BlankToRow(tr - 1)
                self.BlankToCol(tc)
            elif self.BlankCol == tc:
                # standard exception (blank is in the same column but below, so we have to move around)
                if tc != self.PuzzleSize - 1:
                    # not the rightmost column, blank can go right and around
                    self.ExecuteSequenceOld("R", True)
                    self.BlankToRow(tr - 1)
                    self.ExecuteSequenceOld("L", True)
                else:
                    # rightmost column, blank has to go left and around
                    self.ExecuteSequenceOld("L", True)
                    self.BlankToRow(tr - 1)
                    self.ExecuteSequenceOld("R", True)
            elif dr != -1:
                # here blank is left of t and t is not directly below partially solved top row
                self.BlankToRow(tr - 1)
                self.BlankToCol(tc)
            elif tc == self.PuzzleSize - 1:
                # blank is to the left of t, directly below top row, and t is in the rightmost column
                # blank has to go to the column just to the left of t, then up and one square right
                self.BlankToCol(tc - 1)
                self.BlankToRow(tr - 1)
                self.ExecuteSequenceOld("R", True)
            else:
                # blank is to the left ot t, directly below top row, and t is NOT in the rightmost column
                # blank has to go around t
                # if blank is in the same row as t then we have a case similar to classic "go round" exception
                if self.BlankRow == tr:
                    # similar to classic exception; go one down and around t
                    # since t is directly below top row it is not on lowest row, thus blank can go down
                    self.ExecuteSequenceOld("D", True)
                    self.BlankToCol(tc + 1)
                    self.BlankToRow(tr - 1)
                    self.ExecuteSequenceOld("L", True)
                else:
                    # blank is below t; it can go around without any problems
                    self.BlankToCol(tc + 1)
                    self.BlankToRow(tr - 1)
                    self.ExecuteSequenceOld("L", True)
        else:
            # tile t not horizontally aligned, do it now
            if dc > 0:
                # tile t is to the left of its destination
                # step 1: get blank to t's immediate right
                if self.BlankCol > tc:
                    # blank is to the right of tile t
                    # vertical alignment first to appease special case where blank is in top row
                    self.BlankToRow(tr)
                    self.BlankToCol(tc + 1)
                elif self.BlankRow != tr:
                    # blank is to the left or in the same column as t and not in the same row as t
                    # blank in the top row case is irrelevant here as the partial solution would be to the left of it
                    self.BlankToCol(tc + 1)
                    self.BlankToRow(tr)
                else:
                    # blank is to the left of t and in the same row as t
                    # if it's not the lowest row, go down and around, otherwise up and around
                    if tr != self.PuzzleSize - 1:
                        # not the lowest row; go down and around
                        self.ExecuteSequenceOld("D", True)
                        self.BlankToCol(tc + 1)
                        self.ExecuteSequenceOld("U", True)
                    else:
                        # the lowest row; go up and around
                        self.ExecuteSequenceOld("U", True)
                        self.BlankToCol(tc + 1)
                        self.ExecuteSequenceOld("D", True)
            
                # step 2: pull t right to the correct column (destination column)
                if tr != self.PuzzleSize - 1:
                    # not the lowest row
                    for i in range(dc - 1):
                        self.ExecuteSequenceOld("LDRRU", True)
                else:
                    # lowest row
                    for i in range(dc - 1):
                        self.ExecuteSequenceOld("LURRD", True)
                # self.ExecuteSequenceOld("L", True)  --  due to internal optimization (less calls) merge it with next step

                # step 3: position blank for vertical alignment (blank directly above t) if needed
                if dr == 0:
                    # t already in the correct row, no need for vertical alignment; just do leftover "L" step
                    self.ExecuteSequenceOld("L", True)
                else:
                    # prepare for vertical alignment by bringing blank above t
                    if tr != dest / self.PuzzleSize + 1 or dest % self.PuzzleSize == self.PuzzleSize - 1:
                        # regular case; just go up and right (going left is leftover from step 2 due to optimization)
                        self.ExecuteSequenceOld("LUR", True)
                    else:
                        # special case 4: tile t in second row, blank cannot go up and right w/o compromising top row's partial solution
                        # exception to special case 4: last column, because we are solving penultimate tile in last position!
                        # exception just needs to be detected and nothing special should be done!
                        # again, going left on first move in the sequence is leftover from step 2 due to optimization
                        self.ExecuteSequenceOld("LDRRUUL", True)
        
            else:
                # tile t is to the right of its destination
                # step 1: get blank to t's immediate left
                if self.BlankRow == tr and self.BlankCol > tc:
                    # blank is in the same row as t and to the right of t
                    # if it's not the lowest row, go down and around, otherwise up and around
                    if tr != self.PuzzleSize - 1:
                        # not the lowest row; go down and around
                        self.ExecuteSequenceOld("D", True)
                        self.BlankToCol(tc - 1)
                        self.ExecuteSequenceOld("U", True)
                    else:
                        # the lowest row; go up and around
                        self.ExecuteSequenceOld("U", True)
                        self.BlankToCol(tc - 1)
                        self.ExecuteSequenceOld("D", True)
                else:
                    # no problems here (but the order of aligning matters)
                    # well, technically there is one hidden problem: if t is in top row already,
                    # and blank left from it -- moving blank up and right can compromise the partial solution
                    # by first aligning horizontally and only then vertically this problem is prevented
                    # on the other hand the case of blank on top is not problematic as the solution
                    # would be to the left of blank's destination (immediate left of t)
                    self.BlankToCol(tc - 1)
                    self.BlankToRow(tr)

                # step 2: pull t left to the correct column (destination column)
                if tr != self.PuzzleSize - 1:
                    # not the lowest row
                    for i in range(-dc - 1):
                        self.ExecuteSequenceOld("RDLLU", True)
                else:
                    # lowest row
                    for i in range(-dc - 1):
                        self.ExecuteSequenceOld("RULLD", True)
                # self.ExecuteSequenceOld("R", True)  --  due to internal optimization (less calls) merge it with next step

                # step 3: position blank for vertical alignment (blank directly above t) if needed
                # no special case here (in contrast with special case 4 above)
                if dr == 0:
                    # t already in the correct row, no need for vertical alignment; just do leftover "R" step
                    self.ExecuteSequenceOld("R", True)
                else:
                    # prepare for vertical alignment by bringing blank above t
                    self.ExecuteSequenceOld("RUL", True)

        # t is now horizontally in the right place and, if needed, blank is directly above it
        # now do the vertical alignment if needed
        if dr != 0:
            if self.BlankCol != self.PuzzleSize - 1:       # self.BlankCol instead of tc, because tc is not updated!
                # not the rightmost column
                for i in range(-dr - 1):
                    self.ExecuteSequenceOld("DRUUL", True)
            else:
                # rightmost column
                for i in range(-dr - 1):
                    self.ExecuteSequenceOld("DLUUR", True)
            self.ExecuteSequenceOld("D", True)

    def SolveTileVF(self, dest, t):
        # solves the tile: vertical alignment first (VF), then moving the tile left
        # tile t to the square indexed dest
        # this routine preserves the partial solution of the left column (column N actually)
        # also it assumes that the first row is already solved (neither t or blank are thus there)

        # calculate vertical and horizontal offset of tile t from dest
        # probably can be optimized: (perhaps use slicing to) search only within subpuzzle
        tx = self.State.index(t)
        tc = tx % self.PuzzleSize           # t's column index
        tr = tx / self.PuzzleSize           # t's row index
        dc = dest % self.PuzzleSize - tc    # delta columns dc
        dr = dest / self.PuzzleSize - tr    # delta rows dr

        if dc == 0 and dr == 0: return      # tile t is already at square dest
        
        # preveri ali je tile t visje ali nizje od dest in pripelji blank na ustrezno mesto
        # ce je ze na pravem mestu pripelji blank levo od tile t (ce ni tudi horizontalno cisto na levi == N)
        # blank's position to be in is thus (tc - 1, tr)
        if dr == 0:
            # tile t already vertically aligned (but not horizontally), bring blank directly to the left of it
            if self.BlankCol < tc or self.BlankRow > tr:
                # the easiest case, blank is either to the left of or below t
                self.BlankToCol(tc - 1)
                self.BlankToRow(tr)
            elif self.BlankRow == tr:
                # standard exception (blank is in the same row but to the right, so we have to move around)
                if tr != self.PuzzleSize - 1:
                    # not the lowest row, blank can go down and around
                    self.ExecuteSequenceOld("D", True)
                    self.BlankToCol(tc - 1)
                    self.ExecuteSequenceOld("U", True)
                else:
                    # lowest row, blank has to go up and around
                    self.ExecuteSequenceOld("U", True)
                    self.BlankToCol(tc - 1)
                    self.ExecuteSequenceOld("D", True)
            elif dc != -1:
                # here blank is above t and t is not one column to the right of partially solved leftmost column
                self.BlankToCol(tc - 1)
                self.BlankToRow(tr)
            elif tr == self.PuzzleSize - 1:
                # blank is above t, directly right of leftmost column, and t is in the lowest row
                # blank has to go to the row just above t, then left and one square down
                self.BlankToRow(tr - 1)
                self.BlankToCol(tc - 1)
                self.ExecuteSequenceOld("D", True)
            else:
                # blank is above t, directly right of leftmost column, and t is NOT in the lowest row
                # blank has to go around t
                # if blank is in the same column as t then we have a case similar to classic "go round" exception
                if self.BlankCol == tc:
                    # similar to classic exception; go one right and around t
                    # since t is directly right of leftmost column it is not in rightmost column, thus blank can go right
                    self.ExecuteSequenceOld("R", True)
                    self.BlankToRow(tr + 1)
                    self.BlankToCol(tc - 1)
                    self.ExecuteSequenceOld("U", True)
                else:
                    # blank is to the right of t; it can go around without any problems
                    self.BlankToRow(tr + 1)
                    self.BlankToCol(tc - 1)
                    self.ExecuteSequenceOld("U", True)
        else:
            # tile t not vertically aligned, do it now
            if dr > 0:
                # tile t is above its destination
                # step 1: get blank immediately below t
                if self.BlankRow > tr:
                    # blank is below tile t
                    # horizontal alignment first to appease special case where blank is in leftmost column
                    self.BlankToCol(tc)
                    self.BlankToRow(tr + 1)
                elif self.BlankCol != tc:
                    # blank is above or in the same row as t and not in the same column as t
                    # blank in the leftmost column case is irrelevant here as the partial solution would be above it
                    self.BlankToRow(tr + 1)
                    self.BlankToCol(tc)
                else:
                    # blank is above t and in the same column as t
                    # if it's not the rightmost column, go right and around, otherwise left and around
                    if tc != self.PuzzleSize - 1:
                        # not the rightmost column; go right and around
                        self.ExecuteSequenceOld("R", True)
                        self.BlankToRow(tr + 1)
                        self.ExecuteSequenceOld("L", True)
                    else:
                        # the rightmost column; go left and around
                        self.ExecuteSequenceOld("L", True)
                        self.BlankToRow(tr + 1)
                        self.ExecuteSequenceOld("R", True)

                # step 2: pull t down to the correct row (destination row)
                if tc != self.PuzzleSize - 1:
                    # not the rightmost column
                    for i in range(dr - 1):
                        self.ExecuteSequenceOld("URDDL", True)
                else:
                    # rightmost column
                    for i in range(dr - 1):
                        self.ExecuteSequenceOld("ULDDR", True)
                # self.ExecuteSequenceOld("U", True)  --  due to internal optimization (less calls) merge it with next step

                # step 3: position blank for horizontal alignment (blank directly to the left of t) if needed
                if dc == 0:
                    # t already in the correct column, no need for horizontal alignment; just do leftover "U" step
                    self.ExecuteSequenceOld("U", True)
                else:
                    # prepare for horizontal alignment by bringing blank to the left of t
                    if tc != dest % self.PuzzleSize + 1 or dest / self.PuzzleSize == self.PuzzleSize - 1:
                        # regular case; just go left and down (going up is leftover from step 2 due to optimization)
                        self.ExecuteSequenceOld("ULD", True)
                    else:
                        # special case 5: tile t in second column, blank cannot go left and down w/o compromising leftmost column's partial solution
                        # this is analogous to special case 4 in SolveTileHF
                        # exception to special case 5: last row, because we are solving penultimate tile in last position!
                        # exception just needs to be detected and nothing special should be done!
                        # again, going up on first move in the sequence is leftover from step 2 due to optimization
                        self.ExecuteSequenceOld("URDDLLU", True)
            else:
                # tile t is below its destination
                # step 1: get blank immediately above t
                if self.BlankCol == tc and self.BlankRow > tr:
                    # blank is in the same column as t and below t
                    # if it's not the rightmost column, go right and around, otherwise left and around
                    if tc != self.PuzzleSize - 1:
                        # not the rightmost column; go right and around
                        self.ExecuteSequenceOld("R", True)
                        self.BlankToRow(tr - 1)
                        self.ExecuteSequenceOld("L", True)
                    else:
                        # the rightmost column; go left and around
                        self.ExecuteSequenceOld("L", True)
                        self.BlankToRow(tr - 1)
                        self.ExecuteSequenceOld("R", True)
                else:
                    # no problems here (but the order of aligning matters)
                    # well, technically there is one hidden problem: if t is in leftmost column already,
                    # and blank above it -- moving blank left and down can compromise the partial solution
                    # by first aligning vertically and only then horizontally this problem is prevented
                    # on the other hand the case of blank in leftmost column is not problematic as the solution
                    # would be above blank's destination (immediately above t)
                    self.BlankToRow(tr - 1)
                    self.BlankToCol(tc)

                # step 2: pull t up to the correct row (destination row)
                if tc != self.PuzzleSize - 1:
                    # not the rightmost column
                    for i in range(-dr - 1):
                        self.ExecuteSequenceOld("DRUUL", True)
                else:
                    # rightmost column
                    for i in range(-dr - 1):
                        self.ExecuteSequenceOld("DLUUR", True)
                # self.ExecuteSequenceOld("D", True)  --  due to internal optimization (less calls) merge it with next step

                # step 3: position blank for horizontal alignment (blank directly to the left of t) if needed
                # no special case here (in contrast with special case 5 above)
                if dc == 0:
                    # t already in the correct column, no need for horizontal alignment; just do leftover "D" step
                    self.ExecuteSequenceOld("D", True)
                else:
                    # prepare for horizontal alignment by bringing blank to the left of t
                    self.ExecuteSequenceOld("DLU", True)

        # t is now vertically in the right place and, if needed, blank is directly to the left of it
        # now do the horizontal alignment if needed
        if dc != 0:
            if self.BlankRow != self.PuzzleSize - 1:       # self.BlankRow instead of tr, because tr is not updated!
                # not the lowest row
                for i in range(-dc - 1):
                    self.ExecuteSequenceOld("RDLLU", True)
            else:
                # lowest row
                for i in range(-dc - 1):
                    self.ExecuteSequenceOld("RULLD", True)
            self.ExecuteSequenceOld("R", True)
        
    def SolvePuzzle(self):
        # calculates the human-like solution to the puzzle
        # based on decomposition into smaller puzzle
        # returns the number of moves needed and can serve as a pessimistic heuristic

        # clear solution sequence string
        self.Solution = ""

        # outermost loop: controls decomposition of puzzles
        # [PuzzleSize - 2 .. PuzzleSize - 1] represents the database-solvable 2x2 subpuzzle
        for N in range(self.PuzzleSize - 2):
            # first solve the top row
            for tx in range(N * self.PuzzleSize + N, (N + 1) * self.PuzzleSize - 2):
                self.SolveTileHF(tx, tx + 1)          # horizontal alignment first, then move it up
            tx += 1                                   # to compensate for the difference between C's and Python's for loop

            if self.State[tx] != tx + 1 or self.State[tx + 1] != tx + 2:     # if not by chance already solved
                # special case: last two tiles of top row
                self.SolveTileHF(tx + 1, tx + 1);         # horizontal alignment first, then move it up
                if self.State[tx] == tx + 2:
                    # SPECIAL CASE 1: last tile of the row stuck in penultimate position
                    # get blank to tx + self.PuzzleSize (just below the stuck last tile)
                    self.BlankToCol(self.PuzzleSize - 2)
                    self.BlankToRow(N + 1)
                    self.ExecuteSequenceOld("URDLLURRDLULD", True)
                elif self.State[tx] == 0 and self.State[tx + self.PuzzleSize] == tx + 2:
                    # SPECIAL CASE 1a: blank in penultimate position and last tile of the row just below the blank
                    self.ExecuteSequenceOld("RDLLURRDLULD", True)
                else:
                    # SPECIAL CASE 1b: blank in penultimate position and last tile of the row NOT just below the blank
                    # detect it, go one down, and continue as with regular case
                    # can be suboptimal if last tile is already in its place -- thus check and just proceed if this is so
                    if self.State[tx] == 0 and self.State[tx + 1 + self.PuzzleSize] != tx + 2:
                        self.ExecuteSequenceOld("D", True)

                    # regular case
                    self.SolveTileHF(tx + 1 + self.PuzzleSize, tx + 2)     # horizontal alignment, then move it up
                    # get blank to tx by first horizontally (L,R) aligning it and then moving it up
                    self.BlankToCol(self.PuzzleSize - 2)
                    self.BlankToRow(N)
                    self.ExecuteSequenceOld("RD", True)

            # then solve the leftmost column
            for tx in range((N + 1) * self.PuzzleSize + N, (self.PuzzleSize - 2) * self.PuzzleSize, self.PuzzleSize):
                self.SolveTileVF(tx, tx + 1)        # vertical alignment, then move it left

            # the following is to compensate for the difference between C's and Python's for loop (** this is ugly **)
            # two possibilities: either loop was never executed (set tx) or it was (increase tx)
            # C both initiates tx even when loop never executes and increases tx at the end (to make condition fail)
            if (N + 1) * self.PuzzleSize + N >= (self.PuzzleSize - 2) * self.PuzzleSize:
                # loop never executed; set tx
                tx = (N + 1) * self.PuzzleSize + N
            else:
                # loop executed; just increase tx as C would
                tx += self.PuzzleSize                   

            if self.State[tx] != tx + 1 or self.State[tx + self.PuzzleSize] != tx + self.PuzzleSize + 1:
                # special case: last two tiles of leftmost column
                self.SolveTileVF(tx + self.PuzzleSize, tx + 1)     # vertical alignment, then move it left
                if self.State[tx] == tx + 1 + self.PuzzleSize:
                    # SPECIAL CASE 2: last tile of the column stuck in penultimate position of the column
                    self.BlankToRow(self.PuzzleSize - 2)
                    self.BlankToCol(N + 1)
                    self.ExecuteSequenceOld("LDRURDLULDRULDRRULLDR", True)
                elif self.State[tx] == 0 and self.State[tx + 1] == tx + 1 + self.PuzzleSize:
                    # SPECIAL CASE 2a: blank in the penultimate position of the column and last tile just right of it
                    self.ExecuteSequenceOld("DRURDLULDRULDRRULLDR", True)
                else:
                    # SPECIAL CASE 2b: blank in the penultimate position of the column and last tile NOT just right of it
                    # detect it, go one right, and continue as with regular case
                    # can be suboptimal if last tile is already in its place -- thus check and just proceed if this is so
                    if self.State[tx] == 0 and self.State[tx + self.PuzzleSize + 1] != tx + 1 + self.PuzzleSize:
                        self.ExecuteSequenceOld("R", True)

                    # regular case
                    self.SolveTileVF(tx + self.PuzzleSize + 1, tx + 1 + self.PuzzleSize);  # vertical alignment, then move it left
                    # get blank to tx by first vertically (U,D) aligning it and then moving it left
                    self.BlankToRow(self.PuzzleSize - 2)
                    self.BlankToCol(N)
                    self.ExecuteSequenceOld("DR", True)

        # solve the remaining 2x2 puzzle with database lookup
        # i1..i4 hold indeces of last four tiles so we calculate them only once
        # i1..i4 are also the last three tile values remaining (remember tx and tx+1 relation)
        # lowest remaining tile = i2, middle tile = i2+1, and highest tile = i4

        # calculate the indeces
        i4 = self.PuzzleSize ** 2 - 1        # last tile
        i3 = i4 - 1
        i2 = i4 - self.PuzzleSize
        i1 = i2 - 1                          # first tile of the 2x2 subpuzzle

        # check the twelve possibilities methodically (this is database lookup without hash)
        # computing the hash is no quicker than this
        if self.State[i1] == 0:
            if self.State[i2] == i2: self.ExecuteSequenceOld("RD", True)
            elif self.State[i2] == i2 + 1: self.ExecuteSequenceOld("DR", True)
            elif self.State[i2] == i4: self.ExecuteSequenceOld("DRULDR", True)

        elif self.State[i2] == 0:
            if self.State[i1] == i2: self.ExecuteSequenceOld("D", True)
            elif self.State[i1] == i2 + 1: self.ExecuteSequenceOld("LDR", True)
            elif self.State[i1] == i4: self.ExecuteSequenceOld("DLURD", True)

        elif self.State[i3] == 0:
            if self.State[i4] == i2: self.ExecuteSequenceOld("RULDR", True)
            elif self.State[i4] == i2 + 1: self.ExecuteSequenceOld("URD", True)
            elif self.State[i4] == i4: self.ExecuteSequenceOld("R", True)

        elif self.State[i4] == 0:
            if self.State[i3] == i2: self.ExecuteSequenceOld("ULDR", True)
            elif self.State[i3] == i2 + 1: self.ExecuteSequenceOld("LURD", True)
            # elif self.State[i3] == i4: self.ExecuteSequenceOld("", True)  <-- puzzle already solved

        # revert to starting position by undoing all the moves in solution sequence in inverse order
##        for i in range(1, len(self.Solution) + 1):
##            self.UndoMove(self.Solution[-i])
        self.UndoSequenceOld(self.Solution)

        # return number of moves needed to solve the puzzle
        return len(self.Solution)


   











        
