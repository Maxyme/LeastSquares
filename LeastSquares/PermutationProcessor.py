from ItemModel import ItemModel
from LockItem import LockItem
from Processor import Processor

class PermutationProcessor:
    # Temp size array
    tempSizeArray = []

    # Temp locked array to store items that have been locked, in order to try
    # all possible combinations
    lockItemsArray = []
    
    # The list of possibles solutions, contains all the possibles solutions of
    # different sizes
    ListOfPossibleSolutions = []

    # Public method - the one that calls all the others
    def getMinimumSquaresArray(self, puzzleModel):
        # Get array of possible sizes at each position
        possiblePermutationsArray = self.getPossibleSizePerSquare(puzzleModel)
        
        # Get all possible arrays using the possible sizes for each square
        ListOfPossibleSolutions = self.getAllPermutations(puzzleModel, possiblePermutationsArray)
        
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
    def getAllPermutations(self, puzzleModel, permutationArray):
        lockArray = []

        for permutationItem in permutationArray:
            array = permutationItem["SizeArray"]
            item = permutationItem["Item"]

            # skips items with only 1 size possibility
            if len(array) == 1:
                continue

            # loop array from biggest item to smallest
            for maxRecursion in reversed(array):
                # Add to lock array
                lockItem = LockItem(item, maxRecursion)
                lockArray.append(lockItem)

                combinationItem = self.recursionLockSolve(puzzleModel, lockArray)

                # Add combination to list of possibilities
                ListOfPossibleSolutions.append(combinationItem)

        # Recursive method to try all possibilities until the lockItems array
        # contains all possibilities
        #if self.lockItemsArray:
        #    return self.getAllPermutations(puzzleModel, permutationArray)
        #else:
        return ListOfPossibleSolutions
    
    # Advanced solve, tries to make a square as big as possible
    def recursionLockSolve(self, puzzleModel, lockArray):
        # reset marked array
        self.markedArray = []

        solution = []
        for row in range(0, puzzleModel.height):
            for col in range(0, puzzleModel.width):
                # Check if the square is a locked item and the use the max recursion for that item

                squareIsLocked = any(lockItem.Item.x == row and lockItem.Item.y == col for lockItem in lockArray)

                if (row == itemToLock.x and col == itemToLock.y):
                    # Get size and mark neighbours using the item max recursion lock

                    # start at recursion level 1 to mark neighbourgh items
                    currentRecursionLevel = 1
                    size = self.getPossibleSquareSizeWithRecursionLock(row, col, puzzleModel.puzzle, currentRecursionLevel, itemMaxRecursion)
                         
                    size = itemMaxRecursion ** 2
                    solution.append({'X': col, 'Y': row, 'Size': size})
                    # Then skip to the next item
                    continue


                # check for true, which means it is a square and check for
                # marking from previous
                squareAtPosition = puzzleModel.puzzle[row][col]
                
                # check for marked item, which means it is used in a different
                # square

                squareIsMarked = any(item.x == row and item.y == col for item in self.markedArray) # itemToLook not in Processor.markedArray
                if squareAtPosition and not squareIsMarked:
                    recursionLevel = 1
                    size = self.getSquareSize(row, col, puzzleModel.puzzle, 1)
                    #size = self.getPossibleSquareSizeWithRecursionLock(row,
                    #col, puzzleModel.puzzle, recursionLevel)
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