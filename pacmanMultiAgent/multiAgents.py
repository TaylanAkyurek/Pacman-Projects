# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import numpy

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foods = currentGameState.getFood()
        foodList = foods.asList()
       
        distances = []
        if action == Directions.STOP:
            return -9999

        #if there is ghost 
        for state in newGhostStates:
            if newPos == state.getPosition() :
                return -9999
            
        for food in foodList:
            distances.append(manhattanDistance(newPos, food))

        distance = min(distances)
        
        if distance == 0:
            return 9999
        
        #closer too food, better score
        
        distance = 1/ distance
        return distance

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
    
        def value(gameState, currentDepth, agentIndex):
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(gameState), Directions.STOP
            elif agentIndex == 0:
                return maxVal(gameState, agentIndex ,currentDepth)
            else:
                return minVal(gameState,currentDepth,agentIndex)
    
        def maxVal( gameState, agentIndex, currentDepth):
            v = -9999
            
            actions = gameState.getLegalActions(agentIndex)
       
            for action in actions:
                
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents()-1:
                
                 
                    if value(successor, currentDepth + 1, 0)[0] > v:
    
                        v = value(successor, currentDepth + 1, 0)[0]
                        nextAction = action
                else:
                    
                    if  value(successor, currentDepth, agentIndex+1)[0] > v:
                        
                        v = value(successor, currentDepth, agentIndex+1)[0]
                        nextAction = action

            return [v , nextAction]
    
        def minVal(gameState, currentDepth, agentIndex):
            v = 9999
            
            actions = gameState.getLegalActions(agentIndex)
            
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)

                if agentIndex == gameState.getNumAgents()-1:
                    
                    if value(successor, currentDepth + 1, 0)[0] < v:
    
                        v = value(successor, currentDepth + 1, 0)[0]
                        nextAction = action
                else:
                    
                    if  value(successor, currentDepth, agentIndex+1)[0] < v:
                        v = value(successor, currentDepth, agentIndex+1)[0]
                        nextAction = action
                    
            return [v , nextAction]
       
        return value(gameState, 0, 0)[1]
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def value(gameState, currentDepth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(gameState), Directions.STOP
            elif agentIndex == 0:
                return maxVal(gameState, agentIndex ,currentDepth, alpha, beta)
            else:
                return minVal(gameState,currentDepth,agentIndex, alpha, beta)
    
        def maxVal( gameState, agentIndex, currentDepth, alpha, beta):
            v = -9999
            
            actions = gameState.getLegalActions(agentIndex)
       
            for action in actions:
                
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents()-1:
                
                 
                    if value(successor, currentDepth + 1, 0, alpha, beta)[0] > v:
    
                        v = value(successor, currentDepth + 1, 0, alpha, beta)[0]
                        nextAction = action
                else:
                    
                    if  value(successor, currentDepth, agentIndex+1, alpha, beta)[0] > v:
                        
                        v = value(successor, currentDepth, agentIndex+1, alpha, beta)[0]
                        nextAction = action
                if v > beta:
                    nextAction = action
                    return [v , nextAction]
                alpha = max(alpha, v)
                
                
            return [v , nextAction]
    
        def minVal(gameState, currentDepth, agentIndex, alpha, beta):
            v = 9999
            
            actions = gameState.getLegalActions(agentIndex)
            
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)

                if agentIndex == gameState.getNumAgents()-1:
                    
                    if value(successor, currentDepth + 1, 0, alpha, beta)[0] < v:
    
                        v = value(successor, currentDepth + 1, 0, alpha, beta)[0]
                        nextAction = action
                else:
                    
                    if  value(successor, currentDepth, agentIndex+1, alpha, beta)[0] < v:
                        v = value(successor, currentDepth, agentIndex+1, alpha, beta)[0]
                        nextAction = action
                        
                if v < alpha:
                    nextAction = action
                    return [v , nextAction]
                
                beta = min(beta, v)
                    
            return [v , nextAction]
       
        return value(gameState, 0, 0, -999, 999)[1]
    
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def value(gameState, currentDepth, agentIndex):
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(gameState), Directions.STOP
            elif agentIndex == 0:
                return maxVal(gameState, agentIndex ,currentDepth)
            else:
                return minVal(gameState,currentDepth,agentIndex)
    
        def maxVal( gameState, agentIndex, currentDepth):
            v = -9999
            
            actions = gameState.getLegalActions(agentIndex)
       
            for action in actions:
                
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents()-1:
                
                 
                    if value(successor, currentDepth + 1, 0)[0] > v:
    
                        v = value(successor, currentDepth + 1, 0)[0]
                        nextAction = action
                else:
                    
                    if  value(successor, currentDepth, agentIndex+1)[0] > v:
                        
                        v = value(successor, currentDepth, agentIndex+1)[0]
                        nextAction = action

            return [v , nextAction]
    
        def minVal(gameState, currentDepth, agentIndex):
            v = 0
            
            actions = gameState.getLegalActions(agentIndex)
            
            p = 1 / (len(gameState.getLegalActions(agentIndex)))
            
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)

                if agentIndex == gameState.getNumAgents()-1:
                        
                    val = value(successor, currentDepth + 1, 0)[0]
                    v = v + p * val
                    nextAction = action
                else:
                    val = value(successor, currentDepth, agentIndex+1)[0]
                    v = v + p * val
                    nextAction = action
                    
            return [v , nextAction]
       
        return value(gameState, 0, 0)[1]
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)

    newPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    foodList = foods.asList()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    capsules = currentGameState.getCapsules() 
    
    foodDistances = []
    ghostDistances = []
    capsuleDistances = []
    total = 0
    total += 10 * currentGameState.getScore()
    
    
    for state in newGhostStates:
        if newPos == state.getPosition() and state.scaredTimer :
            return 9999
        elif newPos == state.getPosition() and not state.scaredTimer:
            return -9999
        elif newPos != state.getPosition() and not state.scaredTimer:
            ghostDistances.append(manhattanDistance(newPos, state.getPosition()))
            
            
    for food in foodList:
        foodDistances.append(manhattanDistance(newPos, food))
    
    for capsule in capsules:
        capsuleDistances.append(manhattanDistance(newPos, capsule))
    
    if not foodDistances:
        return 9999
    
    else:
        
        total += 10/min(foodDistances)
    
    if ghostDistances:
        total += 3/ min(ghostDistances)
        
    if capsuleDistances:
        total += 20/ min(capsuleDistances)
    
    
                                                                                                                                                
    return total
# Abbreviation
better = betterEvaluationFunction
