from Exists import Exists
from ForAll import ForAll
# from Parse import *

vars = [chr(i) for i in range(114, 123)]
f_names = [chr(i) for i in range(102, 114)]
consts = [chr(i) for i in range(65, 91)]

# Takes a statement that looks like the following: (smth) => (y)
def eliminate_implication(word: str):
    for i in range(len(word)-1):
        if word[i:i+2] == '=>':
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
        print(j, end='-\n')
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
    return result

# Looks for any ~~ in the string and removes them
def remove_double_negation(word: str):
    result = word.replace('~~', '')
    return result

# print(eliminate_implication("(~X) -> (Y)"))
# print(move_negation_inward("(~~X | Y)"))
# print(move_negation_inward("~(Exists(x, q(x,y,z)))"))
# print(remove_double_negation("~~X | Y"))
# e = Exists('z', "Exists(q(x,y,z))")
# e.changeVariable('p(x,y)')
# print(e.statement)

def count_quantifiers(word: str):
    return word.count("Exists") + word.count("ForAll")

def getMatchingBracket(word: str, left: int):
    count = 0
    for i in range(left, len(word)):
        if word[i] == '(':
            count += 1
        elif word[i]==')':
            count -= 1
            if count == 0:
                return i
    return -1

def getVariable(word: str):
    for i in range(5, len(word)):
        if word[i] == ',':
            return word[7:i]

# statement1 = "ForAll(x, p(x)) | ForAll(x, q(x) <=> Exists(y, f(x,y)))"

statement1 = "ForAll(x, (T(x) => ~M(x)))"
statement2 = "ForAll(x, (ForAll(y, (ForAll(z, (M(x) => ~M(y), & ~M(z)))))))"
statement3 = "T(Arthur) => M(Carleton))"
statement4 = "T(Bertram) => ~M(Bertram)"
statement5 = "T(Carleton) => ~M(Carleton))"
statement6 = "T(Arthur)"
statement7 = "T(Bertram)"
prove = "T(Carleton)"

statement1 = "Exists(x, (Dog(x) & Owns(Jack, x)))"
statement2 = "ForAll(x, ((Exists(y, (Dog(y) & Owns(x,y)))) => (AnimalLover(x))))"
statement3 = "ForAll(x, ((AnimalLover(x)) => (ForAll(y, (Animal(y) => ~Kills(x,y))))))"
statement4 = "Kills(Jack,Tuna) | Kills(Curioisity,Tuna)"
statement5 = "Cat(Tuna)"
statement6 = "ForAll(x, (Cat(x) => Animal(x)))"
prove = "~Kills(Curiosity,Tuna)"

# n = count_quantifiers(statement2)
# print(n)
# v = getVariable(statement1)
# print(v)

# for i in range(n):




"""
<=>, =>, &, |, ~
"""