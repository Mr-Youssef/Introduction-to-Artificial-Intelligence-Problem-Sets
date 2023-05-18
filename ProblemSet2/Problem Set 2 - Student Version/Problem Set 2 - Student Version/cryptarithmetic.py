from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        # Helper functions to generate the domains of the new auxiliary variables
        # The domains of the auxiliary variables are the permutations of the domains of the variables they represent
        # For example, if the domain of the variable "A" is {1, 2, 3} and the domain of the variable "B" is {4, 5}
        # then the domain of the auxiliary variable "AB" is {(1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)}
        def domainPermutations2(variable1, variable2):
            return {(x, y) for x in problem.domains[variable1] for y in problem.domains[variable2]}
        
        def domainPermutations3(variable1, variable2, variable3):
            return {(x, y, z) for x in problem.domains[variable1] for y in problem.domains[variable2] for z in problem.domains[variable3]}

        problem.variables = list(set(LHS0 + LHS1 + RHS))
        problem.domains = {letter: set(range(10)) for letter in problem.variables}
        problem.constraints = []

        # binary constraints, all different
        # Note: we did it before adding the carries variables because the carries can be not unique, only the original variables must be unique
        for i in range(len(problem.variables)):
            for j in range(i+1, len(problem.variables)):
                problem.constraints.append(BinaryConstraint((problem.variables[i], problem.variables[j]), lambda x, y: x != y))
    
        # Create variables for the carries, the number of carries is the max between the length of the two LHS
        # Note that my carry variables start from C1 to Cn, where n is the max between the length of the two LHS (not C0)
        for i in range(max(len(LHS0), len(LHS1))):
            problem.variables.append(f"C{i+1}")
        problem.domains.update({f"C{i+1}": set(range(2)) for i in range(max(len(LHS0), len(LHS1)))})

        # Removing the leading zeros from the domains of the variables, since the leading zeros are not allowed, 
        # could be done using unary constraints instead as well
        problem.domains[LHS0[0]].discard(0)
        problem.domains[LHS1[0]].discard(0)
        problem.domains[RHS[0]].discard(0)

        # Just a special case where we can reduce the domain of the first letter of the RHS and the last carry
        # since the last carry + 0 = RHS[0] & since the RHS is greater than the longest LHS, 
        # therefore the last carry must be 1 and hence the first letter of the RHS must be 1
        if len(RHS) > max(len(LHS0), len(LHS1)):
            problem.domains[RHS[0]] = {1}
            problem.domains["C" + str(max(len(LHS0), len(LHS1)))] = {1}

        # Last letter constraints
        auxiliaryLeft = LHS0[-1] + LHS1[-1]                         # auxiliary variable used to make binary constraints from n-ary constraints, the last letter of the LHS0 and LHS1
        problem.variables.append(auxiliaryLeft)                     # add the auxiliary variable to the list of variables
        problem.domains[auxiliaryLeft] = domainPermutations2(LHS0[-1], LHS1[-1])  # add the domain of the auxiliary variable
        problem.constraints.append(BinaryConstraint((auxiliaryLeft, LHS0[-1]), lambda x, y: x[0] == y))  # Binary constraint that the variable in the auxiliary is the letter in the LHS0[-1]
        problem.constraints.append(BinaryConstraint((auxiliaryLeft, LHS1[-1]), lambda x, y: x[1] == y))  # Binary constraint that the variable in the auxiliary is the letter in the LHS1[-1]

        auxiliaryRight = RHS[-1] + "C1"                             # auxiliary variable used to make binary constraints from n-ary constraints, the last letter of the RHS and the carry
        problem.variables.append(auxiliaryRight)                    # add the auxiliary variable to the list of variables
        problem.domains[auxiliaryRight] = domainPermutations2(RHS[-1], "C1")      # add the domain of the auxiliary variable
        problem.constraints.append(BinaryConstraint((auxiliaryRight, RHS[-1]), lambda x, y: x[0] == y))  # Binary constraint that the variable in the auxiliary is the letter in the RHS[-1]
        problem.constraints.append(BinaryConstraint((auxiliaryRight, "C1"), lambda x, y: x[1] == y))     # Binary constraint that the variable in the auxiliary is the carry

        problem.constraints.append(BinaryConstraint((auxiliaryLeft, auxiliaryRight), lambda x, y: x[0] + x[1] == y[0] + 10*y[1]))  # Binary constraint that the sum of the auxiliary variables is the sum of the RHS[-1] and the carry * 10

        # Middle letters constraints
        minLength = min(len(LHS0), len(LHS1))
        for i in range(minLength - 1):
            auxiliaryLeft = LHS0[-2-i] + LHS1[-2-i] + "C" + str(i+1)        # auxiliary variable used to make binary constraints from n-ary constraints, the auxiliary is the conactenation of the two letters of the LHS0 and LHS1 and the carry
            problem.variables.append(auxiliaryLeft)                         # add the auxiliary variable to the list of variables   
            problem.domains[auxiliaryLeft] = domainPermutations3(LHS0[-2-i], LHS1[-2-i], "C" + str(i+1))  # add the domain of the auxiliary variable
            problem.constraints.append(BinaryConstraint((auxiliaryLeft, LHS0[-2-i]), lambda x, y: x[0] == y))  # Binary constraint that the variable in the auxiliary is the letter in the LHS0[-2-i]
            problem.constraints.append(BinaryConstraint((auxiliaryLeft, LHS1[-2-i]), lambda x, y: x[1] == y))  # Binary constraint that the variable in the auxiliary is the letter in the LHS1[-2-i]
            problem.constraints.append(BinaryConstraint((auxiliaryLeft, "C" + str(i+1)), lambda x, y: x[2] == y))  # Binary constraint that the variable in the auxiliary is the carry

            auxiliaryRight = RHS[-2-i] + "C" + str(i+2)                     # auxiliary variable used to make binary constraints from n-ary constraints, the auxiliary is the conactenation of the letter of the RHS and the carry
            problem.variables.append(auxiliaryRight)                        # add the auxiliary variable to the list of variables
            problem.domains[auxiliaryRight] = domainPermutations2(RHS[-2-i], "C" + str(i+2))  # add the domain of the auxiliary variable
            problem.constraints.append(BinaryConstraint((auxiliaryRight, RHS[-2-i]), lambda x, y: x[0] == y))  # Binary constraint that the variable in the auxiliary is the letter in the RHS[-2-i]
            problem.constraints.append(BinaryConstraint((auxiliaryRight, "C" + str(i+2)), lambda x, y: x[1] == y))  # Binary constraint that the variable in the auxiliary is the carry

            problem.constraints.append(BinaryConstraint((auxiliaryLeft, auxiliaryRight), lambda x, y: x[0] + x[1] + x[2] == y[0] + 10*y[1]))  # Binary constraint that the sum of the auxiliary variables is the sum of the RHS[-2-i] and the carry * 10

        # Leftmost letters constraints
        difference = abs(len(LHS0) - len(LHS1))
        longestString = LHS0 if len(LHS0) > len(LHS1) else LHS1
        for i in range(difference):
            auxiliaryLeft = longestString[difference-1-i] + "C" + str(minLength+i)  # auxiliary variable used to make binary constraints from n-ary constraints, the auxiliary is the conactenation of the letter of the longestString and the carry
            problem.variables.append(auxiliaryLeft)                                 # add the auxiliary variable to the list of variables
            problem.domains[auxiliaryLeft] = domainPermutations2(longestString[difference-1-i], "C" + str(minLength+i))  # add the domain of the auxiliary variable
            problem.constraints.append(BinaryConstraint((auxiliaryLeft, longestString[difference-1-i]), lambda x, y: x[0] == y))  # Binary constraint that the variable in the auxiliary is the letter in the longestString[difference-1-i]
            problem.constraints.append(BinaryConstraint((auxiliaryLeft, "C" + str(minLength+i)), lambda x, y: x[1] == y))      # Binary constraint that the variable in the auxiliary is the carry

            auxiliaryRight = RHS[-1-minLength-i] + "C" + str(minLength+i+1)  # auxiliary variable used to make binary constraints from n-ary constraints, the auxiliary is the conactenation of the letter of the RHS and the carry
            problem.variables.append(auxiliaryRight)                         # add the auxiliary variable to the list of variables
            problem.domains[auxiliaryRight] = domainPermutations2(RHS[-1-minLength-i], "C" + str(minLength+i+1))  # add the domain of the auxiliary variable
            problem.constraints.append(BinaryConstraint((auxiliaryRight, RHS[-1-minLength-i]), lambda x, y: x[0] == y))  # Binary constraint that the variable in the auxiliary is the letter in the RHS[-1-minLength-i]
            problem.constraints.append(BinaryConstraint((auxiliaryRight, "C" + str(minLength+i+1)), lambda x, y: x[1] == y))  # Binary constraint that the variable in the auxiliary is the carry

            problem.constraints.append(BinaryConstraint((auxiliaryLeft, auxiliaryRight), lambda x, y: x[0] + x[1] == y[0] + 10*y[1]))  # Binary constraint that the sum of the auxiliary variables is the sum of the RHS[-1-minLength-i] and the carry * 10

        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())