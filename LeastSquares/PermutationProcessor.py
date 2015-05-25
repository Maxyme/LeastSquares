from ItemModel import ItemModel
from LockItem import LockItem
from Processor import Processor
import math 

class PermutationProcessor:
    # Temp size array
    tempSizeArray = []

    # Temp locked array to store items that have been locked, in order to try
    # all possible combinations
    lockItemsArray = []
    
    # The list of possibles solutions, contains all the possibles solutions of
    # different sizes
    ListOfPossibleSolutions = []

    # The number of squares in the puzzle array
    numberOfSquaresInPuzzleModel = 0

    # Public method - the one that calls all the others
    def getMinimumSquaresArray(self, puzzleModel):
        # Get array of possible sizes at each position
        possiblePermutationsArray = self.getPossibleSizePerSquare(puzzleModel)
        
        # Get the number of squares in the puzzle
        numberOfSquaresInPuzzleModel = 0
        for x in range(0, len(puzzleModel.puzzle)):
            self.numberOfSquaresInPuzzleModel += sum(item for item in puzzleModel.puzzle[x] if item == True)

        # Get all possible arrays using the possible sizes for each square
        lockArray = []
        combinationItem = []
        ListOfPossibleSolutions = self.getAllPermutations(puzzleModel, possiblePermutationsArray, lockArray, combinationItem)
        
        # Pick the first smallest array in the list and return
        minimumSquaresArray = []
        if len(ListOfPossibleSolutions) > 0:
            minimumSquaresArray = min(ListOfPossibleSolutions, key=len)

        return minimumSquaresArray

    # Start of Private methods ------------------------------------
    # Returns a array with all items and their possible square size
    def getPossibleSizePerSquare(self, puzzleModel):
        permutationArray = []
        for row in range(0, puzzleModel.height):
            for col in range(0, puzzleModel.width):
                squareAtPosition = puzzleModel.puzzle[row][col]
                if squareAtPosition:
                    #reset temp array
                    self.tempSizeArray = []
                    sizeArray = self.getPossibleSquareSize(row, col, puzzleModel.puzzle, 1)

                    itemToLook = ItemModel(row, col)
                    permutationArray.append({'Item': itemToLook, 'SizeArray': sizeArray})

        return permutationArray

    # Returns a array with all items and their possible square size
    def getPossibleSizePerSquareWithLock(self, puzzleModel, lockArray):
        permutationArray = []
        for row in range(0, puzzleModel.height):
            for col in range(0, puzzleModel.width):
                itemToLook = ItemModel(row, col)

                lockedSquare = next((lockItem for lockItem in lockArray if lockItem.Item.x == row and lockItem.Item.y == col and lockItem.Used == False), None)
                if lockedSquare is not None:
                    # Get the size to mark other squares even if size = lockedSquare.MaxRecursion ** 2
                    currentRecursionLevel = 0
                    size = self.getPossibleSquareSizeWithRecursionLock(row, col, puzzleModel.puzzle, currentRecursionLevel, lockedSquare.MaxRecursion)
                    sizeArray = [size]
                    #solution.append({'X': col, 'Y': row, 'Size': size})
                    permutationArray.append({'Item': itemToLook, 'SizeArray': sizeArray})
                    # Skip to the next item
                    continue

                squareAtPosition = puzzleModel.puzzle[row][col]
                if squareAtPosition:
                    #reset temp array
                    self.tempSizeArray = []
                    sizeArray = self.getPossibleSquareSize(row, col, puzzleModel.puzzle, 1)


                    permutationArray.append({'Item': itemToLook, 'SizeArray': sizeArray})

        return permutationArray

    # Returns an array containing the possible max size of each position
    def getPossibleSquareSize(self, itemXpos, itemYpos, itemArray, recursionLevel):
        # add to temp size array
        self.tempSizeArray.append(recursionLevel)
        
        # Check if all the neighbours for the recursion level are squares and
        # inside the itemArray

        neighboursArray = self.getNeighbours(itemXpos, itemYpos, itemArray, recursionLevel)

        # If all are inside, add to marked array and try again at a higher
        # recursion level
        if self.checkPossibleNeighbours(neighboursArray, itemArray):
            # recursion of method
            return self.getPossibleSquareSize(itemXpos, itemYpos, itemArray, recursionLevel + 1)

        # else, return the array of possible sizes
        else:
            return self.tempSizeArray

    # Returns an array with all possible permutations of the square by
    # Iterating all possible combinations of size for each position and
    # generate an array of object with the positions by finding all possible sizes with a recursion lock on an item
    def getAllPermutations(self, puzzleModel, permutationArray, lockArray, combinationItem):
        
        # return list of possible solution if all items are locked / all items are covered by current solution
        if len(lockArray) > 0:
            sumOfCoveredArea = sum(c.MaxRecursion ** 2 for c in lockArray)
            if self.numberOfSquaresInPuzzleModel == sumOfCoveredArea:
                return self.ListOfPossibleSolutions 

        for permutationItem in permutationArray:
            array = permutationItem["SizeArray"]
            item = permutationItem["Item"]

            # TODO?
            # Skips items with only 1 size possibility
            if len(array) == 1:
                continue

            # Loop array from biggest item to smallest
            for maxRecursion in reversed(array):
                # Add to lock array and get the possible combination array for the locked item
                lockItem = LockItem(item, maxRecursion, False)
                # adjust max recursion based on previous combination item if in combination item
                if len(combinationItem) > 0:
                    previousMaxSize = next((c['Size'] for c in combinationItem if lockItem.Item.x == c['X'] and lockItem.Item.y == c['Y']), None)
                    if previousMaxSize is not None:
                        lockItem.MaxRecursion = math.sqrt(previousMaxSize)
                        else # element was marked


                lockArray.append(lockItem)

                combinationItem = self.recursionLockSolve(puzzleModel, lockArray)

                # crazy recursion test!!
                possiblePermutationsArray = self.getPossibleSizePerSquareWithLock(puzzleModel, lockArray)

                # Get all possible arrays using the possible sizes for each square
                ListOfPossibleSolutions = self.getAllPermutations(puzzleModel, possiblePermutationsArray, lockArray, combinationItem)

                # Mark locked item as used
                itemIndex = lockArray.index(lockItem)
                lockArray[itemIndex].Used = True

                # Add combination to list of possibilities
                self.ListOfPossibleSolutions.append(combinationItem)

        # Recursive method to try all possibilities until the lockItems array
        # contains all possibilities
        #if self.lockItemsArray:
        #    return self.getAllPermutations(puzzleModel, permutationArray)
        #else:
        return self.ListOfPossibleSolutions
    
    # Advanced solve, tries to make a square as big as possible
    def recursionLockSolve(self, puzzleModel, lockArray):
        # reset marked array
        self.markedArray = []

        solution = []
        for row in range(0, puzzleModel.height):
            for col in range(0, puzzleModel.width):
                # Check if the square is a locked item and the use the max recursion for that item

                lockedSquare = next((lockItem for lockItem in lockArray if lockItem.Item.x == row and lockItem.Item.y == col and lockItem.Used == False), None)
                if lockedSquare is not None:
                    # Get the size to mark other squares even if size = lockedSquare.MaxRecursion ** 2
                    currentRecursionLevel = 0
                    size = self.getPossibleSquareSizeWithRecursionLock(row, col, puzzleModel.puzzle, currentRecursionLevel, lockedSquare.MaxRecursion)
                    solution.append({'X': col, 'Y': row, 'Size': size})
                    # Skip to the next item
                    continue

                # Check if there is a square at the position and it was not previously marked
                squareAtPosition = puzzleModel.puzzle[row][col]
                squareIsMarked = any(item.x == row and item.y == col for item in self.markedArray)

                # Add square and size to array if not marked 
                if squareAtPosition and not squareIsMarked:
                    recursionLevel = 1
                    size = self.getSquareSize(row, col, puzzleModel.puzzle, 1)
                    solution.append({'X': col, 'Y': row, 'Size': size})

        return solution

    # Get the maximum square size possible withing the puzzle limit
    def getSquareSize(self, itemXpos, itemYpos, itemArray, recursionLevel):
        # Check if all the neighbours for the recursion level are squares and
        # inside the itemArray
        neighboursArray = self.getNeighbours(itemXpos, itemYpos, itemArray, recursionLevel)

        # If all are inside, add to marked array and try again at a higher
        # recursion level
        if self.checkNeighbours(neighboursArray, itemArray):
            # add to marked items array
            self.markedArray.extend(neighboursArray)
            # recursion of method
            return self.getSquareSize(itemXpos, itemYpos, itemArray, recursionLevel + 1)

        # else, return the square of the last recursion level
        else:
            return recursionLevel ** 2

    # Get the possible recursion level, or square side of each item
    def getPossibleSquareSizeWithRecursionLock(self, itemXpos, itemYpos, itemArray, recursionLevel, maxRecursionLevel):
        # Check if all the neighbours for the recursion level are squares and
        # inside the itemArray
        neighboursArray = self.getNeighbours(itemXpos, itemYpos, itemArray, recursionLevel)

        # If all are inside, add to marked array and try again at a higher
        # recursion level
        if self.checkPossibleNeighbours(neighboursArray, itemArray) and recursionLevel != maxRecursionLevel:
            # add to marked items array
            self.markedArray.extend(neighboursArray)
            # recursion of method
            return self.getPossibleSquareSizeWithRecursionLock(itemXpos, itemYpos, itemArray, recursionLevel + 1, maxRecursionLevel)

         # else, return the square of the last recursion level
        else:
            return recursionLevel ** 2

    # Make an array of the possible items based on recursion level.
    def getNeighbours(self, itemX, itemY, puzzleArray, recursionLevel):
        neighboursArray = []

        # Find the number of neighbours for the recursion level:
        # recursionLevel*2 - 1
        numNeighbours = recursionLevel * 2 + 1

        # get right neighbour items
        for i in range(recursionLevel):
            rightItem = ItemModel(itemX + recursionLevel, itemY + i)
            neighboursArray.append(rightItem)

        # get bottom neighbour items
        for i in range(recursionLevel):
            underItem = ItemModel(itemX + i, itemY + recursionLevel)
            neighboursArray.append(underItem)

        # get bottom corner item
        bottomCornerItem = ItemModel(itemX + recursionLevel, itemY + recursionLevel)
        neighboursArray.append(bottomCornerItem)

        # return the array
        return neighboursArray
    
    # Checks the neighbours to see if they are true and inside the array
    def checkNeighbours(self, neighboursArray, puzzleArray):
        # simple check
        if len(neighboursArray) <= 0:
            return False

        # iterate all the items to see if they exists and are true and not
        # already used in another square (marked)
        # If one is false or doesn't exist, the loop returns false
        for item in neighboursArray:
            try:
                isSquare = puzzleArray[item.x][item.y]
                squareIsMarked = any(marked.x == item.x and marked.y == item.y for marked in self.markedArray)
                if not isSquare or squareIsMarked:
                    return False
                # return isSquare
            except IndexError:
                # break
                return False

        return True
   
    # Make an array of the possible items based on recursion level.
    def getPossibleNeighbours(self, itemX, itemY, puzzleArray, recursionLevel):
        neighboursArray = []

        # Find the number of neighbours for the recursion level:
        # recursionLevel*2 - 1
        numNeighbours = recursionLevel * 2 + 1

        # get right neighbour items
        for i in range(recursionLevel):
            rightItem = ItemModel(itemX + recursionLevel, itemY + i)
            neighboursArray.append(rightItem)

        # get bottom neighbour items
        for i in range(recursionLevel):
            underItem = ItemModel(itemX + i, itemY + recursionLevel)
            neighboursArray.append(underItem)

        # get bottom corner item
        bottomCornerItem = ItemModel(itemX + recursionLevel, itemY + recursionLevel)
        neighboursArray.append(bottomCornerItem)

        # return the array
        return neighboursArray

    # Checks the neighbours to see if they are true and inside the array
    def checkPossibleNeighbours(self, neighboursArray, puzzleArray):
        # simple check
        if len(neighboursArray) <= 0:
            return False

        # iterate all the items to see if they exists and are true and not
        # already used in another square (marked)
        # If one is false or doesn't exist, the loop returns false
        for item in neighboursArray:
            try:
                isSquare = puzzleArray[item.x][item.y]
                # special method for permutation check
                if not isSquare:
                    return False

            except IndexError:
                # break
                return False

        return True