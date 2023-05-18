from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance, euclidean_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
   
    
    #return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1 + min(manhattan_distance(crate, goal) for crate in state.crates for goal in state.layout.goals)
    # The above line passed 2 test cases but with expanding 5667 nodes
    # The below lines passed 2 test cases also but with expanding 4790 nodes
    
    distance: float = 0.0           # distance is at minimum value initially
    
    # looping on the crates and goals to get the furthest crate from the furthest goal
    for crate in state.crates:
        for goal in state.layout.goals:

            # if (distance < manhattan_distance(goal, crate)):
            #     distance = manhattan_distance(goal, crate)
            if (distance < manhattan_distance(goal, crate) + manhattan_distance(crate, state.player)):
                distance = manhattan_distance(goal, crate) + manhattan_distance(crate, state.player)
    
    return distance - 3           # subtracting 3 to make the heuristic at the goal = 0
    
    
