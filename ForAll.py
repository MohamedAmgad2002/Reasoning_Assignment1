class ForAll():
    statement = '('
    variable = ''
    skol = []
    pre = 'ForAll('
    def __init__(self, word: str, skol2: list):
        if not word.startswith("ForAll("):
            raise Exception(f"An Error has occured inside the class ForAll, string:{word} doesn't start with ForAll(")

        self.variable = word[7:word.find(',')]
        self.statement = word[word.find(', ')+2:-1]
        self.skol = skol2.copy()
        print(self.statement)

    def changeVariable(self, newVariable: str):
        # print('-=-=-=-=-=-')
        # print(self.statement)
        self.statement = self.statement.replace('('+self.variable, '('+newVariable)
        self.statement = self.statement.replace(self.variable+',', newVariable+',')
        self.statement = self.statement.replace(','+self.variable, ','+newVariable)
        # print(self.statement)
        self.pre = self.pre.replace('('+self.variable, '('+newVariable)
        self.variable = newVariable
        # ['('+self.variable] or [self.variable+',']

    def changeOtherVariable(self, var1: str, var2: str):
        self.statement = self.statement.replace('('+var1, '('+var2)
        self.statement = self.statement.replace(var1+',', var2+',')
        self.statement = self.statement.replace(','+var1, ','+var2)
        # print(self.skol)
        ndx = -1
        for i in range(len(self.skol)):
            if self.skol[i] == var1:
                ndx = i
                break
        if ndx != -1:
            self.skol[ndx] = var2
