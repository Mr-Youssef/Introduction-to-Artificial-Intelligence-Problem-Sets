from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function
    for constraint in problem.constraints:           # for each constraint in the problem
        if isinstance(constraint, BinaryConstraint) and assigned_variable in constraint.variables:  # if the constraint is binary and involve the assigned variable
            # Get the other involved variable. 
            other_variable = constraint.get_other(assigned_variable)
            if not domains.get(other_variable):      # If the other variable has no domain (in other words, it is already assigned)
                continue                             # skip this constraint
            # Note: don't use domains[other_variable] above because it will throw an error when running cryptarithmatic if the other variable 
            # doesn't exit, use domains.get(other_variable) instead as it will return None if the other variable doesn't exit

            # Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
            domains[other_variable] = {value for value in domains[other_variable] if constraint.is_satisfied({assigned_variable:assigned_value, other_variable:value})}  

            if not domains.get(other_variable):      # If the other variable's domain becomes empty, return False
                return False    
    return True


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function
    
    # create a copy of the domains
    domains_copy = domains.copy()
    # create a list of tuples (value, number of values that don't satisfy the binary constraint with the assigned variable)
    lst = []

    # for each value in the domain of the variable to assign
    for value in domains_copy.get(variable_to_assign):
        count = 0                                    # initialize the number of values that satisfy the binary constraint with the assigned variable to 0
        for constraint in problem.constraints:       # for each constraint in the problem
            if isinstance(constraint, BinaryConstraint) and variable_to_assign in constraint.variables:  # if the constraint is binary and involve the assigned variable
                # Get the other involved variable. 
                other_variable = constraint.get_other(variable_to_assign) 
                if not domains.get(other_variable):  # If the other variable has no domain (in other words, it is already assigned)
                    continue                         # skip this constraint
                # Note: don't use domains[other_variable] above because it will throw an error when running cryptarithmatic if the other variable
                # doesn't exit, use domains.get(other_variable) instead as it will return None if the other variable doesn't exit
                
                # for each value in the domain of the other variable
                for val in domains_copy.get(other_variable):
                    # if the value doesn't satisfy the binary constraint with the assigned variable
                    if not constraint.is_satisfied({variable_to_assign:value, other_variable:val}):
                        # increment the number of values that don't satisfy the binary constraint with the assigned variable by 1
                        count += 1
        # append the tuple (value, number of values that don't satisfy the binary constraint with the assigned variable) to the list
        lst.append((value, count))
        

    # sort the values list based on the number of values that don't satisfy the binary constraint with the assigned variable
    lst.sort(key=lambda x: (x[1], x[0]))

    # return a list of the values sorted in ascending order (from the lowest to the highest value)
    return [value[0] for value in lst]


# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #TODO: Write this function
    if not one_consistency(problem):                    # if 1-Consistency deems the whole problem unsolvable
        return None
    
    def recur_solve(Problem, assignment, domains):      # recursive function to apply backtracking search with forward checking
        if Problem.is_complete(assignment):             # if the assignment is complete, then return it
            return assignment

        variable = minimum_remaining_values(Problem, domains)               # get the variable that should be picked based on the MRV heuristic
        values = least_restraining_values(Problem, variable, domains)       # get the domain of the given variable order based on the "least restraining value" heuristic
        domains.pop(variable, None)                     # remove the variable from the domains in order to not be considered in the next recursive call                    
        for value in values:                            # for each value in the domain of the variable after applying the "least restraining value" heuristic
            assignment[variable] = value                # assign the value to the variable
            domains_copy = domains.copy()               # create a copy of the domains to be used in the next recursive call 

            # if forward checking returns True, this means that the assignment is still solvable after the given assignment
            if forward_checking(Problem, variable, value, domains_copy):
                result = recur_solve(Problem, assignment, domains_copy)     # recursive call to the function to continue the backtracking search
                if result:                              # if the recursive call returns a result, then return it
                    return result
            assignment.pop(variable, None)              # remove the variable from the assignment in order to not be considered in the next recursive call
        return None                                     # if no solution was found, return None
    
    return recur_solve(problem, {}, problem.domains)    # call the recursive function with the initial empty assignment and the initial domains