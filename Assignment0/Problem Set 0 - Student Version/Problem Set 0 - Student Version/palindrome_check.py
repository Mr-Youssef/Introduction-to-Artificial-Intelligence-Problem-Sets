import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    #TODO: ADD YOUR CODE HERE
    #Comments: [::-1] means start at the end of the string and end at position 0, 
    #and move with step -1, which is one step backwards.
    return string == string[::-1]