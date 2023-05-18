from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]       # A tuple of points where state[i] is the position of car 'i'.

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the slot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        return self.cars    # The initial state is the tuple of positions of all the cars.
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        # Here we loop on the states (cars) and check if the state is not in the goal slot 
        # or if the index of the state is not the same as the index of the slot to check whether the car is in the right slot (its slot) or not
        # if one of the 2 conditions is met, we return false, otherwise if both are not met we return true
        for i in range(len(state)):
            if state[i] not in self.slots or self.slots.get(state[i]) != i:
                return False
            else:
                return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        actions = []
        # We loop on the state (cars) and also loop on the direction to get all possible actions, 
        # then check if the car can move in a direction or not (remeber passages contain all the possible paths available to move in),
        # also we have to check if the car is not in the same position as another car (if it is, it means that the car can't move in that direction)  
        # if both conditions are satisfied, we add this action to the list of actions
        for i in range(len(state)):
            for d in Direction:
                if state[i] + d.to_vector() in self.passages and state[i] + d.to_vector() not in state:
                    actions.append((i, d))  # We append the action as a tuple of the index of the car and the direction
        return actions
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        temp = list(state)    # Here we used temp list as state is a tuple and we can't change the values of a tuple
        temp[action[0]] = temp[action[0]].__add__(action[1].to_vector())   # where action[0] is the index of the car and action[1] is the direction this car should take
        return tuple(temp)
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE
        new_state = state[action[0]].__add__(action[1].to_vector())   
        # new_state is the new position of the car after taking the action (the successor state)
        # if the new state is in the slots and the index of the slot is not the same as the index of the car, we return 26 - action[0] + 100
        # this check is to know whether the car moved to another car's slot or not
        # 26 - action[0] : action[0] is the index of the car and we want to give a higher cost to the car with a higher index
        # so car A (index 0) will have cost of 26, car B (index 1) will have cost of 25, and so on
        # 100 : this is to give a higher cost to the car that moved to another car's slot
        if  new_state in self.slots and self.slots.get(new_state) != action[0]:
            return 26 - action[0] + 100
        else:
            return 26 - action[0]
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
