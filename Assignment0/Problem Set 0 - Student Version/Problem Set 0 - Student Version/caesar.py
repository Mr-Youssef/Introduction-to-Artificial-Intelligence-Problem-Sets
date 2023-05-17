from typing import Tuple, List
import utils

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    #TODO: ADD YOUR CODE HERE
    splitedStr = ciphered.split(" ")
    newDict={}
    for i in dictionary:
        newDict[i] = "0"  #Convert from list to dictionary with assigning a dummy value equal 0
    min= float('inf')  #Infinite number
    tempTuple={}
    for i in range(26):
        freq=0
        temp_arr = []
        for j in splitedStr:
            tempString=""
            for k in j:
                if ord(k)-i < 97: #97 corresponds to 'a' in ascii
                    tempString+= chr(ord(k)-i + 26)  #wrap around
                else:    
                    tempString+= chr(ord(k)-i)
            if not newDict.get(tempString):
                freq+=1
            temp_arr.append(tempString)
        temp_arr = " ".join(temp_arr)
        if freq<min:
            min=freq
            tempTuple=(temp_arr,i,min)
    return tempTuple


            
                
