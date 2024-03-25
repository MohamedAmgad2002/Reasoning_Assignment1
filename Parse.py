# from main import eliminate_implication
from Exists import Exists
from ForAll import ForAll
vars = [chr(i) for i in range(114, 123)]
f_names = [chr(i) for i in range(102, 114)]
consts = [chr(i) for i in range(97, 102)]
# print(consts)
# print(f_names)
# print(vars)

# Takes a statement that looks like the following: 
# (smth) => (y) returns ~(smth) | (y)
# (smth) <=> (y) returns ~(smth) | (y) & ~(y) | (smth)
# Calls move_negation_inward on the result
def eliminate_implication(word: str):
    for i in range(len(word)-1):
        if word[i:i+2] == '=>':
            # print(word[:i])
            first_index = getMatchingBracketBackwards(word, i-2)
            first_part = word[:first_index]
            output = move_negation_inward('~' + word[first_index:i].rstrip())
            word = first_part + output.rstrip() + ' | ' + word[i+2:].lstrip()

    return word

# Takes a statement that looks like the following: ~(smth)
# smth is a combination of ors, ands, and nots
# HAS TO HAVE BRACKETS
def move_negation_inward(word: str):
    # for i in range(len(word)):
    word = word[2:]
    word = word[:len(word)-1]
    parts = word.split()
    comp = ['~'+i for i in parts]
    # print(comp)
    # print('(', end='')
    result = ''
    for j in comp:
        # print(j, end='-\n')
        if j == '~|':
            result += '&'
        elif j == '~&':
            result += '|'
        elif j.startswith('~Exists('):
            result += " ForAll"
            result += j[7:]
        elif j.startswith('~ForAll('):
            result += " Exists"
            result += j[7:]
        else:
            result += f' {j} '
    result = '(' + result[1:len(result)-1] + ')'
    # print(result)
    more = result.find('~(')
    if more != -1:
        # print("ENTERED")
        preBracket = result[:more]
        # print(preBracket)
        moreEnd = getMatchingBracket(result, more+1)
        # print(result[more:moreEnd+1])
        postBracket = result[moreEnd:]
        moreResult = move_negation_inward(result[more:moreEnd+1])
        # print(moreResult)
        # print(postBracket)
        result = preBracket + moreResult + postBracket
    return result

# Looks for any ~~ in the string and removes them
def remove_double_negation(word: str):
    result = word.replace('~~', '')
    return result

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



# print("Exists(y,(y & x)) | (x & z) => (s | z) <=> ForAll(x, (s & z)) | (s & y | z) => s")
print("0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789")
# splitStatement("Exists(y,(y & x)) | (x & z) => (s | z) <=> ForAll(x, (s & z)) | (s & y | z) => s")
# splitStatement("(Exists(y,(y & x)) <=> ForAll(x, (x & z)))")

"""
Ax. () 
ForAll(y,(y & x)) | (x & z)
Exists(y,(y & x)) | (x & z)
(Exists(y,(y <-> x)) | (x & z)) <-> (x)
(Exists(y,(y & x)) | (x & z)) -> (x)
(x & z)
l = ["(~y | x)", "(~x | z)", "(z | ~y)"]
"""

def getMatchingBracket(word: str, index: int):
    count = 1
    for i in range(index+1, len(word)):
        if word[i] == '(':
            count += 1
        elif word[i] == ')':
            count -= 1
            if count == 0:
                return i

def getMatchingBracketBackwards(word: str, index: int):
    count = 1
    for i in range(index-1, -1, -1):
        if word[i] == ')':
            count += 1
        elif word[i] == '(':
            count -= 1
            if count == 0:
                return i

def count_quantifiers(word: str):
    # return word.count("Exists") + word.count("ForAll")\
    starts = []
    for i in range(len(word)-6):
        if word[i:i+6] == "Exists":
            starts.append(i)
        elif word[i:i+6] == "ForAll":
            starts.append(i)
    return starts


def extract_quantifier(word: str, index: int):
    if word[index:index+6] == "Exists":
        end = getMatchingBracket(word, index+7)
        return word[index:end+1]
    elif word[index:index+6] == "ForAll":
        end = getMatchingBracket(word, index+7)
        return word[index:end+1]

# def extract_quantifier_variable(word: str, index: int):
    

def CNFify(word: str):
    print(word)

    # Eliminate Implication
    # and Check for negated brackets (Executed inside eliminate_implication)
    word = eliminate_implication(word)
    print(word)

    # Check for double negation
    # word = remove_double_negation(word)
    # print(word)

    # Check for quantifiers
    c = count_quantifiers(word)
    # print(c)\
    used_vars = []
    quantifiers = []
    for i in c:
        # print(extract_quantifier(word, i))
        if word[i] == 'E':
            quantifiers.append(Exists(extract_quantifier(word, i), []))
        else:
            quantifiers.append(ForAll(extract_quantifier(word, i), []))
        if quantifiers[-1].variable in used_vars:
            for i in vars:
                if i not in used_vars:
                    quantifiers[-1].changeVariable(i)
                    break
        used_vars.append(quantifiers[-1].variable)
        # print(used_vars)
    # print(getMatchingBracket(word, c[0]+6))
    for i in quantifiers:
        print(type(i), end=', ')
        print(i.variable, end=', ')
        print(i.statement)

# CNFify("ForAll(y, ((Exists(x, (Test(y,x))) & Easy(y)) => ForAll(z, (Pass(z,y)))))")
# CNFify("(ForAll(x, (ForAll(y, (ForAll(z, ((M(x)) => (~M(y) & ~M(z))))))))")
# NEED TO ADD A CHECKER IN CASE OF MOVING NEGATION INTO BRACKET THAT THERE IS NO LETTER BEFORE IT
# CAN REMOVE THE BRACKETS ON T(x) TO UNDERSTAND
CNFify("(ForAll(x, ((T(x)) => (~M(x)))))")
