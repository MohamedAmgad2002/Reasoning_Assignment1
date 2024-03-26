from Parse import CNFify
from solve import standardize
print("==============Testing================")
statement1 = "ForAll(y, ((Exists(x, (Test(y,x))) & Easy(y)) => ForAll(z, (Pass(z,y))))"
print(CNFify(statement1))
# (~Test(y,x) | ~Easy(y) | (Pass(z,y)))

print("=====================================")
statement1 = "ForAll(x, ((T(x)) => (~M(x))))"
statement2 = "ForAll(x, (ForAll(y, (ForAll(z, ((M(x)) => (~M(y) & ~M(z))))))))"
statement3 = "T(Arthur) => M(Carleton))"
statement4 = "T(Bertram) => ~M(Bertram)"
statement5 = "T(Carleton) => ~M(Carleton))"
statement6 = "T(Arthur)"
statement7 = "T(Bertram)"
x1 = CNFify(statement1)
x2 = CNFify(statement2)
x3 = CNFify(statement3)
x4 = CNFify(statement4)
x5 = CNFify(statement5)
x6 = CNFify(statement6)
x7 = CNFify(statement7)
kb = [x1, x2, x3, x4, x5, x6, x7]
print("before standardize")
for i in kb:
    print(i)
print("after standardize")
kb = standardize(kb)
for i in kb:
    print(i)
# USE RESOLUTION TO PROVE THAT
prove1 = "~T(Carleton)"
prove2 = "~T(Arthur)"
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
kb = [f'({x1})', x2, x3, x4, x5, x6]
print("before standardize")
for i in kb:
    print(i)
kb = standardize(kb)
print("after standardize")
for i in kb:
    print(i)
# USE RESOLUTION TO PROVE THAT
prove = "Exciting(a)"
print("=====================================")
statement1 = "ForAll(x, (ForAll(y, ((CScourse(x) & Test(y,x)) => (Exists(z, Fail(z,y)))))))"
# statement2 = "ForAll()"
statement3 = "~(Exists(x, Exists(y, (Pass(x,y) & Fail(x,y)))))"
statement4 = "ForAll(x, (Stupid(x) | Smart(x)))"
statement5 = "ForAll(x, ((~Poor(x) & Smart(x)) => (Happy(x))))"
statement6 = "ForAll(x, ((~Exciting(x)) => (~Happy(x))))"
# x1 = CNFify(statement1)
# x2 = CNFify(statement2)
x3 = CNFify(statement3)
print(x3)
# x4 = CNFify(statement4)
# x5 = CNFify(statement5)
# x6 = CNFify(statement6)
# kb = [f'({x1})', x2, x3, x4, x5, x6]
# print("before standardize")
# for i in kb:
    # print(i)
# kb = standardize(kb)
# print("after standardize")
# for i in kb:
    # print(i)
# USE RESOLUTION TO PROVE THAT
# prove = "Kills(Curiosity,Tuna)"