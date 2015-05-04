from ItemModel import ItemModel

class PermutationProcessor:
    markedArray = []
    tempSizeArray = []

    def getAllPermutation(self, puzzleModel):
        permutationArray = []
        for row in range(0, puzzleModel.height):
            for col in range(0, puzzleModel.width):

                squareAtPosition = puzzleModel.puzzle[row][col]
                if squareAtPosition:
                    #resetArray
                    self.tempSizeArray = []
                    sizeArray = self.getSquareSize(row, col, puzzleModel.puzzle, 1)

                    itemToLook = ItemModel(row, col)
                    permutationArray.append({'Item': itemToLook, 'SizeArray': sizeArray})

        return permutationArray

    def tryAllPermutation(self, puzzleModel):
        permutationArray = []
        for row in range(0, puzzleModel.height):
            for col in range(0, puzzleModel.width):

                squareAtPosition = puzzleModel.puzzle[row][col]
                if squareAtPosition:
                    #resetArray
                    self.tempSizeArray = []
                    sizeArray = self.getSquareSize(row, col, puzzleModel.puzzle, 1)

                    itemToLook = ItemModel(row, col)
                    permutationArray.append({'Item': itemToLook, 'SizeArray': sizeArray})

        return permutationArray


    def getSquareSize(self, itemXpos, itemYpos, itemArray, recursionLevel):
        # add to temp size array
        self.tempSizeArray.append(recursionLevel**2)
        
        # Check if all the neighbours for the recursion level are squares and inside the itemArray
        neighboursArray = self.getNeighbours(itemXpos, itemYpos, itemArray, recursionLevel)

        # If all are inside, add to marked array and try again at a higher recursion level
        if self.checkNeighbours(neighboursArray, itemArray):
            # add to marked items array
            self.markedArray.extend(neighboursArray)


            # recursion of method
            return self.getSquareSize(itemXpos, itemYpos, itemArray, recursionLevel + 1)


        # else, return the square of the last recursion level
        else:
            return self.tempSizeArray # recursionLevel**2
    
        # make an array of the possible items based on recursion level.
    def getNeighbours(self, itemX, itemY, puzzleArray, recursionLevel):
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
    def checkNeighbours(self, neighboursArray, puzzleArray):
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
                #squareIsMarked = any(marked.x == item.x and marked.y == item.y for marked in self.markedArray)
                #if not isSquare or squareIsMarked:
                #    return False
                # return isSquare
            except IndexError:
                # break
                return False

        return True
