# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:35:37 2024

@author: tcapon
"""

import math
import os
import json
import copy
import itertools
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
from matplotlib.backend_bases import MouseButton


def grid2letter(x):
    letter = chr(ord('a') + (int(x-1)%26))
    copies = int(((x-1) // 26) + 1)
    return letter*copies
    
def print2d(data):
    return os.linesep.join([str(i)+'<'+', '.join([str(list(v)) for v in row]) + '>' for i,row in enumerate(data)])


mygame = None

def on_click(event):
    if event.button is MouseButton.LEFT and event.inaxes:
        print("Clicked ",event.xdata, ",", event.ydata)
        x = round(event.xdata*2)/2 - 1
        y = round(event.ydata*2)/2 - 1
        print(y,",",x)
        newnode = (y,x)
        if newnode in mygame.nodes:
            # remove node
            mygame.nodes.remove(newnode)
            print("Removing node at (",y,",",x,")")
        else:
            mygame.nodes.append(newnode)
            print("Adding node at (",y,",",x,")")
        mygame.fillNodes()
        mygame.graphBoard()
        
        
    
        
class GameBoard:
    rows = 5
    cols = 5
    tiles = []
    mirror_options = []
    path_options = []
    nodes = []
    node_tiles = []
    changed_tiles = []
    connected_tiles = []
    axes = None
    numberOfGuesses = 0
    numberOfMerges = 0
    
    def __init__(self, rows=None, cols=None, nodes=[], filename=None):
        if filename:
            # ignore other arguments if filename is given
            self.loadBoard(filename)
        else:
            self.rows = rows or cols
            self.cols = cols or rows
            self.nodes = nodes
        self.tiles = [[-1 for i in range(self.cols)] for j in range(self.rows)]
        self.node_tiles = [[False for i in range(self.cols)] for j in range(self.rows)]
        self.changed_tiles = [[False for i in range(self.cols)] for j in range(self.rows)]
        self.connected_tiles = [[False for i in range(self.cols)] for j in range(self.rows)]
        self.mirror_options = [[[] for i in range(self.cols)] for j in range(self.rows)]
        self.path_options = [[[] for i in range(self.cols)] for j in range(self.rows)]
        self.fillNodes()
        self.fillMirrors()
    
    def __str__(self):
        return os.linesep.join([''.join(["{0: >5}{1}".format((t if t>=0 else ' '),('*' if n else ('+' if c else ' '))) for t,n,c in zip(row,node_row,change_row)]) for row,node_row,change_row in zip(self.tiles,self.node_tiles,self.changed_tiles)]) + '\n' + str(self.countEmpties()) + ' tiles to go'
    
    def saveBoard(self,filename):
        with open(filename, 'w', encoding='utf8') as outfile:
            saveData = {"rows":self.rows,
                        "cols":self.cols,
                        "nodes":self.nodes,
                        "tiles":self.tiles}
            json.dump(saveData,outfile)
    
    def loadBoard(self,filename):
        with open(filename) as infile:
            saveData = json.load(infile)
            self.cols = saveData['cols']
            self.rows = saveData['rows']
            self.nodes = saveData["nodes"]
            self.tiles = saveData["tiles"]
            
    def graphBoard(self):
        nodesy = [node[0]+1 for node in self.nodes]
        nodesx = [node[1]+1 for node in self.nodes]
        if self.axes:
            ax = self.axes
            ax.clear()
        else:
            fig, ax = plt.subplots()
            self.axes = ax
            self.click_binding = fig.canvas.mpl_connect('button_press_event', on_click)
        yticks = [y+0.5 for y in range(0,self.rows)]
        xticks = [x+0.5 for x in range(0,self.cols)]
        plt.grid(which='minor')
        ax.set_ylim([0.5,self.rows+0.5])
        ax.set_xlim([0.5,self.cols+0.5])
        ax.xaxis.set_major_locator(FixedLocator(range(1,self.cols+1)))
        ax.yaxis.set_major_locator(FixedLocator(range(1,self.rows+1)))
        ax.set_xticks(xticks,minor=True)
        ax.set_yticks(yticks,minor=True)
        ax.tick_params(which='both', length=0)
        xlabels = ax.get_xticks().tolist()
        newxlabels = [grid2letter(x) for x in xlabels]
        ax.set_xticklabels(newxlabels)
        ax.invert_yaxis()
        ax.plot(nodesx, nodesy, 'bo')
    
    def graphSolution(self):
        self.graphBoard()
        ax = self.axes
        # loop through each box edge and draw a line if needed
        # vertical lines
        for y,row in enumerate(self.tiles):
            for x,tile in enumerate(row):
                if tile != -1:
                    if x > 0:
                        if row[x-1] != tile and row[x-1] != -1:
                            # Previous tile in row was different, draw a line behind us
                            ax.plot([x+0.5,x+0.5], [y+0.5,y+1.5],'-r')
                    if y > 0:
                        if self.tiles[y-1][x] != tile and self.tiles[y-1][x] != -1:
                            # Tile above was different, draw a line above us
                            ax.plot([x+0.5,x+1.5], [y+0.5,y+0.5],'-r')
        
        
    
    def getTile(self,point):
        return self.tiles[point[0]][point[1]]
    
    def getMirrors(self,point):
        return self.mirror_options[point[0]][point[1]]
    
    def getNeighbors(self,point):
        r = point[0]
        c = point[1]
        neighbors = []
        if r > 0:
            neighbors.append((r-1,c))
        if r < self.rows-1:
            neighbors.append((r+1,c))
        if c > 0:
            neighbors.append((r,c-1))
        if c < self.cols-1:
            neighbors.append((r,c+1))
        return neighbors

        
    def countEmpties(self):
        empties = 0
        for r, row in enumerate(self.tiles):
            for c, tile in enumerate(row):
                if tile == -1:
                    empties = empties + 1
        return empties
    
    def mirrorPoint(self, node, point):
        # Return the coordinates of the point mirrored around the given node
        # node + (node - point) = 2*node - point
        if isinstance(node,int):
            node = self.nodes[node]
        mpt = (int(node[0]*2 - point[0]), int(node[1]*2 - point[1]))
        if mpt[0] < 0 or mpt[0] > self.rows-1 or mpt[1] < 0 or mpt[1] > self.cols-1:
            return None
        return mpt
    
    
    # Run once to fill the tile matrix based on the node list
    def fillNodes(self):
        for idx, node in enumerate(self.nodes):
            for r in range(math.floor(node[0]), math.ceil(node[0])+1):
                for c in range(math.floor(node[1]), math.ceil(node[1])+1):
                    self.tiles[r][c] = idx
                    self.node_tiles[r][c] = True  # Mark this as a node
                    self.connected_tiles[r][c] = True  # Mark this as node-connected
           
    # Run once to fill the mirror_options matrix based on what tiles are accessible to mirror around each node
    def fillMirrors(self):
        # Perform one iteration to fill in which nodes each empty tile could
        # belong to based on whether the mirrored tile is available
        self.mirror_options = [[set([]) for i in range(self.cols)] for j in range(self.rows)]
        for r, row in enumerate(self.tiles):
            for c, tile in enumerate(row):
                if tile == -1:
                    newtile = []
                    #print('Solving for '+str((r,c)))
                    # try mirroring the point around each node
                    for n, node in enumerate(self.nodes):
                        mpt = self.mirrorPoint(node,(r,c))
                        if mpt:
                            # mirrored point is on the gameboard
                            # make sure it's also blank or the same as the node
                            mtile = self.getTile(mpt)
                            if mtile == -1 or mtile == n:
                                newtile.append(n)
                    self.mirror_options[r][c] = set(newtile)
        return self.mirror_options
    
    # Re-check all currently assigned mirror_options (not normally needed)
    def updateMirrors(self):
        # Check the existing mirror options to see if any have changed
        for r, row in enumerate(self.mirror_options):
            for c, tile_options in enumerate(row):
                # For each node that was previously able to mirror this tile, 
                # only include it if its mirror is still free
                self.mirror_options[r][c] = set([n for n in tile_options if (
                                                 self.getTile(self.mirrorPoint(self.nodes[n],(r,c))) == -1
                                                 and n in self.getMirrors(self.mirrorPoint(self.nodes[n],(r,c)))
                                                )])
                
                    
    # Re-scan the whole board to see what mirror-able tiles are accessible from their nodes.
    def fillPaths(self):
        # Find which nodes are accessible from each open tile
        # Nodes and accessible values propagate along axes
        # Erase previous path data and recreate it based on solved and current mirror_option tiles only
        self.path_options = [[set([]) for i in range(self.cols)] for j in range(self.rows)]
        changeMade = True
        loopCount = 0
        while changeMade:
            changeMade = False # clear flag for this iteration
            loopCount = loopCount + 1
            for r, row in enumerate(self.tiles):
                for c, tile in enumerate(row):
                    if tile == -1:
                        # This tile is not solved yet
                        newtile = []
                        pt = (r,c)
                        # Find all options in adjacent tiles
                        neighbors = self.getNeighbors(pt)
                        for npt in neighbors:
                            nn = self.getTile(npt)
                            if nn != -1:
                                newtile.append(nn)
                            newtile.extend(self.path_options[npt[0]][npt[1]])
                        newtile = self.mirror_options[r][c].intersection(set(newtile))
                        if newtile != self.path_options[r][c]:
                            changeMade = True
                            self.path_options[r][c] = newtile
        print("Finished "+str(loopCount)+" iterations finding accessible tiles")   
        return self.path_options
    
    # When a tile is solved, remove that tile as an option from the other nodes it can mirror around
    def clearMirrors(self,point):
        # For the given point, that was just solved,
        # if there were any other mirror options for it, remove the mirrors of the ones that weren't solved
        for n in self.mirror_options[point[0]][point[1]]:
            node = self.nodes[n]
            mpt = self.mirrorPoint(node,point)
            if n in self.mirror_options[mpt[0]][mpt[1]]:
                self.mirror_options[mpt[0]][mpt[1]].remove(n)
        self.mirror_options[point[0]][point[1]] = set([])
    
    
    def markTileConnected(self,point):
        # Given a solved point, mark it connected
        # Call recursively to all its neighbors that also become newly connected
        r = point[0]
        c = point[1]
        n = self.tiles[r][c]
        self.connected_tiles[r][c] = True
        neighbors = self.getNeighbors(point)
        for npt in neighbors:
            if self.getTile(npt) == n and not self.connected_tiles[npt[0]][npt[1]]:
                # this adjacent tile is solved for the same node as this new one
                # and the adjacent tile is not connected yet
                # mark the new tile as connected
                self.markTileConnected(npt)
    
    # Mark tile as solved for this node
    # Mark mirrored tile as solved for this node
    # Check if tile is connected to the node
    # Update adjacent tiles if connected status might have changed
    def solveTile(self,point,nodeNumber):
        r = point[0]
        c = point[1]
        node = self.nodes[nodeNumber]
        self.tiles[r][c] = nodeNumber
        self.changed_tiles[r][c] = True
        self.clearMirrors(point)
        mpt = self.mirrorPoint(node,point)
        if self.tiles[mpt[0]][mpt[1]] == -1:
            print('Filling in',mpt,'for',nodeNumber)
            self.tiles[mpt[0]][mpt[1]] = nodeNumber
            self.clearMirrors(mpt)
            self.changed_tiles[mpt[0]][mpt[1]] = True
        else:
            raise Exception('Mirror tile not available for '+str(point)+' against node '+str(node))
        # Update flag for whether this tile is connected to the node or not
        neighbors = self.getNeighbors(point)
        for npt in neighbors:
            nnode = self.getTile(npt)
            if nnode == nodeNumber and self.connected_tiles[npt[0]][npt[1]]:
                # this adjacent tile is solved for the same node as this new one
                # and the adjacent tile is connected to the node
                # so this one is also
                self.markTileConnected(point)
                self.markTileConnected(mpt)
                break
        
            
    
    def mergePathsToMirrors(self):
        # Remove items from the mirror_options lists if they are not pathable
        self.changed_tiles = [[False for i in range(self.cols)] for j in range(self.rows)]
        for r, row in enumerate(self.tiles):
            for c, tile in enumerate(row):
                if tile == -1:
                    newtile = []
                    pt = (r,c)
                    for a in self.mirror_options[r][c]:
                        if a in self.path_options[r][c]:
                            # Make sure the mirror point is also in the path options
                            mpt = self.mirrorPoint(self.nodes[a],pt)
                            if a in self.path_options[mpt[0]][mpt[1]]:
                                newtile.append(a)
                        
                    # Now see if there is only one valid option for this tile
                    if len(newtile) == 0:
                        print(print2d(self.mirror_options))
                        print('No valid nodes for tile '+str(pt))
                        return None
                    elif len(newtile) == 1:
                        # Claim this tile and its mirror
                        n = newtile[0]
                        print('Filling in',pt,'for',n)
                        self.solveTile(pt,n)
                        
                    else:
                        self.mirror_options[r][c] = set(newtile)
                        
        return self.mirror_options
    
    
    def pathNextFn(self,series):
        # get the current endpoint of the path
        originPt = series[0]
        nodeNumber = self.getTile(originPt)
        nodePoint = self.nodes[nodeNumber]
        currentPt = series[-1]
        # Check if we made it to a connected tile
        if self.getTile(currentPt) == nodeNumber and self.connected_tiles[currentPt[0]][currentPt[1]]:
            # We are at the end condition, no further path steps needed
            return []
        
        # return all the neighbors with valid mirror option *or already filled in for this node* and not already in the path 
        neighbors = [pt for pt in self.getNeighbors(currentPt) if not (pt in series) and not (self.mirrorPoint(nodePoint,pt) in series) and 
                       #( (self.getTile(pt) == self.getTile(originPt) and self.connected_tiles[pt[0]][pt[1]]) or
                       ( (self.getTile(pt) == self.getTile(originPt)) or
                         (nodeNumber in self.mirror_options[pt[0]][pt[1]]) ) ]
        return neighbors
        
    
    # Iterator to return each possible path from a point to a connected point of the same node
    def pathSeriesGenerator(self,startPt):
        series = [startPt]
        options = [self.pathNextFn(series)]
        while len(options) > 0:
            # iterate
            if len(options[-1]) > 0:
                # Try next one of this level
                series.append(options[-1].pop(0))
                options.append(self.pathNextFn(series))
                if len(options[-1]) == 0:
                    yield series
            else:
                # Already done the last one of this leg, yield and back up
                series.pop(-1)
                options.pop(-1)
    
    
    def findIsolatedTiles(self):
        # Check if any of the newly solved tiles are isolated from their nodes
        # Do this after every tile has been filled this iteration
    
        # mirror_options has all the possible nodes for each tile with both a 
        # path and a mirror, so any path made among them can also be mirrored.
        
        for r, row in enumerate(self.tiles):
            for c, tile in enumerate(row):
                n = self.tiles[r][c]
                if n != -1 and not self.connected_tiles[r][c]:
                    pt = (r,c)
                    # solved tile is not adjacent to another of the same node
                    print("Found isolated tile at",pt,"for node",n)
                
                    # Now walk outwards from this tile through the available mirror_options
                    # Record how many steps away each one is
                    # Until you get to a connected tile
                    # If there is only one tile with a specific distance
                    common_points = None
                    for path in self.pathSeriesGenerator(pt):
                        if self.getTile(path[-1]) == n:
                            if common_points == None:
                                common_points = set(path[1:-1])
                            else:
                                common_points = common_points.intersection(set(path[1:-1]))
                            #print('path:',path)
                            #print('common points:',common_points)
                            if len(common_points) == 0:
                                break
                    
                    # Any point that is common to all paths can be solved
                    if common_points:
                        for cpt in common_points:
                            print('Filling in connecting tile ',cpt,'for',n)
                            self.solveTile(cpt,n)
            
    
    class STATUS(Enum):
        ERROR = -1
        DONE = 0
        TIMEOUT = 1
        STUCK = 2
    
    def forkBoard(self):
        # Do something to make a guess and then try to solve from there
        # find the next tile to assign as a guess
        solve_point_matrix = [[(r,c) for c,tile in enumerate(row) if len(tile)>1] for r,row in enumerate(self.mirror_options)]
        solve_point_list = sorted(
            itertools.chain.from_iterable(solve_point_matrix),
            key=lambda x: len(self.getMirrors(x))
            )
        for solve_point in solve_point_list:
            solve_node = next(iter(self.getMirrors(solve_point)))
            print("Guessing that",solve_point,"is node",solve_node,"... Trying to solve")
            self.numberOfGuesses = self.numberOfGuesses+1
            # Make a copy of the game, and pick the assignment of the selected point
            newgame = copy.deepcopy(self)
            newgame.solveTile(solve_point, solve_node)
            result = newgame.solveBoard(silent=True)
            
            if result == self.STATUS.ERROR:
                # remove the chosen option from the original copy of the board
                self.mirror_options[solve_point[0]][solve_point[1]].remove(solve_node)
                #mpt = self.mirrorPoint(solve_node, solve_point)
                #self.mirror_options[mpt[0]][mpt[1]].remove(solve_node)
                print("Proved that",solve_point,"cannot be node",solve_node)
                break
            elif result == self.STATUS.DONE:
                # Found the exact right solution
                print("Proved that",solve_point,"is definitely",solve_node)
                self.solveTile(solve_point,solve_node)
                break
            else:
                # Timed out or was inconclusive
                print("Inconclusive result from setting",solve_point,"to node",solve_node)
        
                
    def solveBoard(self,silent=False):
        togo = self.countEmpties()
        for i in range(50):
            if togo == 0:
                print("Finished in "+str(i)+" cycles!")
                return self.STATUS.DONE
            if not silent: print("Fill Paths ",i+1)
            self.fillPaths()
            if not silent: print("Merge ",i+1)
            if not self.mergePathsToMirrors():
                return self.STATUS.ERROR
            filled = togo - self.countEmpties()
            if filled == 0:
                self.findIsolatedTiles()
            if not silent: print(self)
            newtogo = self.countEmpties()
            if newtogo < togo:
                togo = newtogo
                self.numberOfMerges = self.numberOfMerges+1
            else:
                if not silent: 
                    print("Stuck at iteration ",i+1)
                    print("\nMiror Options:")
                    print(print2d(self.mirror_options))
                #print("\nPath Options:")
                #print(print2d(mygame.path_options))
                return self.STATUS.STUCK
        if not silent: 
            print("Not finished after",i,"iterations")
            print("\nMiror Options:")
            print(print2d(self.mirror_options))
        return self.STATUS.TIMEOUT
        


size = 15

mygame = GameBoard(rows=size,cols=size)
#mygame = GameBoard(filename="fifteen3.txt")
#mygame = GameBoard(filename="fifteen1.txt")
#mygame = GameBoard(filename="monthly1.txt")
#mygame = GameBoard(filename="daily14.txt")
#mygame = GameBoard(filename="weekly513.txt")
#mygame = GameBoard(filename="fifteen4.txt")
#mygame = GameBoard(filename="fifteen2.txt")

#print("Initial State")
#print(mygame)
#mygame.graphBoard()
savename = "fifteen46.txt"
#makeerror()
mygame = GameBoard(filename=savename)
#mygame.saveBoard(savename)
#print("Saved ",size,"x",size," game with ",len(mygame.nodes), " nodes as '",savename,"'")
status = mygame.solveBoard()
while status != GameBoard.STATUS.DONE:
    print(status)
    if status == GameBoard.STATUS.ERROR:
        break
    elif status == GameBoard.STATUS.STUCK:
        input("Press enter for next guess")
        mygame.forkBoard()
    elif status == GameBoard.STATUS.TIMEOUT:
        break
    status = mygame.solveBoard()
    
mygame.graphSolution()
print("Made",mygame.numberOfMerges,"merge cycles in the solution path")
print("Used",mygame.numberOfGuesses,"guesses while solving")


#while(pleaseExit == False):
#    pass

    
