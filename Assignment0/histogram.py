from typing import Any, Dict, List
import utils


def histogram(values: List[Any]) -> Dict[Any, int]:
    '''
    This function takes a list of values and returns a dictionary that contains the list elements alongside their frequency
    For example, if the values are [3,5,3] then the result should be {3:2, 5:1} since 3 appears twice while 5 appears once 
    '''
    #TODO: ADD YOUR CODE HERE
    #Comments: Initiate an empty dictionary and loop on the list, if an element in the list exists in the dict then increment
    #its freq, if not then make its freq = 1
    frequencyDict : Dict[Any, int] = {}
    for element in values:
        if element in frequencyDict:
            frequencyDict[element]+=1
        else:
            frequencyDict[element]=1
    return frequencyDict