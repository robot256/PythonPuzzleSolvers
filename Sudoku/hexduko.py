# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:12:39 2018

@author: tcapon
"""


import copy
import math
import itertools



A = 10
B = 11
C = 12
D = 13
E = 14
F = 15
G = 16

hexdict = {0:'\u2610',1:'1',2:'2',3:'3',4:'4',
           5:'5',6:'6',7:'7',8:'8',
           9:'9',10:'A',11:'B',12:'C',
           13:'D',14:'E',15:'F',16:'G'}

hexchar = {'10':'A','11':'B','12':'C',
           '13':'D','14':'E','15':'F','16':'G'}

#board = [
#[E,0,0,5, 0,C,0,0, 6,3,0,0, 2,0,0,0],
#[3,0,2,1, E,0,0,0, 0,D,0,7, 0,0,6,0],
#[A,0,8,0, 0,7,G,0, 0,0,0,0, F,9,0,0],
#[0,6,0,D, A,0,B,0, E,0,0,C, 0,3,0,0],
#
#[7,0,0,E, 0,0,5,0, 0,4,3,0, 9,0,C,0],
#[0,0,0,B, 8,0,E,0, C,0,0,9, 4,0,0,0],
#[0,D,0,0, 9,B,0,0, 1,0,0,0, 7,2,0,G],
#[0,3,0,2, 0,0,0,0, 0,6,0,0, 0,E,1,0],
#
#[0,E,F,0, 0,0,9,0, 0,0,0,0, B,0,8,0],
#[B,0,6,C, 0,0,0,E, 0,0,D,G, 0,0,9,0],
#[0,0,0,G, 1,0,0,4, 0,8,0,2, 3,0,0,0],
#[0,4,0,8, 0,D,F,0, 0,C,0,0, 6,0,0,7],
#
#[0,0,E,0, C,0,0,F, 0,A,0,5, 1,0,7,0],
#[0,0,5,6, 0,0,0,0, 0,2,9,0, 0,8,0,D],
#[0,G,0,0, 2,0,A,0, 0,0,0,F, C,5,0,6],
#[0,0,0,F, 0,0,6,9, 0,0,C,0, 0,0,0,4]]

#board = [
#    [F,0,0,0,7,D,0,0,0,2,B,3,E,1,0,0],
#    [6,4,G,0,C,F,0,0,A,8,1,E,0,D,0,0],
#    [0,0,0,B,0,0,0,0,4,7,0,0,0,0,A,3],
#    [0,E,5,0,3,0,A,6,D,F,G,0,0,0,0,0],
#    [3,B,0,5,0,0,0,9,0,A,0,1,G,7,C,E],
#    [2,A,0,0,B,3,0,0,0,E,0,0,0,F,0,0],
#    [0,0,0,0,0,0,E,A,0,0,C,D,0,5,2,9],
#    [D,7,0,0,G,0,0,0,0,5,3,0,0,6,0,A],
#    [7,0,D,0,0,A,8,0,0,0,0,5,0,0,3,6],
#    [5,G,B,0,2,1,0,0,E,3,0,0,0,0,0,0],
#    [0,0,1,0,0,0,7,0,0,0,8,B,0,0,E,5],
#    [E,C,3,8,6,0,4,0,1,0,0,0,A,0,9,G],
#    [0,0,0,0,0,E,B,2,7,C,0,A,0,9,D,0],
#    [B,2,0,0,0,0,F,7,0,0,0,0,6,0,0,0],
#    [0,0,E,0,A,8,6,C,0,0,D,4,0,3,F,7],
#    [0,0,7,A,D,9,3,0,0,0,5,2,0,0,0,B]
#   ]

#board = [
#    [0,4,0,0,G,0,6,0,5,B,E,0,0,0,A,0],
#    [2,0,0,0,3,0,1,C,0,8,0,0,0,G,0,0],
#    [0,0,F,0,4,0,0,0,C,2,0,D,0,6,3,0],
#    [0,1,0,0,A,0,0,D,0,0,9,4,0,F,0,B],
#    [0,A,1,7,0,0,0,0,0,D,0,0,B,0,2,0],
#    [0,B,D,0,5,9,C,2,3,0,7,0,0,0,1,0],
#    [0,6,C,0,0,0,0,0,0,0,0,2,F,0,0,4],
#    [0,2,0,F,0,A,E,B,4,0,1,6,C,0,0,0],
#    [0,0,0,5,C,E,0,3,9,G,2,0,A,0,D,0],
#    [C,0,0,4,8,0,0,0,0,0,0,0,0,5,9,0],
#    [0,9,0,0,0,6,0,F,8,4,5,3,0,C,E,0],
#    [0,F,0,3,0,0,A,0,0,0,0,0,4,7,8,0],
#    [F,0,4,0,D,8,0,0,2,0,0,G,0,0,5,0],
#    [0,3,9,0,E,0,7,G,0,0,0,F,0,1,0,0],
#    [0,0,8,0,0,0,5,0,0,7,0,9,0,0,0,D],
#    [0,7,0,0,0,C,3,A,0,E,0,5,0,0,F,0]
#   ]

board = [
    [0,C,D,0,0,E,7,0,6,0,F,0,0,0,0,5],
    [0,0,4,0,0,0,G,0,7,0,0,2,0,0,0,F],
    [F,0,0,1,0,0,4,0,0,0,B,8,D,0,2,A],
    [0,0,2,0,0,9,F,A,0,0,E,1,0,7,6,0],
    [0,3,A,B,0,0,0,0,0,F,0,C,0,G,0,0],
    [E,0,0,F,A,4,C,3,D,0,0,0,0,0,0,0],
    [C,4,5,0,E,0,2,0,A,0,0,0,F,0,0,7],
    [0,6,1,0,0,0,5,0,B,0,0,0,C,0,A,0],
    [0,5,0,A,0,0,0,8,0,1,0,0,0,B,C,0],
    [9,0,0,7,0,0,0,1,0,3,0,4,0,5,8,D],
    [0,0,0,0,0,0,0,D,E,A,9,7,2,0,0,6],
    [0,0,3,0,F,0,A,0,0,0,0,0,9,4,E,0],
    [0,D,F,0,5,C,0,0,1,2,7,0,0,A,0,0],
    [A,E,0,5,6,D,0,0,0,4,0,0,G,0,0,C],
    [G,0,0,0,7,0,0,4,0,6,0,0,0,D,0,0],
    [B,0,0,0,0,A,0,E,0,G,5,0,0,1,F,0]
   ]

def multiReplace(s,d=hexchar):
    s = str(s)
    for k in d:
        s = s.replace(k,d[k])
    s = s.replace(', ','')
    
    return s

def PrintBoard(b):
    s = ''
    for irow,row in enumerate(b):
        for icol,elem in enumerate(row):
            if isinstance(elem,int):
                s = s + '\\' + hexdict[elem] + '/ '
            else:
                s = s + multiReplace(elem) + ' '
            if icol % 4 == 3:
                s = s + '  '
        s = s + '\n\n'
        if irow % 4 == 3:
            s = s + '\n'
    print('_______________________________________')
    print(s.strip('\n'))
    print('---------------------------------------')
    
PrintBoard(board)


# Now replace all the zeros with a list of all the possible combos
allNums = [1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G]
boardSize = len(board[0])
boxSize = int(math.sqrt(boardSize))

for row in board:
    row[:] = [copy.deepcopy(allNums) if x==0 else x for x in row]


def UpdatePencils(b):
    count = 0
    # Now start eliminating elements
    for row in b:
        nums = [x for x in row if isinstance(x,int)]
        for element in row:
            for num in nums:
                try:
                    count = count + element.count(num)
                    element.remove(num)
                except (ValueError, AttributeError):
                    pass
    
    
    # eliminate along columns
    
    for icol in range(boardSize):
        nums = [row[icol] for row in b if isinstance(row[icol],int)]
        for row in b:
            for num in nums:
                try:
                    count = count + row[icol].count(num)
                    row[icol].remove(num)
                except (ValueError, AttributeError):
                    pass
    
    # eliminate within boxes
    
    for brow in range(boxSize):
        for bcol in range(boxSize):
            # now check all the boxes
            nums = []
            for irow in range(boxSize):
                for icol in range(boxSize):
                    x = b[brow*boxSize + irow][bcol*boxSize + icol]
                    if isinstance(x,int):
                        nums.append(x)
            for irow in range(boxSize):
                for icol in range(boxSize):
                    element = b[brow*boxSize + irow][bcol*boxSize + icol]
                    for num in nums:
                        try:
                            count = count + element.count(num)
                            element.remove(num)
                        except (ValueError, AttributeError):
                            pass
    return count

def ResolvePencils(b):
    # Upgrade all the pencil marks with only one option remaining
    count = 0
    for irow,row in enumerate(b):
        for icol in range(boardSize):
            try:
                if len(row[icol])==1:
                    row[icol] = row[icol][0]
                    count = count + 1
                    print('upgrading {0},{1} to \\{2}/'.format(irow,icol,multiReplace(row[icol])))
            except TypeError:
                pass
    return count


def ValidatePencils(b):
    # Upgrade all the pencil marks with only one option remaining
    count = 0
    for irow,row in enumerate(b):
        for icol in range(boardSize):
            try:
                if len(row[icol])==0:
                    count = count + 1
                    print('error at {0},{1}'.format(irow,icol))
            except TypeError:
                pass
    return count

def DeducePencils(b):
    # Find pencils with only one of that number in a given row, column, or box
    
    count = 0
    # Search rows for numbers with only one pencil
    for irow,row in enumerate(b):
        rowdict = {}
        for icol,element in enumerate(row):
            try:
                for x in element:
                    try:
                        rowdict[x].append(icol)
                    except KeyError:
                        rowdict[x] = [icol]
            except TypeError:
                pass
        for x in rowdict:
            if len(rowdict[x]) == 1:
                # x is only in one square's pencils
                if isinstance(row[rowdict[x][0]],int):
                    # Super fucking error
                    print('Found error at {0},{1}'.format(irow,rowdict[x][0]))
                    return -1
                count = count + 1
                print('row deduced {0},{1} {2} to be \\{3}/'.format(irow,rowdict[x][0],multiReplace(row[rowdict[x][0]]),multiReplace(x)))
                row[rowdict[x][0]] = x
                return count
        
    
    
    # eliminate along columns
    
    for icol in range(boardSize):
        coldict = {}
        for irow,row in enumerate(b):
            try:
                for x in row[icol]:
                    try:
                        coldict[x].append(irow)
                    except KeyError:
                        coldict[x] = [irow]
            except TypeError:
                pass
        for x in coldict:
            if len(coldict[x]) == 1:
                if isinstance(b[coldict[x][0]][icol],int):
                    # Super fucking error
                    print('Found error at {0},{1}'.format(coldict[x][0],icol))
                    return -1
                count = count + 1
                print('col deduced {0},{1} {2} to be \\{3}/'.format(coldict[x][0],icol,multiReplace(b[coldict[x][0]][icol]),multiReplace(x)))
                b[coldict[x][0]][icol] = x
                return count
#    # eliminate within boxes
    
    for brow in range(boxSize):
        for bcol in range(boxSize):
            # now check all the boxes
            boxdict = {}
            for irow in range(boxSize):
                for icol in range(boxSize):
                    try:
                        for x in b[brow*boxSize + irow][bcol*boxSize + icol]:
                            try:
                                boxdict[x].append([brow*boxSize + irow,bcol*boxSize + icol])
                            except KeyError:
                                boxdict[x] = [[brow*boxSize + irow,bcol*boxSize + icol]]
                    except TypeError:
                        pass
            for x in boxdict:
                if len(boxdict[x]) == 1:
                    if isinstance(b[boxdict[x][0][0]][boxdict[x][0][1]],int):
                        print('Found error at {0},{1}'.format(boxdict[x][0][0],boxdict[x][0][1]))
                        return -1
                    count = count + 1
                    print('box deduced {0},{1} {2} to be \\{3}/'.format(boxdict[x][0][0],boxdict[x][0][1],multiReplace(b[boxdict[x][0][0]][boxdict[x][0][1]]),multiReplace(x)))
                    b[boxdict[x][0][0]][boxdict[x][0][1]] = x
                    return count
    
    return count



def SetDeducePencils(b):
    # Find pencils with only one of that number in a given row, column, or box
    
    count = 0
    # Search rows for squares with only X pencil marks and find subsets within them
    for irow,row in enumerate(b):
        cellcount = {}
        totalcount = 0
        for icol,element in enumerate(row):
            try:
                cellcount[len(element)].append(icol)
                totalcount = totalcount + 1
            except KeyError:
                cellcount[len(element)] = [icol]
                totalcount = totalcount + 1
            except TypeError:
                pass
        #pprint([irow,cellcount])
        cellsmaller = []
        for setsize in [kk for kk in sorted(cellcount) if kk < totalcount]:
            # Find all the cells with this many or fewer pencils
            cellsmaller.extend(cellcount[setsize])
            # try all the permutations of this many things!
            for combo in itertools.combinations(cellsmaller,setsize):
                # we have e.g. 2 cells, need to see if they contain the same two pencil marks
                minset = set.union(*[set(row[c]) for c in combo])
                if len(minset) == setsize:
                    # Found a set!
                    print('found row set {0}:{1} {2}'.format(irow,str(sorted(combo)),multiReplace(str(minset))))
                    # Now eliminate these pencils from any cells outside the set
                    for icol,element in enumerate(row):
                        if icol in combo:
                            continue
                        try:
                            foo = len(element)
                            s = multiReplace(element)
                            for x in minset:
                                try:
                                    element.remove(x)
                                    count = count + 1
                                except ValueError:
                                    pass
                            if len(element) < foo:
                                print('purged {0} {2} -> {1}'.format(icol,multiReplace(element),s))
                        except TypeError:
                            pass
                    if count > 0:
                        return count
    
    
    # eliminate along columns
    
        # Search rows for squares with only X pencil marks and find subsets within them
    for icol in range(boardSize):
        cellcount = {}
        totalcount = 0
        for irow,row in enumerate(b):
            try:
                cellcount[len(row[icol])].append(irow)
                totalcount = totalcount + 1
            except KeyError:
                cellcount[len(row[icol])] = [irow]
                totalcount = totalcount + 1
            except TypeError:
                pass
        #pprint([icol,cellcount])
        cellsmaller = []
        for setsize in [kk for kk in sorted(cellcount) if kk < totalcount]:
            # Find all the cells with this many or fewer pencils
            cellsmaller.extend(cellcount[setsize])
            # try all the permutations of this many things!
            for combo in itertools.combinations(cellsmaller,setsize):
                # we have e.g. 2 cells, need to see if they contain the same two pencil marks
                minset = set.union(*[set(b[c][icol]) for c in combo])
                if len(minset) == setsize:
                    # Found a set!
                    print('found col set {0}:{1} {2}'.format(icol,str(sorted(combo)),multiReplace(str(minset))))
                    # Now eliminate these pencils from any cells outside the set
                    for irow,row in enumerate(b):
                        if irow in combo:
                            continue
                        try:
                            foo = len(row[icol])
                            s = multiReplace(row[icol])
                            for x in minset:
                                try:
                                    row[icol].remove(x)
                                    count = count + 1
                                except ValueError:
                                    pass
                            if len(row[icol]) < foo:
                                print('purged {0} {2} -> {1}'.format(irow,multiReplace(row[icol]),s))
                        except TypeError:
                            pass
                    if count > 0:
                        return count
    
    
    
    # Search for Box sets (bento?)
    for brow,bcol in itertools.product(range(boxSize),repeat=2):
        # list the coordinates in this box
        boxcells = [[brow*boxSize+irow, bcol*boxSize+icol] for irow,icol in itertools.product(range(boxSize),repeat=2)]
        
        # now check all the boxes
        cellcount = {}
        totalcount = 0
        
        for icell,cell in enumerate(boxcells):
            try:
                cellcount[len(b[cell[0]][cell[1]])].append(icell)
                totalcount = totalcount + 1
            except KeyError:
                cellcount[len(b[cell[0]][cell[1]])] = [icell]
                totalcount = totalcount + 1
            except TypeError:
                pass
        #pprint([(brow,bcol),cellcount])
        cellsmaller = []
        for setsize in [kk for kk in sorted(cellcount) if kk < totalcount]:
            # Find all the cells with this many or fewer pencils
            cellsmaller.extend(cellcount[setsize])
            # try all the permutations of this many things!
            for combo in itertools.combinations(cellsmaller,setsize):
                # we have e.g. 2 cells, need to see if they contain the same two pencil marks
                minset = set.union(*[set(b[boxcells[c][0]][boxcells[c][1]]) for c in combo])
                if len(minset) == setsize:
                    # Found a set!
                    print('found box set {0}:{1} {2}'.format((brow,bcol),str(sorted(combo)),multiReplace(str(minset))))
                    # Now eliminate these pencils from any cells outside the set
                    for icell,cell in enumerate(boxcells):
                        if icell in combo:
                            continue
                        try:
                            foo = len(b[cell[0]][cell[1]])
                            s = multiReplace(b[cell[0]][cell[1]])
                            for x in minset:
                                try:
                                    b[cell[0]][cell[1]].remove(x)
                                    count = count + 1
                                except ValueError:
                                    pass
                            if len(b[cell[0]][cell[1]]) < foo:
                                print('purged {0} {2} -> {1}'.format((brow,bcol),multiReplace(b[cell[0]][cell[1]]),s))
                        except TypeError:
                            pass
                    if count > 0:
                        return count
 
    return count

def ForkBoards(b):
    
    boards = []
    
    # Find the smallest number of pencils on the board
    minPencils = boardSize*boardSize
    minCell = None
    for irow,icol in itertools.product(range(boardSize),repeat=2):
        try:
            foo = len(b[irow][icol])
            if foo < minPencils:
                minPencils = foo
                minCell = (irow,icol)
        except TypeError:
            pass
    
    if minCell:
        # Fork the board into this many paths
        for mark in b[minCell[0]][minCell[1]]:
            boards.append(copy.deepcopy(b))
            boards[-1][minCell[0]][minCell[1]] = mark
            #print('Creating new fork:')
            #PrintBoard(boards[-1])
    else:
        boards = None
    
    return boards



#    
UpdatePencils(board)
if ValidatePencils(board) > 0:
        print('oops')
PrintBoard(board)
eliminateCount = 0
upgradeCount = 0
deduceCount = 0
setDeduceCount = 0
iterCount = 0
boardStack = []
restore = False
while iterCount == 0 or restore == True or (upgradeCount + eliminateCount + deduceCount + setDeduceCount > 0 
                         and iterCount < 400):
    iterCount = iterCount + 1
    eliminateCount = 0
    upgradeCount = 0
    deduceCount = 0
    setDeduceCount = 0
    error = False
    finished = False
    
    print('-------------- Iteration ' + str(iterCount) + ' --------------')
    #if iterCount==63 or iterCount==64:
    #    PrintBoard(board)
    eliminateCount = UpdatePencils(board)
    if eliminateCount == -1:
        error = True
    else:
        print('Eliminated '+ str(eliminateCount))
        upgradeCount = ResolvePencils(board)
        if upgradeCount ==-1:
            error = True
        elif upgradeCount == 0:
            deduceCount = DeducePencils(board)
            if deduceCount == -1:
                error = True
            elif deduceCount == 0:
                setDeduceCount = SetDeducePencils(board)
                if setDeduceCount == -1:
                    error = True
                elif setDeduceCount == 0:
                    # Nothing worked, take a guess
                    # Find the first square with the minimum number of pencil marks
                    try:
                        boardStack.extend(ForkBoards(board))
                        error = True
                    except TypeError:
                        finished = True
    
    if finished == True:
        print('Completed puzzle!')
    elif ValidatePencils(board) > 0 or error == True:
        try:
            print('Stumped at this point:')
            PrintBoard(board)
            board = boardStack.pop()
            print('Trying next guess:')
            PrintBoard(board)
            restore = True
        except IndexError:
            print('No Pencils Remaining, cannot complete puzzle!.')
            break
    else:
        restore = False
        
    #if eliminateCount > 0:
    #    PrintBoard(board)
    
    #if upgradeCount + eliminateCount + deduceCount > 0:
    #    PrintBoard(board)
    
PrintBoard(board)
print(iterCount)