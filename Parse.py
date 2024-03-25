from main import eliminate_implication
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

def bracketCount(word: str, limit: int, start=0):
    count = 0

    if limit > len(word):
        raise Exception("Limit can't be bigger than word length")
    for i in range(start, limit):
        if word[i] == '(':
            count += 1
        elif word[i]==')':
            count -= 1
        
    return count

def getFirstInstance(word: str, symbol: str):
    i = 0
    while i < len(word):
        result = word.find(symbol, i)
        if result != -1 and bracketCount(word, result) == 0:
            return result
        
        i += 1
    return -1

def splitStatement(word: str):
    print(word)
    bicond = getFirstInstance(word, '<=>')
    if bicond != -1:
        s1 = word[:bicond-1]
        s2 = word[bicond+4:]
        s = eliminate_implication(s1 + ' => ' + s2)
        s += ' & ' + eliminate_implication(s2 + ' => ' + s1)
        splitStatement(s1)
        splitStatement(s2)
        print(s)
        return
    cond = getFirstInstance(word, '=>')
    if cond != -1:
        splitStatement(word[:cond-1])
        splitStatement(word[cond+3:])
        return
    conjunct = getFirstInstance(word, '&')
    if conjunct != -1:
        splitStatement(word[:conjunct-1])
        splitStatement(word[conjunct+2:])
        return
    disjunct = getFirstInstance(word, '|')
    if disjunct != -1:
        splitStatement(word[:disjunct-1])
        splitStatement(word[disjunct+2:])
        return
    # print(getFirstInstance(word, '=>'))
    # print(getFirstInstance(word, '&'))



print("Exists(y,(y & x)) | (x & z) => (s | z) <=> ForAll(x, (s & z)) | (s & y | z) => s")
print("01234567890123456789012345678901234567890123456789012345678901234567890123456789")
# splitStatement("Exists(y,(y & x)) | (x & z) => (s | z) <=> ForAll(x, (s & z)) | (s & y | z) => s")
splitStatement("(Exists(y,(y & x)) <=> ForAll(x, (x & z)))")

"""
Ax. () 
ForAll(y,(y & x)) | (x & z)
Exists(y,(y & x)) | (x & z)
(Exists(y,(y <-> x)) | (x & z)) <-> (x)
(Exists(y,(y & x)) | (x & z)) -> (x)
(x & z)
l = ["(~y | x)", "(~x | z)", "(z | ~y)"]
"""

def CNFify(word: str):
    print(word)

