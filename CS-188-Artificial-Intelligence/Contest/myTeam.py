# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'AwesomeAgent', second = 'AwesomeAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class AwesomeAgent(CaptureAgent):
  #Our agent which subclasses CaptureAgent

  def __init__(self, index, timeForComputing = 0.1):
    CaptureAgent.__init__(self, index, timeForComputing)
    self.hmm_list = {}

  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)

    """
    Initialize all variables
    """
    height = gameState.data.layout.height
    width = gameState.data.layout.width
    walls = gameState.data.layout.walls
    curr_state = gameState.getAgentState(self.index)
    curr_pos = gameState.getAgentState(self.index).getPosition()
    us = self.getTeam(gameState)
    them = self.getOpponents(gameState)
    our_food = self.getFoodYouAreDefending(gameState)
    their_food = self.getFood(gameState)
    score = self.getScore(gameState)
    capsules = self.getCapsules(gameState)


    food_grid = self.getFoodYouAreDefending(gameState)
    halfway = food_grid.width / 2
    if self.red:    
      xrange = range(halfway)
    else:       
      xrange = range(halfway, food_grid.width)
    for y in range(food_grid.height):
      for x in xrange:
        food_grid[x][y] = True
    self.our_side = food_grid


    """
    HMM for reading where opponent is
    """
    self.hmm_list = dict([(index, util.Counter()) for 
      index in self.getOpponents(gameState)])
    if self.red:
      self.agentsOnTeam = gameState.getRedTeamIndices()
    else:
      self.agentsOnTeam = gameState.getBlueTeamIndices()
    self.legalPositions = [p for p in gameState.getWalls().asList(False)]
    for dist in self.hmm_list.values():
      # initializes randomly over all positions
      for p in self.legalPositions:
        dist[p] = 1
      dist.normalize()

    #initialize uniformly, somehow


  def chooseAction(self, gameState):

    """
    Utilize an MDP with weights and features to compute optimal action
    from maximal Q-score.
    """

    legal_actions = gameState.getLegalActions(self.index)
    action_values = []
    max_value = float("-inf")
    optimal_action = None
    print legal_actions
    for a in legal_actions:
      print "WTF"
      action_value = self.evaluate(gameState, a)
      print a, action_value
      if (action_value > max_value):
        max_value = action_value
        optimal_action = a
    print optimal_action
    return optimal_action

  def evaluate (self, gameState, action):
    features = self.getFeatures(gameState, action)
    #print features
    weights = self.getWeights(gameState, action)
    scores = features * weights
    return scores

  def getFeatures(self, gameState, action):
    """
    features
    - Distance to Food
    - Distance to power capsules 
    - Distance to home base 

    - Distance to enemy ghosts
    - Distance to enemy scared ghosts 
    - Distance to enemy pacman

    - Current score 
    - Scared time remaining
    - If we're scared
    - How long enemy has been on our side 
    - 
    """

    features = util.Counter()

    height = gameState.data.layout.height
    width = gameState.data.layout.width
    walls = gameState.data.layout.walls
    
    if self.red:
      longitude = width/2 + 1
    else:
      longitude = width/2
    border_positions = [(longitude, i) for i in range(height) if not walls[longitude][i]]

    successor = gameState.generateSuccessor(self.index, action)
    successor_pos = successor.getAgentState(self.index).getPosition()

    successor_capsules = self.getCapsules(successor)

    enemies = self.getOpponents(successor)

    their_food = self.getFood(successor)

    score = self.getScore(successor)

    "Distance to food"
    #food_list = [pos for pos in list(their_food) if their_food[pos[0]][pos[1]]]
    food_list = []
    for y in range(their_food.height):
      for x in range(their_food.width):
        if their_food[x][y]:
          food_list.append((x, y))
    food_distances = [self.getMazeDistance(successor_pos, pos) for pos in food_list]
    closest_food = min(food_distances)

    "Distance to capsules"
    capsules_distances = [self.getMazeDistance(successor_pos, pos) for pos in successor_capsules]
    closest_capsule = min(capsules_distances)

    "Distance to our side"
    if not self.our_side[int(successor_pos[0])][int(successor_pos[1])]:
      our_side_list = []
      for y in range(self.our_side.height):
        for x in range(self.our_side.width):
          if self.our_side[x][y]:
            our_side_list.append((x, y))
      our_side_list = [(x, y) for (x, y) in our_side_list if not walls[x][y]]
      our_side_distances = [self.getMazeDistance(successor_pos, pos) for pos in our_side_list]
      our_side_dist = min(our_side_distances)
    else:
      our_side_dist = 0

    "Attack and defense modes"
    attack_feature = 0
    defense_feature = 0
    enemy_agents = [successor.getAgentState(i) for i in enemies]
    their_attackers = [a for a in enemy_agents if a.isPacman]
    their_defenders = [a for a in enemy_agents if not a.isPacman]

    border_distances = [self.getMazeDistance(successor_pos, pos) for pos in border_positions]
    nearest_border = min(border_distances)

    enemy_positions = [successor.getAgentPosition(a) for a in enemies if successor.getAgentPosition(a) is not None]
    enemy_distances = [self.getMazeDistance(successor_pos, pos) for pos in enemy_positions]
    nearest_enemy = min(enemy_distances) if enemy_distances else 100

    if len(their_attackers) == 2:
      features['borderDistance'] = -100 * nearest_border
      features['enemyDistance'] = -100 * nearest_enemy
      features['foodDistance'] = -1000 * closest_food
      features['capsuleDistance'] = 0
      features['ourSideDistance'] = 0
    else:
      features['borderDistance'] = -10 * nearest_border
      features['enemyDistance'] = -100 * nearest_enemy
      features['foodDistance'] = -1000 * closest_food
      features['capsuleDistance'] = -100 * closest_capsule
      features['ourSideDistance'] = -10 * nearest_border

    return features

  def getWeights(self, gameState, action):
    """
    TODO
    """

    weights = dict()

    weights['foodDistance'] = 1
    weights['capsuleDistance'] = 1
    weights['ourSideDistance'] = 1
    weights['borderDistance'] = 1
    weights['enemyDistance'] = 1

    return weights

    """
    HMM tracking with observe and elapse time.
    """

    # for opponent in self.hmm_list:
    #   self._timeUpdate(gameState, opponent)
    # distributions = self.hmm_list.values()
    # updated_dists = []
    # for dist in distributions:
    #   new_dist = util.Counter()
    #   new_dist[dist.argMax()] = 1
    #   updated_dists.append(new_dist)
    # actions = gameState.getLegalActions(self.index)
    # self.displayDistributionsOverPositions(updated_dists)
    # return random.choice(actions)

  def _timeUpdate(self, gameState, opponent):
    # run forward algorithm time update for opponent positions
    current_position = gameState.getAgentPosition(self.index)
    noisy_distances = gameState.getAgentDistances()
    opponent_position = gameState.getAgentPosition(opponent)
    if opponent_position is not None:
      self.hmm_list[opponent] = util.Counter()
      self.hmm_list[opponent][opponent_position] = 1
      self.hmm_list[opponent].normalize()
      return 
    self._elapseTime(opponent, gameState)
    updated_dist = self.hmm_list[opponent]
    #do observing
    for p in self.legalPositions:
      # the observe step is sketched out below. For now if you run it you
      # just see the P(E|X) distributions laid out on the screen, not anything else.
      trueDistance = util.manhattanDistance(p, current_position)
      #distribution[p] = gameState.getDistanceProb(trueDistance, noisy_distances[opponent])
      updated_dist[p] *= gameState.getDistanceProb(trueDistance, noisy_distances[opponent])
    updated_dist.normalize()
    self.hmm_list[opponent] = updated_dist

  def _elapseTime(self, opponent, gameState):
      # we need to have an elapse time as well as an observe here.
      # elapse time our model for P(X_{t + 1}|X_t) will be that their
      # agent chooses a given direction at random. That should give us 
      # enough accuracy
    current_position = gameState.getAgentPosition(self.index)
    distribution = self.hmm_list[opponent]
    updated_dist = util.Counter()
    for p in self.legalPositions:
      x_coord, y_coord = p
      possible_new_positions = [(x_coord + 1, y_coord), (x_coord - 1, y_coord), (x_coord, y_coord + 1), (x_coord, y_coord - 1)]
      legal_new_positions = [pos for pos in possible_new_positions if pos in self.legalPositions]
      prob = 1.0/len(legal_new_positions)
      for pos in legal_new_positions:
        updated_dist[pos] += prob*distribution[p]
    updated_dist.normalize()
    self.hmm_list[opponent] = updated_dist







class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on). 
    
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    ''' 
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py. 
    '''
    CaptureAgent.registerInitialState(self, gameState)

    ''' 
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    ''' 
    You should change this in your own agent.
    '''

    return random.choice(actions)

