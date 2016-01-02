# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        # print "game state", successorGameState
        # print "position", newPos
        # print "food", newFood
        # print "ghost states", newGhostStates
        # print "scared times", newScaredTimes

        "*** YOUR CODE HERE ***"

        #New Food score
        newFoodList = newFood.asList()
        nearest_food = float("inf")
        for foodPos in newFoodList:
          food_dist = util.manhattanDistance(newPos, foodPos)
          nearest_food = min(nearest_food, food_dist)

        #Old Food score
        oldFoodList = currentGameState.getFood().asList()
        food_eaten = len(oldFoodList) - len(newFoodList)

        #New Ghost score
        nearest_ghost = float("inf")
        for ghost in newGhostStates:
          ghostPos = ghost.getPosition()
          ghost_dist = util.manhattanDistance(newPos, ghostPos)
          nearest_ghost = min(nearest_ghost, ghost_dist) 

        if nearest_ghost < 2:
          ghost_score = nearest_ghost
          food_score = 1.0 / nearest_food

        else:
          ghost_score = 20.0
          food_score = 10.0 / nearest_food
        return food_score + ghost_score * food_eaten
        # return successorGameState.getScore()

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
        """
        "*** YOUR CODE HERE ***"

        # returns action associated with max v
        # print self.minimaxDecision(gameState, 0, self.depth)[1]
        return self.minimaxDecision(gameState, 0, self.depth)[1]

        # util.raiseNotDefined()

    def minimaxDecision(self, state, agentIndex, depth):
      if agentIndex == state.getNumAgents():
        agentIndex = 0
        depth -= 1
      if self.terminalTest(state, depth):
        return self.evaluationFunction(state), None
      if agentIndex == 0:
        return self.maxValue(state, agentIndex, depth)
      else:
        return self.minValue(state, agentIndex, depth)

    def maxValue(self, state, agentIndex, depth):
      # if terminalTest(state, depth):
      #   return self.evaluationFunction(state)
      v = float("-inf")
      for action in state.getLegalActions(agentIndex):
        successor = state.generateSuccessor(agentIndex, action)
        newAgentIndex = agentIndex + 1
        value = max((v, None), self.minimaxDecision(successor, newAgentIndex, depth))[0]
        if value != v:
          v = value
          max_action = action
      return (v, max_action)

    def minValue(self, state, agentIndex, depth):
      # if terminalTest(state, depth):
      #   return self.evaluationFunction(state)
      v = float("inf")
      #if agentIndex == state.getNumAgents() - 1:
      #  depth -= 1  
      newAgentIndex = agentIndex + 1
      for action in state.getLegalActions(agentIndex):
          successor = state.generateSuccessor(agentIndex, action)
          value = min((v, None), self.minimaxDecision(successor, newAgentIndex, depth))[0]
          if value != v:
            v = value
            min_action = action
      return (v, min_action)    

    def terminalTest(self, state, depth):
      return depth <= 0 or state.isWin() or state.isLose()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetaDecision(gameState, 0, self.depth, float("-inf"), float("inf"))[1]

        # util.raiseNotDefined()

    def alphaBetaDecision(self, state, agentIndex, depth, alpha, beta):
      if agentIndex == state.getNumAgents():
        agentIndex = 0
        depth -= 1
      if self.terminalTest(state, depth):
        return self.evaluationFunction(state), None
      if agentIndex == 0:
        return self.maxValue(state, agentIndex, depth, alpha, beta)
      else:
        return self.minValue(state, agentIndex, depth, alpha, beta)

    def maxValue(self, state, agentIndex, depth, alpha, beta):
      # if terminalTest(state, depth):
      #   return self.evaluationFunction(state)
      v= float("-inf")
      for action in state.getLegalActions(agentIndex):
        successor = state.generateSuccessor(agentIndex, action)
        newAgentIndex = agentIndex + 1
        value = max((v, None), self.alphaBetaDecision(successor, newAgentIndex, depth, alpha, beta))[0]
        if value != v:
          v = value
          max_action = action
        if v > beta:
          return (v, max_action)
        alpha = max (alpha, v)
      return (v, max_action)

    def minValue(self, state, agentIndex, depth, alpha, beta):
      # if terminalTest(state, depth):
      #   return self.evaluationFunction(state)
      v = float("inf")
      #if agentIndex == state.getNumAgents() - 1:
      #  depth -= 1  
      newAgentIndex = agentIndex + 1
      for action in state.getLegalActions(agentIndex):
          successor = state.generateSuccessor(agentIndex, action)
          value = min((v, None), self.alphaBetaDecision(successor, newAgentIndex, depth, alpha, beta))[0]
          if value != v:
            v = value
            min_action = action
          if v < alpha:
            return (v, min_action)
          beta = min(beta, v)
      return (v, min_action)    

    def terminalTest(self, state, depth):
      return depth <= 0 or state.isWin() or state.isLose()    

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
        return self.expectimaxDecision(gameState, 0, self.depth)[1]

        # util.raiseNotDefined()

    def expectimaxDecision(self, state, agentIndex, depth):
      if agentIndex == state.getNumAgents():
        agentIndex = 0
        depth -= 1
      if self.terminalTest(state, depth):
        return self.evaluationFunction(state), None
      if agentIndex == 0:
        return self.maxValue(state, agentIndex, depth)
      else:
        return self.expValue(state, agentIndex, depth)

    def maxValue(self, state, agentIndex, depth):
      # if terminalTest(state, depth):
      #   return self.evaluationFunction(state)
      v = float("-inf")
      for action in state.getLegalActions(agentIndex):
        successor = state.generateSuccessor(agentIndex, action)
        newAgentIndex = agentIndex + 1
        value = max((v, None), self.expectimaxDecision(successor, newAgentIndex, depth))[0]
        if value != v:
          v = value
          max_action = action
      return (v, max_action)

    def expValue(self, state, agentIndex, depth):
      # if terminalTest(state, depth):
      #   return self.evaluationFunction(state)
      v = 0.0
      #if agentIndex == state.getNumAgents() - 1:
      #  depth -= 1  
      newAgentIndex = agentIndex + 1
      actions = state.getLegalActions(agentIndex)
      p = 1.0 / len(actions)
      for action in actions:
          successor = state.generateSuccessor(agentIndex, action)
          v += p * self.expectimaxDecision(successor, newAgentIndex, depth)[0]
      return (v, None)    

    def terminalTest(self, state, depth):
      return depth <= 0 or state.isWin() or state.isLose()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    curr_food = currentGameState.getFood().asList()
    curr_pac_pos = currentGameState.getPacmanPosition()
    curr_ghosts_states= currentGameState.getGhostStates()
    curr_ghosts_positions = currentGameState.getGhostPositions()
    curr_scared_times = [curr_ghost_state.scaredTimer for  curr_ghost_state in curr_ghosts_states]
    curr_score = currentGameState.getScore()

    FOOD_COEFF = 1.0
    GHOST_COEFF = 1.0
    SCARED_COEFF = 1.0


    nearest_food = float("inf")
    for foodPos in curr_food:
      food_dist = util.manhattanDistance(curr_pac_pos, foodPos)
      nearest_food = min(nearest_food, food_dist)
    food_score = 1.0 / nearest_food

    #Ghost Positions
    nearest_ghost = float("inf")
    for ghost_pos in curr_ghosts_positions:
      ghost_dist = util.manhattanDistance(curr_pac_pos, ghost_pos)
      nearest_ghost = min(nearest_ghost, ghost_dist)

    #Scared Times
    min_scared_time = min(curr_scared_times)

    #Logic
    if nearest_ghost <= 3.0:
      ghost_score = 1.0
      GHOST_COEFF = -100000
    else:
      GHOST_COEFF = 1.0
      ghost_score = 1.0 / nearest_ghost


    if min_scared_time == 0.0:
      scared_score = 1.0
      SCARED_COEFF = -100000
    elif min_scared_time <= 20.0:
      scared_score = 1.0 / min_scared_time
      SCARED_COEFF = 1.0
    else:
      scared_score = 1.0 / min_scared_time
      SCARED_COEFF = 1.0

    #Overall score
    score = curr_score + FOOD_COEFF * food_score + GHOST_COEFF * ghost_score + SCARED_COEFF * scared_score
    return score

    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

