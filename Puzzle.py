# read puzzle from .txt file
def GetPuzzle(filename):
    f = open(filename, "r")
    PuzzleMatrix = [list(line.split("\n")[0]) for line in f]
    return PuzzleMatrix

# print puzzle
def PrintPuzzle(puzzle):
    for i in range(len(puzzle)):
        print("".join(puzzle[i]))

# check if coordinate is valid
def IsValidCoordinate(i,j,N):
    if i < 1 or i > N or j < 1 or j > N:
        return False
    return True
    
# check if a tile is a tent candidate
def IsTileTentCandidate(puzzle,i,j):
    size = len(puzzle)-1
    if IsValidCoordinate(i-1,j,size):
        if puzzle[i-1][j] == "P":
            return True
    if IsValidCoordinate(i+1,j,size):
        if puzzle[i+1][j] == "P":
            return True
    if IsValidCoordinate(i,j-1,size):
        if puzzle[i][j-1] == "P":
            return True
    if IsValidCoordinate(i,j+1,size):
        if puzzle[i][j+1] == "P":
            return True
    return False

# check if tile is in a tent area
def IsTileTentArea(puzzle,i,j):
    size = len(puzzle)-1
    for ii in range(i-1,i+2):
        for jj in range(j-1,j+2):
            if IsValidCoordinate(ii,jj,size):
                if puzzle[ii][jj] == "T":
                    return True
    return False

# mark grass area
def MarkGrass(puzzle):
    size = len(puzzle)

    # mark untouched line or tent area line
    for i in range (1,size):
        for j in range (1,size):
            if puzzle[i][j] == ".":
                if not IsTileTentCandidate(puzzle,i,j) or IsTileTentArea(puzzle,i,j):
                    puzzle[i][j] = "G"

    # mark row with 0 tents left
    for i in range(1,size):
        if int(puzzle[i][0]) == 0:
            for j in range(1,size):
                if puzzle[i][j] == ".":
                    puzzle[i][j] = "G"

    # mark col with 0 tents left
    for j in range(1,size):
        if int(puzzle[0][j]) == 0:
            for i in range(1,size):
                if puzzle[i][j] == ".":
                    puzzle[i][j] = "G"
    return

# find empty location
def FindEmptyTile(puzzle, coord):
    size = len(puzzle)
    for i in range (1,size):
        for j in range (1,size):
            if puzzle[i][j] == ".":
                coord[0] = i
                coord[1] = j
                return True
    return False

# safe functionality
def IsSafe(puzzle,i,j):
    # check row constraints
    rowTents = puzzle[i][0]
    if int(rowTents) < 0:
        return False
    
    # check col constraints
    colTents = puzzle[0][j]
    if int(colTents) < 0:
        return False

    return True

# check if puzzle is really puzzle
def VerifySolve(puzzle):
    size = len(puzzle)
    for i in range(1,size):
        if puzzle[i][0] != "0":
            return []

    for j in range(1,size):
        if puzzle[0][j] != "0":
            return []
    
    return puzzle

# backtracking function
def SolvePuzzle(puzzle):
    puzzleBackup = [[puzzle[i][j] for j in range(len(puzzle))] for i in range(len(puzzle))]

    # find empty location
    coord = [0,0]
    if not FindEmptyTile(puzzle,coord):
        return VerifySolve(puzzle)

    x = coord[0]
    y = coord[1]

    # check if tent is safe to place
    if IsSafe(puzzle,x,y):
        puzzle[x][y] = "T"
        puzzle[x][0] = str(int(puzzle[x][0])-1)
        puzzle[0][y] = str(int(puzzle[0][y])-1)

        MarkGrass(puzzle)

        newPuzzle1 = SolvePuzzle(puzzle)
        if newPuzzle1 != []:
            return newPuzzle1

        puzzle = [[puzzleBackup[i][j] for j in range(len(puzzle))] for i in range(len(puzzle))]
        puzzle[x][y] = "G"

        newPuzzle2 = SolvePuzzle(puzzle)
        if newPuzzle2 != []:
            return newPuzzle2
        
    return []

# main program
if __name__ == "__main__":
    puzzle = GetPuzzle("Puzzle3.txt")
    puzzleProblem = [[puzzle[i][j] for j in range(len(puzzle))] for i in range(len(puzzle))]
    MarkGrass(puzzle)
    solved = SolvePuzzle(puzzle)
    if solved != []:
        for i in range (1,len(puzzle)):
            for j in range(1,len(puzzle)):
                if solved[i][j] == "G":
                    solved[i][j] = "."
        for i in range(len(puzzle)):
            puzzleProblem[i].append("   ")
            for j in range(len(puzzle)):
                puzzleProblem[i].append(solved[i][j])
        PrintPuzzle(puzzleProblem)
    else:
        print("Solution not found")
