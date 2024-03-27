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
    for i in range(len(word)-3):
        if word[i:i+2] == '=>':
            # print(word[:i])
            first_index = getMatchingBracketBackwards(word, i-2)
            if word[first_index-1].isalpha():
                while word[first_index-1].isalpha():
                    first_index -= 1 
            first_part = word[:first_index]
            # print(first_part, end=' / \n')
            # print(word[first_index:i])
            output = move_negation_inward('~' + word[first_index:i].rstrip())
            word = first_part + output.rstrip() + ' | ' + word[i+2:].lstrip()
        elif word[i:i+3] == '<=>':
            first_index = getMatchingBracketBackwards(word, i-2)
            if word[first_index-1].isalpha():
                while word[first_index-1].isalpha():
                    first_index -= 1 
            first_part = word[:first_index]
            output = move_negation_inward('~' + word[first_index:i].rstrip())
            word = first_part + output.rstrip() + ' | ' + word[i+3:].lstrip() + ' & '  + word[first_index:i].rstrip() +   ' | ' + move_negation_inward('~' + word[i+3:].lstrip())

    return word

def distribute(word: str):
    # Base case: if the expression does not contain an OR, return the expression as it is
    if '|' not in word:
        return word
    # Split the expression into two parts at the OR
    left, right = word.split('|', 1)
    # If either part is an AND expression, distribute the OR over the AND
    if '&' in left and '&' in right:
        left_subparts = left.split('&')
        right_subparts = right.split('&')
        return ' & '.join(f'({distribute(f"{left_subpart.strip()}|{right_subpart.strip()}")})' for left_subpart in left_subparts for right_subpart in right_subparts)
    elif '&' in left:
        subparts = left.split('&')
        return ' & '.join(f'({distribute(f"{subpart.strip()}|{right.strip()}")})' for subpart in subparts)
    elif '&' in right:
        subparts = right.split('&')
        return ' & '.join(f'({distribute(f"{left.strip()}|{subpart.strip()}")})' for subpart in subparts)
    # If neither part is an AND expression, return the expression as it is
    return word

# Takes a statement that looks like the following: ~(smth)
# smth is a combination of ors, ands, and nots
# HAS TO HAVE BRACKETS
def move_negation_inward(word: str):
    # print("  0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789")
    # print(" ", word, end='-=-=-=-')
    index = word.find('~(')
    index2= word.find('~Exists(')
    index3= word.find('~ForAll(')
    cutoff = 1
    if index != -1:
        cutoff = 2
        end = getMatchingBracket(word, index+1)
        # print(index, end)
        if index != 0 or end != len(word)-1:
            return move_negation_inward(word[:index] + move_negation_inward(word[index:end+1]) + word[end+1:])
    elif index2 != -1:
        end = getMatchingBracket(word, word.find('(', index2+7))
        if index2 != 0 or end != len(word)-1:
            index2 = index2 + 7
            return move_negation_inward(word[:index2] + move_negation_inward(word[index2:end+1]) + word[end+1:])
    elif index3 != -1:
        end = getMatchingBracket(word, word.find('(', index2+7))
        if index3 != 0 or end != len(word)-1:
            index3 = index3 + 7
            return move_negation_inward(word[:index3] + move_negation_inward(word[index3:end+1]) + word[end+1:])
    else:
        return word
    # print()
    word = word[cutoff:]
    word = word[:len(word)-1]

    parts = word.split()
    comp = ['~'+i for i in parts]
    result = ''
    for j in comp:
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
    if result.find('~(') != -1:
        return move_negation_inward(result)
    return result

# def move_negation_inward(word: str):
#     # for i in range(len(word)):
#     # if word.find('~(') == -1:
#     #     return word
#     if word.startswith('~('):
#         word = word[2:]
#     elif word.startswith('~'):
#         word = word[1:]
#     if word.endswith(')'):
#         word = word[:len(word)-1]
    # parts = word.split()
    # comp = ['~'+i for i in parts]
    # # print(comp)
    # # print('(', end='')
    # result = ''
    # for j in comp:
    #     # print(j, end='-\n')
    #     if j == '~|':
    #         result += '&'
    #     elif j == '~&':
    #         result += '|'
    #     elif j.startswith('~Exists('):
    #         result += " ForAll"
    #         result += j[7:]
    #     elif j.startswith('~ForAll('):
    #         result += " Exists"
    #         result += j[7:]
    #     else:
    #         result += f' {j} '
    # result = '(' + result[1:len(result)-1] + ')'
    # # print(result)
    # more = result.find('~(')
    # if more != -1:
    #     # print("ENTERED")
    #     preBracket = result[:more]
    #     # print(preBracket)
    #     moreEnd = getMatchingBracket(result, more+1)
    #     # print(result[more:moreEnd+1])
    #     postBracket = result[moreEnd:]
    #     moreResult = move_negation_inward(result[more:moreEnd+1])
    #     # print(moreResult)
    #     # print(postBracket)
    #     result = preBracket + moreResult + postBracket
    # return result

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
  # print(word)

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
# print("0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789")
# splitStatement("Exists(y,(y & x)) | (x & z) => (s | z) <=> ForAll(x, (s & z)) | (s & y | z) => s")
# splitStatement("(Exists(y,(y & x)) <=> ForAll(x, (x & z)))")

