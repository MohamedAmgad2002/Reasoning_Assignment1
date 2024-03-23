from main import eliminate_implication, remove_double_negation, move_negation_inward
from Exists import Exists
from ForAll import ForAll
vars = [chr(i) for i in range(114, 123)]
f_names = [chr(i) for i in range(102, 114)]
consts = [chr(i) for i in range(97, 102)]
# print(consts)
# print(f_names)
# print(vars)
def getBracketEndIndex(word: str):
    count = 1
    for i in range(len(word)):
        if word[i] == '(':
            count += 1
        elif word[i] == ')':
            count -= 1
        
        if count == 0:
            return i+1
    return -1

def parseString(word: str):
    if word.startswith("ForAll("):
        ForAll(word[7:word.find(',')], word[word.find(',')+1:word.find(',')+2+getBracketEndIndex(word[word.find(',')+2:])])
    elif word.startswith("Exists("):
        Exists(word[7:word.find(',')], word[word.find(',')+1:word.find(',')+2+getBracketEndIndex(word[word.find(',')+2:])])

    



parseString("Exists(y,(y & x)) | (x & z)")

"""
Ax. ()
ForAll(y,(y & x)) | (x & z)
Exists(y,(y & x)) | (x & z)
(Exists(y,(y <-> x)) | (x & z)) <-> (x)
(Exists(y,(y & x)) | (x & z)) -> (x)
(1 & z)
[(~y | x), (~x | z), (z | ~y)]
"""