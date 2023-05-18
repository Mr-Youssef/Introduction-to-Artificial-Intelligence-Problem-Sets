from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    playerTurn = game.get_turn(state)           # 0 for player, >0 for enemy
    terminal, values = game.is_terminal(state)  # terminal is a boolean, values is a list of values for all agents
    if terminal: return (values[0], None)       # return value for the player (which acts at the max nodes), and no action
    if (max_depth == 0): return (heuristic(game, state, 0), None) # return heuristic value for the player, and no action when max depth is reached

    if (playerTurn == 0):                       # for my player turn
        maxVal = float('-inf')                  # set maxVal to negative infinity for initialization
        bestAction = None                       # set bestAction to None for initialization
        for action in game.get_actions(state):  # for each action in the list of actions
            successor = game.get_successor(state, action)   # get the successor state
            value, _ = minimax(game, successor, heuristic, max_depth-1)  # recursively call minimax on the successor state
            if (value > maxVal):                # if the value is greater than the max value, update the max value and best action
                maxVal = value
                bestAction = action
        return (maxVal, bestAction)             # return the max value and the best action
    
    else:                                       # for enemy's turn
        minVal = float('inf')                   # set minVal to positive infinity for initialization 
        bestAction = None                       # set bestAction to None for initialization
        for action in game.get_actions(state):  # for each action in the list of actions
            successor = game.get_successor(state, action)   # get the successor state
            value, _ = minimax(game, successor, heuristic, max_depth-1)  # recursively call minimax on the successor state
            if (value < minVal):                # if the value is less than the min value, update the min value and best action
                minVal = value
                bestAction = action
        return (minVal, bestAction)             # return the min value and the best action
    

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha = float('-inf'), beta = float('inf')) -> Tuple[float, A]:
    #TODO: Complete this function
    playerTurn = game.get_turn(state)           # 0 for player, >0 for enemy
    terminal, values = game.is_terminal(state)  # terminal is a boolean, values is a list of values for all agents
    if terminal: return (values[0], None)       # return value for the player (which acts at the max nodes), and no action
    if (max_depth == 0): return (heuristic(game, state, 0), None) # return heuristic value for the player, and no action when max depth is reached

    if (playerTurn == 0):                       # for my player turn
        maxVal = float('-inf')                  # set maxVal to negative infinity for initialization
        bestAction = None                       # set bestAction to None for initialization
        for action in game.get_actions(state):  # for each action in the list of actions
            successor = game.get_successor(state, action)   # get the successor state
            value, _ = alphabeta(game, successor, heuristic, max_depth-1, alpha, beta)  # recursively call alphabeta on the successor state
            # Note: when calling alphabeta, alpha and beta have to be passed in as parameters, 
            # otherwise they will be reset to -inf and inf which is not what we want

            if (value > maxVal):                # if the value is greater than the max value, update the max value and best action
                maxVal = value
                bestAction = action
            if (value > alpha):                 # if the value is greater than alpha, save the new alpha
                alpha = value
            if (alpha >= beta):                 # if alpha is greater than or equal beta, prune the rest of the tree
                break
        return (maxVal, bestAction)             # return the max value and the best action after pruning
    
    else:                                       # for enemy's turn
        minVal = float('inf')                   # set minVal to positive infinity for initialization
        bestAction = None                       # set bestAction to None for initialization
        for action in game.get_actions(state):  # for each action in the list of actions
            successor = game.get_successor(state, action)   # get the successor state
            value, _ = alphabeta(game, successor, heuristic, max_depth-1, alpha, beta)  # recursively call alphabeta on the successor state
            # Note: when calling alphabeta, alpha and beta have to be passed in as parameters, 
            # otherwise they will be reset to -inf and inf which is not what we want

            if (value < minVal):                # if the value is less than the min value, update the min value and best action
                minVal = value
                bestAction = action
            if (value < beta):                  # if the value is less than beta, save the new beta
                beta = value
            if (alpha >= beta):                 # if alpha is greater than or equal beta, prune the rest of the tree
                break
        return (minVal, bestAction)             # return the min value and the best action after pruning

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha = float('-inf'), beta = float('inf')) -> Tuple[float, A]:
    #TODO: Complete this function
    playerTurn = game.get_turn(state)           # 0 for player, >0 for enemy
    terminal, values = game.is_terminal(state)  # terminal is a boolean, values is a list of values for all agents
    if terminal: return (values[0], None)       # return value for the player (which acts at the max nodes), and no action
    if (max_depth == 0): return (heuristic(game, state, 0), None) # return heuristic value for the player, and no action when max depth is reached

    # move ordering part
    sortedActions = []                          # create a list to store sorted actions, 
                                                # it will be a list of tuples (heuristic value, action) 
                                                # to sort the actions based on heuristic value
    for action in game.get_actions(state):      # for each action in the list of actions
        sortedActions.append((heuristic(game, game.get_successor(state, action), playerTurn), action)) # append the heuristic value and action to the list as a tuple
    sortedActions.sort(reverse = True, key = lambda x : x[0])  # sort the list of tuples based on heuristic value in descending order

    if (playerTurn == 0):                       # for my player turn
        maxVal = float('-inf')                  # set maxVal to negative infinity for initialization
        bestAction = None                       # set bestAction to None for initialization
        for _,action in sortedActions:          # for each action in the list of actions after sorting
            successor = game.get_successor(state, action)   # get the successor state
            value, _ = alphabeta_with_move_ordering(game, successor, heuristic, max_depth-1, alpha, beta)  # recursively call alphabeta_with_move_ordering on the successor state
            # Note: when calling alphabeta_with_move_ordering, alpha and beta have to be passed in as parameters, 
            # otherwise they will be reset to -inf and inf which is not what we want

            if (value > maxVal):                # if the value is greater than the max value, update the max value and best action
                maxVal = value
                bestAction = action
            if (value > alpha):                 # if the value is greater than alpha, save the new alpha
                alpha = value
            if (alpha >= beta):                 # if alpha is greater than or equal beta, prune the rest of the tree
                break
        return (maxVal, bestAction)             # return the max value and the best action after pruning
    
    else:                                       # for enemy's turn
        minVal = float('inf')                   # set minVal to positive infinity for initialization
        bestAction = None                       # set bestAction to None for initialization
        for _,action in sortedActions:            # for each action in the list of sorted actions
            successor = game.get_successor(state, action)   # get the successor state
            value, _ = alphabeta_with_move_ordering(game, successor, heuristic, max_depth-1, alpha, beta)  # recursively call alphabeta_with_move_ordering on the successor state
            # Note: when calling alphabeta_with_move_ordering, alpha and beta have to be passed in as parameters, 
            # otherwise they will be reset to -inf and inf which is not what we want

            if (value < minVal):                # if the value is less than the min value, update the min value and best action
                minVal = value
                bestAction = action
            if (value < beta):                  # if the value is less than beta, save the new beta
                beta = value
            if (alpha >= beta):                 # if alpha is greater than or equal beta, prune the rest of the tree
                break
        return (minVal, bestAction)             # return the min value and the best action after pruning


# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    playerTurn = game.get_turn(state)           # 0 for player, >0 for enemy
    terminal, values = game.is_terminal(state)  # terminal is a boolean, values is a list of values for all agents
    if terminal: return (values[0], None)       # return value for the player (which acts at the max nodes), and no action
    if (max_depth == 0): return (heuristic(game, state, 0), None) # return heuristic value for the player, and no action when max depth is reached

    if (playerTurn == 0):                       # for my player turn
        maxVal = float('-inf')                  # set maxVal to negative infinity for initialization
        bestAction = None                       # set bestAction to None for initialization
        for action in game.get_actions(state):  # for each action in the list of actions
            successor = game.get_successor(state, action)   # get the successor state
            value, _ = expectimax(game, successor, heuristic, max_depth-1)  # recursively call expectimax on the successor state
            if (value > maxVal):                # if the value is greater than the max value, update the max value and best action
                maxVal = value
                bestAction = action
        return (maxVal, bestAction)             # return the max value and the best action
    
    else:                                       # for enemy's turn
        # Note: the enemy acts randomly, so we need to calculate the average value of all possible actions
        sumVal = 0                              # set sumVal to 0 for initialization
        bestAction = None                       # set bestAction to None for initialization
        for action in game.get_actions(state):  # for each action in the list of actions
            successor = game.get_successor(state, action)   # get the successor state
            value, _ = expectimax(game, successor, heuristic, max_depth-1)  # recursively call expectimax on the successor state
            sumVal += value                     # add the value to the sum value
        return (sumVal/len(game.get_actions(state)), bestAction)  # return the average value and the best action
    