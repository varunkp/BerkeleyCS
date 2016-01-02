# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action

        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

class SearchNode(object):

  def __init__(self, state, action, cost, parent):
    self.state = state
    self.action = action
    self.cost = cost
    self.parent = parent

  def retraceActionList(self):
    if not self.parent:
      return []
    return self.parent.retraceActionList() + [self.action]
      
def AStarNode(SearchNode):

  def __init__(self, state, action, cost, parent, heuristic_cost):
    super(AStarNode, self).__init__(state, action, cost, parent)
    self.heuristic_cost = heuristic_cost

def searchWithoutPriority(problem, data_struct):
    start_state = problem.getStartState()
    fringe = data_struct()
    explored_set = set()
    fringe.push(SearchNode(start_state, None, 0, None)) #node logic

    while not fringe.isEmpty():
      current_node = fringe.pop()
      current_state = current_node.state
      if problem.isGoalState(current_state):
        return current_node.retraceActionList()
      if current_state in explored_set:
        continue
      explored_set.add(current_state)
      for successor, action, cost in problem.getSuccessors(current_state):
        successor_node = SearchNode(successor, action, cost, current_node)
        fringe.push(successor_node)
    return None

def depthFirstSearch(problem):
  return searchWithoutPriority(problem, util.Stack)


def breadthFirstSearch(problem):
  return searchWithoutPriority(problem, util.Queue)


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    fringe = util.PriorityQueue()
    explored_set = set()
    cost = 0
    fringe.push(SearchNode(problem.getStartState(), None, cost, None), cost)
    while not fringe.isEmpty():
      current_node = fringe.pop()
      current_state = current_node.state
      if problem.isGoalState(current_state):
        return current_node.retraceActionList()
      if current_state in explored_set:
        continue
      explored_set.add(current_state)
      for successor, action, step_cost in problem.getSuccessors(current_state):
        updated_cost = current_node.cost + step_cost
        new_node = SearchNode(successor, action, updated_cost, current_node)
        fringe.push(new_node, updated_cost)
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    explored_set = set()
    cost = 0
    start_state = problem.getStartState()
    fringe.push(
        SearchNode(start_state, None, cost, None), 
        heuristic(start_state, problem))
    #fringe.push((problem.getStartState(), [], cost, heuristic(problem.getStartState(), problem)), cost)
    while not fringe.isEmpty():
      #state, moves_so_far, cost_so_far, _ = fringe.pop()
      current_node = fringe.pop()
      current_state = current_node.state
      if current_state in explored_set:
        continue
      explored_set.add(current_state)
      if problem.isGoalState(current_state):
        return current_node.retraceActionList()
      for successor, action, step_cost in problem.getSuccessors(current_state):
        updated_cost = current_node.cost + step_cost
        new_node = SearchNode(
            successor, 
            action, 
            updated_cost,
            current_node)
        fringe.push(new_node, updated_cost + heuristic(successor, problem))
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
