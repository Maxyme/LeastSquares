#!/usr/bin/python
# http://cimpress.com/techchallenge/register/?utm_source=site&utm_medium=registration&utm_campaign=techchallenge
########################################################################
# Cimpress Tech Challenge 2: Covering a grid with squares
# Sample solution by Cimpress (Python).
# Illustrates how to communicate with the Cimpress API server.
########################################################################

import json
import requests

# import Processor
from PuzzleModel import PuzzleModel
from Processor import Processor
from PermutationProcessor import PermutationProcessor

class Solver:
    # CHANGE THIS VALUE
    # Your unique API key obtained when you registered
    # Hard-code this. Use the same key for the entire contest.
    API_KEY = '0ca6c9910de6470895bfbdd0bf5b462a'

    # CHANGE THIS VALUE
    # The environment, either 'trial' for practicing and debugging, or 'contest'
    # for actual submissions that count.
    ENV = 'trial'

    # URL of contest server
    BASE_URL = 'http://techchallenge.cimpress.com'

    # Retrieve a puzzle from the server. Returns JSON.
    def getPuzzle(self):
        url = '{0}/{1}/{2}/puzzle'.format(self.BASE_URL, self.API_KEY, self.ENV)
        return requests.get(url).text

    # Submit the solution. Returns JSON results.
    def submitSolution(self, id, squares):
        url = '{0}/{1}/{2}/solution'.format(self.BASE_URL, self.API_KEY, self.ENV)
        solution = {'id': id, 'squares': squares}
        return requests.post(url, data=json.dumps(solution)).text

# Main program
print('Using API key: {0}'.format(Solver.API_KEY))
s = Solver()

# Get a puzzle, and convert the returned JSON to a Python dictionary

# jsonResult = s.getPuzzle()
# puzzle = json.loads(jsonResult)

# test method from file!
with open('dataSquare4x4.json') as data_file:    
    puzzleJson = json.load(data_file)

# send json into object
puzzle = PuzzleModel(puzzleJson['id'], puzzleJson['width'], puzzleJson['height'], puzzleJson['puzzle'])

# Demonstrate some of the returned values
print('You retrieved a puzzle with {0} width x {1} height and ID={2}'.format(
    puzzle.width,
    puzzle.height,
    puzzle.id))

print('Generating solution')
# squares = s.solve(puzzleJson)

# normal method, works ok..
# -------------------------
#p = Processor()
#squares = p.solve(puzzle)

#squaresAdvanced = p.advancedSolve(puzzle)

#print('Number of squares normal method')
#print(len(squares))

#print('Squares normal method')
#print(squares)

#print('Number of squares advanced method')
#print(len(squaresAdvanced))

#print('Squares advanced method')
#print(squaresAdvanced)

#print('Submitting solution')

# permutation method, testing
# -------------------------
permutationProcessor = PermutationProcessor()

permutationSquareArray = permutationProcessor.getMinimumSquaresArray(puzzle)
print(permutationSquareArray)

# jsonResult = s.submitSolution(puzzle['id'], squares)

# Describe the response

#response = json.loads(jsonResult);
#if len(response['errors']) > 0:
#	print('Your solution failed with {0} problems and used {1} squares.'.format(
#	       len(response['errors']),
#	       response['numberOfSquares']))
#else:
#		print('Your solution succeeded with {0} squares, for a score of {1}, with a time penalty of {2}.'.format(
#	       response['numberOfSquares'],
#	       response['score'],
#	       response['timePenalty']))