def getMatchingBracket(word: str, index: int):
    count = 1
    # print("GetMatchingBracket: ",word, index, end=' ')
    for i in range(index+1, len(word)):
        if word[i] == '(':
            count += 1
        elif word[i] == ')':
            count -= 1
            if count == 0:
                # print(count, i, end='/\n')
                return i
    # print(count)
    return -1

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

    c_end = []
    for i in starts:
        c_end.append(getMatchingBracket(word, i+6))

    return starts, c_end

def extract_quantifier(word: str, index: int):
  # print(word, index)
  # print("0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789")
    if word[index:index+6] == "Exists":
        end = getMatchingBracket(word, index+7)
        return word[index:end+1]
    elif word[index:index+6] == "ForAll":
        end = getMatchingBracket(word, index+7)
        return word[index:end+1]

def skolemize(word: str, c: list, c_end: list, quantifiers: list):

    global consts
    global f_names
    left = len(c)
    c_counter = 0
    f_counter = 0
    offset = 0
    i = 0
    while left > 0:
        start_index = c[i]
        end_index = c_end[i]
        if type(quantifiers[i]) != Exists:
            i += 1
            left -= 1
            continue

        # IF THERE ARE NO CONSTANTS
        if len(quantifiers[i].skol) == 0:
            var = quantifiers[i].variable
            newVar = consts[c_counter]
            quantifiers[i].changeVariable(newVar)

            for j in range(len(quantifiers)):
                # IF THE QUANTIFIER IS INSIDE THE CURRENT QUANTIFIER
                if c_end[j] < end_index:
                    quantifiers[j].changeOtherVariable(var, newVar)
          # print(c_counter, consts)
            c_counter += 1
        
        else:
            var = quantifiers[i].variable
            newVar = f_names[f_counter] + '(' + ','.join(quantifiers[i].skol) + ')'
          # print("====", newVar)
            quantifiers[i].changeVariable(newVar)

            for j in range(len(quantifiers)):
                if c_end[j] < end_index:
                    quantifiers[j].changeOtherVariable(var, newVar)
                    c, c_end = count_quantifiers(word)
          # print("From ", var, " To ", newVar)
            f_counter += 1


        word = update_statements(word, quantifiers, c, c_end)


        left -= 1
        i += 1

    return word

def removeMatchingBracket(word: str, index: int = 0):
    # print(word)
    if word[index] == '(':
        i = getMatchingBracket(word, index)
        # print(index, i)
        if i == len(word)-1:
            # print(i)
            return removeMatchingBracket(word[:index] + word[index+1:i] + word[i+1:])
        else:
            # print(i)
            return word[:index] + word[index+1:i] + word[i+1:]
    return word

def removeQuantifiers(word):
    c, c_end = count_quantifiers(word)
    while len(c) > 0:
      # print(c)
      # print(c_end)
        start_index = c[0]
        offset = word.find(',', c[0])
        end_index = c_end[0]
      # print(start_index)
      # print(offset)
      # print(end_index)
      # print('012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789')
        # word = word.lstrip().rstrip()
        # print("==", word, "Before: ")
        word = word[:start_index] + word[offset+2:end_index] + word[end_index+1:]
        # word = word.lstrip().rstrip()
        # print("==", word, "After : ")
        
        c, c_end = count_quantifiers(word)

        word = removeMatchingBracket(word)
      # print(word, "After : ")
        c, c_end = count_quantifiers(word)

    return word

def build_quantifiers(word, quantifiers, c, c_end):
    used_vars = []
    scoped_vars = []
  # print("Build_Quantifiers")
  # print(word)
  # print(c, c_end)
    for i in c:
        # print(extract_quantifier(word, i))
        for j in range(len(c_end)):
            if i >= c_end[j] and quantifiers[j].variable in scoped_vars:
                var = quantifiers[j].variable
              # print("Removed: ", var)
                scoped_vars.remove(var)

        if word[i] == 'E':
            quantifiers.append(Exists(extract_quantifier(word, i), scoped_vars))
          # print(scoped_vars, i)
            scoped_vars.append(quantifiers[-1].variable)
          # print("Added: ", scoped_vars[-1])
        else:
            quantifiers.append(ForAll(extract_quantifier(word, i), scoped_vars))
        if quantifiers[-1].variable in used_vars:
            for i in vars:
                if i not in used_vars:
                    quantifiers[-1].changeVariable(i)
                    break
        used_vars.append(quantifiers[-1].variable)
            # print(used_vars)
  # print("END BUILD_QUANTIFIERS")
    return quantifiers

