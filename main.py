from Parse import CNFify
from solve import resolution
# print("==============Testing================")
# statement1 = """ForAll(y, (((Exists(x, (Test(y,x))) & Easy(y)) => (ForAll(z, (Pass(z,y)))))"""
# print(CNFify(statement1))
# (~Test(y,x) | ~Easy(y) | (Pass(z,y)))


def loadStatement(word: list, kb: list):
    # print('run')
    for i in word:
        # print(type(i))
        kb.append(i)
    return kb


print("=====================================")
statement1 = "ForAll(x, ((T(x)) => (~M(x))))"
statement2 = "ForAll(x, (ForAll(y, (ForAll(z, ((M(x)) => (~M(y) & ~M(z))))))))"
statement3 = "T(Arthur) => M(Carleton)"
statement4 = "T(Bertram) => ~M(Bertram)"
statement5 = "T(Carleton) => ~M(Carleton)"
statement6 = "T(Arthur)"
statement7 = "T(Bertram)"
x1 = CNFify(statement1)
x2 = CNFify(statement2)
x3 = CNFify(statement3)
x4 = CNFify(statement4)
x5 = CNFify(statement5)
x6 = CNFify(statement6)
x7 = CNFify(statement7)
out = [x1, x2, x3, x4, x5, x6, x7]
kb = []
for i in out:
    loadStatement(i, kb)
for i in kb:
    print(i)
# print(kb)
# print(len(kb))
# for i in kb:
    # print(i)
# USE RESOLUTION TO PROVE THAT
prove1 = "(~T(Carleton))"
prove2 = "(~M(Arthur))"
# USE RESOLUTION TO PROVE THAT
if resolution(kb, prove1, 200):
    print('{}')
if resolution(kb, prove2, 200):
    print('{}')
print("=====================================")
statement1 = "ForAll(x, ((Read(x)) => (~Stupid(x))))"
statement2 = "Read(John) & Wealthy(John)"
statement3 = "ForAll(x, ((Poor(x)) => (~Wealthy(x))))"
statement4 = "ForAll(x, (Stupid(x) | Smart(x)))"
statement5 = "ForAll(x, ((~Poor(x) & Smart(x)) => (Happy(x))))"
statement6 = "ForAll(x, ((~Exciting(x)) => (~Happy(x))))"
x1 = CNFify(statement1)
x2 = CNFify(statement2)
x3 = CNFify(statement3)
x4 = CNFify(statement4)
x5 = CNFify(statement5)
x6 = CNFify(statement6)
out = [x1, x2, x3, x4, x5, x6]
kb = []
for i in out:
    loadStatement(i, kb)
for i in kb:
    print(i)
# USE RESOLUTION TO PROVE THAT
prove = "(Exciting(x))"
if resolution(kb, prove, 200):
    print('{}')
print("=====================================")
statement1 = "ForAll(x, (ForAll(y, ((CScourse(x) & Test(y,x)) => (Exists(z, Fail(z,y)))))))"
statement1 = "ForAll(x, (ForAll(y, ((CScourse(x)) => (Exists(z, Fail(z,y)))))))"
statement2 = "ForAll(y, ((Exists(x, (Test(y,x))) & Easy(y)) => (ForAll(z, (Pass(z,y))))))"
statement3 = "~(Exists(x, Exists(y, (Pass(x,y) & Fail(x,y)))))"
statement4 = "Test(Exam1,Class1)"
statement5 = "Easy(Exam1)"
prove = "(~CScourse(Class1))"
x1 = CNFify(statement1)
x2 = CNFify(statement2)
x3 = CNFify(statement3)
x4 = CNFify(statement4)
x5 = CNFify(statement5)
out = [x1, x2, x3, x4, x5]
kb = []
for i in out:
    loadStatement(i, kb)
for i in kb:
    print(i)
if resolution(kb, prove, 20000):
    print('{}')
# for i in kb:
# print(i)
# USE RESOLUTION TO PROVE THAT
