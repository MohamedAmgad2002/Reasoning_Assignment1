from Exists import Exists
from ForAll import ForAll

# Takes a statement that looks like the following: smth -> y
def eliminate_implication(word: str):
    for i in range(len(word)):
        if word[i:i+2] == '->':
            word = '~' + word[:i] + '|' + word[i+2:]

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
        if j == '~|':
            result += '&'
        elif j == '~&':
            result += '|'
        else:
            result += f' {j} '
    result = '(' + result[1:len(result)-1] + ')'
    return result

# Looks for any ~~ in the string and removes them
def remove_double_negation(word: str):
    result = word.replace('~~', '')
    return result

# print(eliminate_implication("(~X) -> (Y)"))
# print(move_negation_inward("(~~X | Y)"))
# print(remove_double_negation("~~X | Y"))
# e = Exists('z', "Exists(q(x,y,z))")
# e.changeVariable('p(x,y)')
# print(e.statement)



"""
<->, ->, &, |, ~
"""