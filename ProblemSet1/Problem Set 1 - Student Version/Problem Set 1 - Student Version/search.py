from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq
from queue import LifoQueue

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    
    # Here we check if the initial state is the goal state
    if problem.is_goal(initial_state):
        return None
    frontier = deque() # This is a queue which is used to store the frontier states, we use a deque for O(1) pop and append operations
    frontier_for_fastSearch = set()  # This is a set which is used to check if a state is in the frontier in O(1)
    frontier.append(initial_state)
    frontier_for_fastSearch.add(initial_state)
    explored = set()
    childTOparent = {}  # We later use this dict to reconstruct the path, its key is the child and its value is a tuple of the parent and the action taken to get from parent to child
    pathSolution = []   # This list of actions will contain the solution path which we will return
    while (len(frontier) > 0):  # While the frontier is not empty
        node = frontier.popleft()
        frontier_for_fastSearch.remove(node)
        explored.add(node)  # since the node is expanded, we add it to the explored set
        for action in problem.get_actions(node):  # For each action in the actions list of this node, we loop to do all the available actions of this node
            successorChild = problem.get_successor(node, action)
            if successorChild not in explored and successorChild not in frontier_for_fastSearch: # If the child is not in the explored set and not in the frontier set
                childTOparent[successorChild] = (node, action)  # We save the parent and the action taken to get from parent to child for backtracking purposes
                if problem.is_goal(successorChild):  # Note: we make the goal test BEFORE adding the child to the frontier

                    # Here we backtrack to reconstruct the path from the initial state to the goal state when we reacch the goal state
                    while successorChild != initial_state:
                        pathSolution.append(childTOparent[successorChild][1]) # We append the action taken to get from parent to child
                        successorChild = childTOparent[successorChild][0] # We update the child to be the parent of the previous child
                    return pathSolution[::-1]  # We return the reversed pathSolution list which is the path from the initial state to the goal state as the pathSolution list is in reverse order
                
                # if the child is not the goal state, we add it to the frontier
                frontier.append(successorChild)
                frontier_for_fastSearch.add(successorChild)
    return None

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # Here we check if the initial state is the goal state
    if problem.is_goal(initial_state):
        return None
    
    frontier = LifoQueue() # This is a stack which is used to store the frontier states, we use a LifoQueue for O(1) pop and append operations
    frontier_for_fastSearch = set() # This is a set which is used to check if a state is in the frontier in O(1)
    frontier.put(initial_state)
    frontier_for_fastSearch.add(initial_state)
    explored = set()
    childTOparent = {}  # We later use this dict to reconstruct the path, its key is the child and its value is a tuple of the parent and the action taken to get from parent to child
    pathSolution = []   # This list of actions will contain the solution path which we will return
    while (not frontier.empty()): # While the frontier is not empty
        node = frontier.get()
        frontier_for_fastSearch.remove(node)
        explored.add(node)  # since the node is expanded, we add it to the explored set
        if problem.is_goal(node):  # Note: we make the goal test AFTER removing the node from the frontier
            # Here we backtrack to reconstruct the path from the initial state to the goal state when we reacch the goal state
            while node != initial_state:
                pathSolution.append(childTOparent[node][1])  # We append the action taken to get from parent to child
                node = childTOparent[node][0]  # We update the child to be the parent of the previous child
            return pathSolution[::-1]  # We return the reversed pathSolution list which is the path from the initial state to the goal state as the pathSolution list is in reverse order
        
        for action in problem.get_actions(node):  # For each action in the actions list of this node, we loop to do all the available actions of this node
            successorChild = problem.get_successor(node, action)
            if successorChild not in explored and successorChild not in frontier_for_fastSearch:# If the child is not in the explored set and not in the frontier set
                childTOparent[successorChild] = (node, action)  # We save the parent and the action taken to get from parent to child for backtracking purposes
                # Since the child is not the goal state, we add it to the frontier
                frontier.put(successorChild)
                frontier_for_fastSearch.add(successorChild)
    return None
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    node = (0, 0, initial_state) # The node is a tuple of the path cost as the 1st priority, a 2nd priority which the heapq uses when there are 2 nodes of equal path costs, and the state
    
    # Here we check if the initial state is the goal state
    if problem.is_goal(initial_state):
        return None
    
    priority2 = 0
    frontier = []
    heapq.heappush(frontier, node) # This is a priority queue which is used to store the frontier states, we use a heapq for O(log(n)) push and pop operations
    frontier_for_fastSearch = set() # This is a set which is used to check if a state is in the frontier in O(1)
    frontier_for_fastSearch.add(initial_state)
    explored = set()
    childTOparent = {}  # We later use this dict to reconstruct the path, its key is the child and its value is a tuple of the parent and the action taken to get from parent to child
    pathSolution = []   # This list of actions will contain the solution path which we will return
    while (len(frontier) > 0):  # While the frontier is not empty
        node = heapq.heappop(frontier)
        frontier_for_fastSearch.remove(node[2])
        if problem.is_goal(node[2]):    # Note: we make the goal test AFTER removing the node from the frontier
            # Here we backtrack to reconstruct the path from the initial state to the goal state when we reacch the goal state
            while node[2] != initial_state:
                pathSolution.append(childTOparent[node[2]][1])  # We append the action taken to get from parent to child
                temp = childTOparent[node[2]][0]  # We update the child to be the parent of the previous child
                node = (0, 0, temp)
            return pathSolution[::-1]  # We return the reversed pathSolution list which is the path from the initial state to the goal state as the pathSolution list is in reverse order
        
        explored.add(node[2])  
        for action in problem.get_actions(node[2]):  # For each action in the actions list of this node, we loop to do all the available actions of this node
            successorChild = problem.get_successor(node[2], action)

            child_cost = problem.get_cost(node[2], action)
            accumulative_cost = node[0] + child_cost # The accumulative cost is the path cost of the parent plus the cost of the action taken to get to the child
            
            if successorChild not in explored and successorChild not in frontier_for_fastSearch:  # If the child is not in the explored set and not in the frontier set
                childTOparent[successorChild] = (node[2], action)  # We save the parent and the action taken to get from parent to child for backtracking purposes
                priority2 += 1  # We increment the 2nd priority to make sure that the heapq does not remove the node with the same path cost as the current node
                
                # Since the child is not the goal state, we add it to the frontier
                heapq.heappush(frontier, (accumulative_cost, priority2, successorChild))
                frontier_for_fastSearch.add(successorChild)

            elif successorChild in frontier_for_fastSearch:
                for i in range(len(frontier)):
                    # In case a better path is found to a node in the frontier, we have to replace it with the current node
                    if frontier[i][2] == successorChild:
                        if frontier[i][0] > accumulative_cost:
                            childTOparent[successorChild] = (node[2], action)
                            frontier[i] = (accumulative_cost, frontier[i][1], successorChild)
                            heapq.heapify(frontier)
                        break

    return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    node = (0, 0, initial_state)  # The node is a tuple of the path cost as the 1st priority, a 2nd priority which the heapq uses when there are 2 nodes of equal path costs, and the state
    
    # Here we check if the initial state is the goal state
    if problem.is_goal(initial_state):
        return None
    
    priority2 = 0
    frontier = []
    heapq.heappush(frontier, node)  # This is a priority queue which is used to store the frontier states, we use a heapq for O(log(n)) push and pop operations
    frontier_for_fastSearch = set() # This is a set which is used to check if a state is in the frontier in O(1)
    frontier_for_fastSearch.add(initial_state)
    explored = set()
    childTOparent = {}  # We later use this dict to reconstruct the path, its key is the child and its value is a tuple of the parent and the action taken to get from parent to child
    pathSolution = []   # This list of actions will contain the solution path which we will return
    while (len(frontier) > 0):  # While the frontier is not empty
        node = heapq.heappop(frontier)
        frontier_for_fastSearch.remove(node[2])
        if problem.is_goal(node[2]):    # Note: we make the goal test AFTER removing the node from the frontier
            # Here we backtrack to reconstruct the path from the initial state to the goal state when we reacch the goal state
            while node[2] != initial_state:
                pathSolution.append(childTOparent[node[2]][1])  # We append the action taken to get from parent to child
                temp = childTOparent[node[2]][0]  # We update the child to be the parent of the previous child
                node = (0, 0, temp)
            return pathSolution[::-1]  # We return the reversed pathSolution list which is the path from the initial state to the goal state as the pathSolution list is in reverse order
        
        explored.add(node[2])
        for action in problem.get_actions(node[2]):  # For each action in the actions list of this node, we loop to do all the available actions of this node
            successorChild = problem.get_successor(node[2], action)

            child_cost = problem.get_cost(node[2], action)
            accumulative_cost = node[0] + child_cost  # The accumulative cost is the path cost of the parent plus the cost of the action taken to get to the child
            heuristic_cost = heuristic(problem, successorChild) - heuristic(problem, node[2])  # The heuristic cost is the heuristic value of the child minus the heuristic value of the parent as it is not accumulative
            total_cost = accumulative_cost + heuristic_cost  # The total cost is the accumulative path cost + the heuristic cost

            if successorChild not in explored and successorChild not in frontier_for_fastSearch:  # If the child is not in the explored set and not in the frontier set
                childTOparent[successorChild] = (node[2], action)  # We save the parent and the action taken to get from parent to child for backtracking purposes
                priority2 += 1  # We increment the 2nd priority to make sure that the heapq does not remove the node with the same path cost as the current node
                
                # Since the child is not the goal state, we add it to the frontier
                heapq.heappush(frontier, (total_cost, priority2, successorChild))
                frontier_for_fastSearch.add(successorChild)

            elif successorChild in frontier_for_fastSearch:
                for i in range(len(frontier)):
                    # In case a better path is found to a node in the frontier, we have to replace it with the current node
                    if frontier[i][2] == successorChild:
                        if frontier[i][0] > total_cost:
                            childTOparent[successorChild] = (node[2], action)
                            frontier[i] = (total_cost, frontier[i][1], successorChild)
                            heapq.heapify(frontier)
                        break

    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    node = (0, 0, initial_state)  # The node is a tuple of the path cost as the 1st priority, a 2nd priority which the heapq uses when there are 2 nodes of equal path costs, and the state
    
    # Here we check if the initial state is the goal state
    if problem.is_goal(initial_state):
        return None
    
    priority2 = 0
    frontier = []
    heapq.heappush(frontier, node)  # This is a priority queue which is used to store the frontier states, we use a heapq for O(log(n)) push and pop operations
    frontier_for_fastSearch = set() # This is a set which is used to check if a state is in the frontier in O(1)
    frontier_for_fastSearch.add(initial_state)
    explored = set()
    childTOparent = {}  # We later use this dict to reconstruct the path, its key is the child and its value is a tuple of the parent and the action taken to get from parent to child
    pathSolution = []   # This list of actions will contain the solution path which we will return
    while (len(frontier) > 0):  # While the frontier is not empty
        node = heapq.heappop(frontier)
        frontier_for_fastSearch.remove(node[2])
        if problem.is_goal(node[2]):    # Note: we make the goal test AFTER removing the node from the frontier
            # Here we backtrack to reconstruct the path from the initial state to the goal state when we reacch the goal state
            while node[2] != initial_state:
                pathSolution.append(childTOparent[node[2]][1])  # We append the action taken to get from parent to child
                temp = childTOparent[node[2]][0]  # We update the child to be the parent of the previous child
                node = (0, 0, temp)
            return pathSolution[::-1]  # We return the reversed pathSolution list which is the path from the initial state to the goal state as the pathSolution list is in reverse order
        
        explored.add(node[2])
        for action in problem.get_actions(node[2]):  # For each action in the actions list of this node, we loop to do all the available actions of this node
            successorChild = problem.get_successor(node[2], action)  

            heuristic_cost = heuristic(problem, successorChild)
            total_cost = heuristic_cost  # The total cost is equal to the heuristic cost only for Greedy Best First Search

            if successorChild not in explored and successorChild not in frontier_for_fastSearch:  # If the child is not in the explored set and not in the frontier set
                childTOparent[successorChild] = (node[2], action)  # We save the parent and the action taken to get from parent to child for backtracking purposes
                priority2 += 1  # We increment the 2nd priority to make sure that the heapq does not remove the node with the same path cost as the current node
                
                # Since the child is not the goal state, we add it to the frontier
                heapq.heappush(frontier, (total_cost, priority2, successorChild))
                frontier_for_fastSearch.add(successorChild)

    return None