def update_statements(word, quantifiers, c, c_end):
    for i in range(len(quantifiers)):
        start_index = c[i]
        end_index = c_end[i]
      # print('===============================================')
      # print("Using: ", quantifiers[i].statement)
      # print("With Indexes: ", start_index, end_index)
      # print('012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789')
      # print(word, "Was:    ")
        word = word[:start_index] + quantifiers[i].pre + quantifiers[i].statement + ')' + word[end_index+1:]
      # print(word, "Now is: ")
      # print('===============================================')
        c, c_end = count_quantifiers(word)
    return word

def removeDuplicateBrackets(word: str):
    # print(word)
    changed = False
    for i in range(len(word)-1):
        if word[i:i+2] == '((':
            # print(@chingBracket(word, i))
            # print(getMatchingBracket(word, i+1))
            if (getMatchingBracket(word, i) == getMatchingBracket(word, i+1) + 1):
                word = removeMatchingBracket(word, i)
                changed = True
    if changed:
        return removeDuplicateBrackets(word)
    else:
        return word

def CNFify(word: str):

    # print(word)

    # Eliminate Implication
    # and Compute negated brackets (Executed inside eliminate_implication)
    word = eliminate_implication(word)
    # print(word)

    # Check for double negation
    word = remove_double_negation(word)
    # print(word)

    # Check for quantifiers
    c, c_end = count_quantifiers(word)
    # print("Start: ", c)
    # print("End:   ", c_end)
    quantifiers = []

    quantifiers = build_quantifiers(word, quantifiers, c, c_end)
    # print(getMatchingBracket(word, c[0]+6))

    word = update_statements(word, quantifiers, c, c_end)
    quantifiers = []
    build_quantifiers(word, quantifiers, c, c_end)
    # update_statements(word, quantifiers)

    # print("0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789")
    # print(word)
    word = skolemize(word, c, c_end, quantifiers)
    # print("0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789")
    # print(word)
    word = removeQuantifiers(word)
    word = removeDuplicateBrackets(word)
    # print(word)
    word = distribute(word)
    # print(word)
    word = removeDuplicateBrackets(word)
    # print(word)
    word = move_negation_inward(word)
    # print(word)
    word = removeMatchingBracket(word)
    # print(word)
    result = process(word)
    return result

    # quantifiers[-1].changeVariable('zayat')
    # for i in quantifiers[::-1]:

    #   # print(type(i), end=', ')
    #   # print(i.variable, end=', ')
        # print(i.skol.index('y'), end=', \n')
    #   # print(i.statement)
    # print(word.replace(quantifiers[-1].statement, 'test'))

def finish_brackets(word):
    arr = [i.rstrip().lstrip() for i in word.split('|')]
    for i in range(len(arr)):
        if arr[i].startswith('(') and getMatchingBracket(arr[i], 0) == len(arr[i])-1:
            arr[i] = arr[i][1:len(arr[i])-1]

    result = ''
    for i in arr:
        result += i + ' | '
    return result[:len(result)-3]

def process(word):
    arr = word.split('&')
    result = []
    for i in arr:
        # print(finish_brackets(i.rstrip().lstrip()))
        # print(finish_brackets(removeMatchingBracket(i.rstrip().lstrip())))
        result.append('('+finish_brackets(removeMatchingBracket(i.rstrip().lstrip()))+')')

    return result
if __name__ == "__main__":
    # x = CNFify("(ForAll(y, ((Exists(x, (Test(y,x))) & Easy(y)) => ForAll(z, (Pass(z,y)))))")
    # x = getMatchingBracket("(((ForAll(x, (~Test(y,x))) | ~Easy(y)) | ForAll(z, (Pass(z,y)))))", 0)
    y = CNFify("(Exists(y, ((ForAll(x, (Test(y,x))) & Easy(y)) => Exists(x, (Pass(x,y))))))")
    # print(x)
    print(y)
    # NEED TO ADD A CHECKER IN CASE OF MOVING NEGATION INTO BRACKET THAT THERE IS NO LETTER BEFORE IT
    # CAN REMOVE THE BRACKETS ON T(x) TO UNDERSTAND
    # z = CNFify("(ForAll(x, (ForAll(y, (ForAll(z, ((M(x)) => (~M(y) & ~M(z))))))))")
    # z = CNFify("(ForAll(x, (ForAll(y, (ForAll(z, ((M(x) | M(z)) => (~M(y) & ~M(z)))))))))")
    # z = CNFify("~(Exists(x, Exists(y, (Pass(x,y) & Fail(x,y)))))")
    # z = move_negation_inward("~(Pass(a,f(a)) & Fail(a,f(a)))")
    # print(z)
    # CNFify("(ForAll(x, ((T(x)) => (~M(x)))))")
    # CNFify("(Te(x) => ~M(x))")
