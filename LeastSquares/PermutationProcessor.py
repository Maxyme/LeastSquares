from ItemModel import ItemModel
from Processor import Processor

class PermutationProcessor:
    tempSizeArray = []
    
    def getMinimumSquaresArray(self, puzzleModel):
        # get permutation array
        permutationArray = self.getAllPermutation(puzzleModel)
        
        # get all possible arrays
        ListOfPossibleSolutions = self.tryAllPermutation(puzzleModel, permutationArray)
        
        # pick the smallest array and return
        minimumSquaresArray = []
        if len(ListOfPossibleSolutions) > 0:
            minimumSquaresArray = min(ListOfPossibleSolutions, key=len)

        return minimumSquaresArray

    # returns a array with all items and their possible square size
    def getAllPermutation(self, puzzleModel):
        processor = Processor()

        permutationArray = []
        for row in range(0, puzzleModel.height):
            for col in range(0, puzzleModel.width):
                squareAtPosition = puzzleModel.puzzle[row][col]
                if squareAtPosition:
                    #resetArray
                    self.tempSizeArray = []
                    sizeArray = self.getPossibleSquareSize(row, col, puzzleModel.puzzle, 1)

                    itemToLook = ItemModel(row, col)
                    permutationArray.append({'Item': itemToLook, 'SizeArray': sizeArray})

        return permutationArray

    # returns list of array for all possible combinations 
    def tryAllPermutation(self, puzzleModel, permutationArray):

        ListOfPossibleSolutions = []
        processor = Processor()

        #iterate all possible combinations
        combinationItem = processor.advancedSolve(puzzleModel)

        listOfCombinations.append(combinationItem)
        return ListOfPossibleSolutions 

    # Get the possible recursion level, or square side of each item
    def getPossibleSquareSize(self, itemXpos, itemYpos, itemArray, recursionLevel):
        # add to temp size array
        # self.tempSizeArray.append(recursionLevel**2)
        self.tempSizeArray.append(recursionLevel)
        
        # Check if all the neighbours for the recursion level are squares and inside the itemArray
        processor = Processor()
        neighboursArray = processor.getNeighbours(itemXpos, itemYpos, itemArray, recursionLevel)

        # If all are inside, add to marked array and try again at a higher recursion level
        if self.checkPossibleNeighbours(neighboursArray, itemArray):
            # recursion of method
            return self.getPossibleSquareSize(itemXpos, itemYpos, itemArray, recursionLevel + 1)

        # else, return the array of possible sizes
        else:
            return self.tempSizeArray
    
     # make an array of the possible items based on recursion level.
    def getPossibleNeighbours(self, itemX, itemY, puzzleArray, recursionLevel):
        neighboursArray = []

        # Find the number of neighbours for the recursion level: recursionLevel*2 - 1
        numNeighbours = recursionLevel*2 + 1

        # get right neighbour items
        for i in range(recursionLevel):
            rightItem =  ItemModel(itemX + recursionLevel, itemY + i)
            neighboursArray.append(rightItem)

        # get bottom neighbour items
        for i in range(recursionLevel):
            underItem =  ItemModel(itemX + i, itemY + recursionLevel)
            neighboursArray.append(underItem)

        # get bottom corner item
        bottomCornerItem =  ItemModel(itemX + recursionLevel, itemY + recursionLevel)
        neighboursArray.append(bottomCornerItem)

        # return the array
        return neighboursArray

    # Checks the neighbours to see if they are true and inside the array
    def checkPossibleNeighbours(self, neighboursArray, puzzleArray):
        # simple check
        if len(neighboursArray) <= 0:
            return False

        # iterate all the items to see if they exists and are true and not already used in another square (marked)
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
