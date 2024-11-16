# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:42:39 2024

@author: robot
"""
import os
import copy

class GameBoard:
    rows = 8
    cols = 8
    row_sums = []
    col_sums = []
    goal_count = {}
    ships_made = {}
    tiles = []
    
    
    def __init__(self, row_sums, col_sums, goal_count = {}, filled=[], blanked=[]):
        self.rows = len(col_sums)
        self.cols = len(row_sums)
        self.row_sums = row_sums
        self.col_sums = col_sums
        self.goal_count = goal_count
        self.ships_made = {}
        for length in goal_count.keys():
            self.ships_made[length] = 0
        
        self.tiles = [[-1 for i in range(self.cols)] for j in range(self.rows)]
        for pt in filled:
            self.tiles[pt[0]][pt[1]] = 1
        for pt in blanked:
            self.tiles[pt[0]][pt[1]] = 0
        
        
    def __str__(self):
       return os.linesep.join([' '.join([' ']+[str(x) for x in self.col_sums])] +
                              [' '.join([str(self.row_sums[k])] + ["{0}".format('*' if t == 1 else ('-' if t == 0 else ' ')) for t in row]) for k,row in enumerate(self.tiles)] + [str(self.goal_count), str(self.ships_made)]
           )

    # Returns true if any new tiles filled in
    def fillLines(self):
        # Go through the row and col sums and fill in any that are done
        changed = False
        
        # check rows against row goals
        for rowk,row in enumerate(self.tiles):
            # Check if any are empty
            empty = len([x for x in row if x == -1])
            #blanked = len([x for x in row if x == 0])
            filled = len([x for x in row if x == 1])
            
            if filled > self.row_sums[rowk]:
                raise(Exception("Too many filled tiles in row "+str(rowk)))
            
            # check if this row is completed done already
            if empty == 0:
                continue
            
            # check if we have enough filled tiles in this row
            if filled == self.row_sums[rowk]:
                # blank the rest of the tiles
                for colj in range(self.cols):
                    if row[colj] == -1:
                        row[colj] = 0
                        changed = True
                continue
            
            # check if there are exactly the right number of empties to fill in
            if empty + filled == self.row_sums[rowk]:
                # fill the rest of the tiles
                for colj in range(self.cols):
                    if row[colj] == -1:
                        row[colj] = 1
                        changed = True
                continue
            
        
        # check cols against col goals
        for colj in range(self.cols):
            # Check if any are empty
            empty = len([row[colj] for row in self.tiles if row[colj] == -1])
            #blanked = len([row[colj] for row in self.tiles if row[colj] == 0])
            filled = len([row[colj] for row in self.tiles if row[colj] == 1])
            
            if filled > self.col_sums[colj]:
                raise(Exception("Too many filled tiles in column "+str(colj)))
            
            # check if this row is completed done already
            if empty == 0:
                continue
            
            # check if we have enough filled tiles in this row
            if filled == self.col_sums[colj]:
                # fill in the rest of the blank tiles
                for rowk in range(self.rows):
                    if self.tiles[rowk][colj] == -1:
                        self.tiles[rowk][colj] = 0
                        changed = True
                continue
    
            # check if we have enough filled tiles in this row
            if filled + empty == self.col_sums[colj]:
                # fill in the rest of the filled tiles
                for rowk in range(self.rows):
                    if self.tiles[rowk][colj] == -1:
                        self.tiles[rowk][colj] = 1
                        changed = True
                continue
        return changed
    
    
    # Returns true if any new tiles filled in
    def fillDiagonals(self):
        changed = False
        # check rows against row goals
        for k in range(self.rows):
            for j in range(self.cols):
                if self.tiles[k][j] == 1:
                    # make sure the diagonal adjacent tiles are blanked
                    if k > 0 and j > 0:
                        if self.tiles[k-1][j-1] == 1:
                            raise Exception("Invalid diagonal filled at "+str((k-1,j-1)))
                        if self.tiles[k-1][j-1] == -1:
                            self.tiles[k-1][j-1] = 0
                            changed = True
                    if k < self.rows-1 and j > 0:
                        if self.tiles[k+1][j-1] == 1:
                            raise Exception("Invalid diagonal filled at "+str((k+1,j-1)))
                        if self.tiles[k+1][j-1] == -1:
                            self.tiles[k+1][j-1] = 0
                            changed = True
                    if k > 0 and j < self.cols-1:
                        if self.tiles[k-1][j+1] == 1:
                            raise Exception("Invalid diagonal filled at "+str((k-1,j+1)))
                        if self.tiles[k-1][j+1] == -1:
                            self.tiles[k-1][j+1] = 0
                            changed = True
                    if k < self.rows-1 and j < self.cols-1:
                        if self.tiles[k+1][j+1] == 1:
                            raise Exception("Invalid diagonal filled at "+str((k+1,j+1)))
                        if self.tiles[k+1][j+1] == -1:
                            self.tiles[k+1][j+1] = 0
                            changed = True
        return changed
    
    # Returns true if all goals are met (game solved)
    def refreshGoals(self):
        # Count the number of ships of each size we have
        for length in self.goal_count.keys():
            self.ships_made[length] = 0
        
        # count along rows first
        for k in range(self.rows):
            length = 0
            for j in range(self.cols):
                if self.tiles[k][j] == 1:
                    if length >= 0:
                        if k > 0 and self.tiles[k-1][j] == 1:
                            # this is part of a column ship
                            length = -1
                        elif k < self.rows-1 and self.tiles[k+1][j] == 1:
                            length = -1
                        else:
                            length += 1
                            if j == self.cols-1:
                                #print('found row ship ' + str(length))
                                self.ships_made[length] += 1
                                length = -1
                elif self.tiles[k][j] == 0:
                    if length > 0:
                        #print('found row ship ' + str(length))
                        self.ships_made[length] += 1
                    length = 0
                elif self.tiles[k][j] == -1:
                    length = -1
                    
        
        # then count along columns
        for j in range(self.cols):
            length = 0
            for k in range(self.rows):
                if self.tiles[k][j] == 1:
                    if length >= 0:
                        if j > 0 and self.tiles[k][j-1] == 1:
                            # this is part of a row ship
                            length = -1
                        elif j < self.cols-1 and self.tiles[k][j+1] == 1:
                            length = -1
                        else:
                            length += 1
                            if k == self.rows-1:
                                if length > 1:
                                    #print('found col ship ' + str(length))
                                    self.ships_made[length] += 1
                                length = -1
                elif self.tiles[k][j] == 0:
                    if length > 1:
                        #print('found col ship ' + str(length))
                        self.ships_made[length] += 1
                    length = 0
                elif self.tiles[k][j] == -1:
                    length = -1
        for k in list(self.goal_count.keys()):
            if self.ships_made[k] != self.goal_count[k]:
                return False
        return True
    
    # Returns true if all goals are met (game solved)
    def guess(self):
        # Try filling in a random thing
        for k in range(self.rows):
            for j in range(self.cols):
                if self.tiles[k][j] == -1:
                    clone = copy.deepcopy(self)
                    clone.tiles[k][j] = 1
                    try:
                        if clone.solve():
                            self.tiles = copy.deepcopy(clone.tiles)
                            return True
                    except:
                        self.tiles[k][j] = 0
        raise Exception("No guesses worked")
    
    
    # Returns true if all goals are met (game solved)
    def solve(self):
        stuck = False
        while not stuck:
            stuck = not self.fillLines() and not self.fillDiagonals()
        if self.refreshGoals():
            return True
        else:
            return self.guess()
   
        
    
myGame = GameBoard([4,1,1,2,1,3,4,3], [5,1,0,5,1,5,1,1], {1:3, 2:3, 3:2, 4:1}, [], [(1,3)])
#myGame = GameBoard([3,0,4,0,2,1], [2,2,2,2,1,1], {1:3, 2:2, 3:1}, [(2,4), (5,3)], [(2,5), (5,2), (5,4), (4,3)])
myGame.solve()
print(myGame)
print("Finished")
