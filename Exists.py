class Exists():
    statement = '('
    variable = ''
    
    def __init__(self, variable: str, word: str, *argv):
        if not word.startswith("Exists("):
            raise Exception(f"An Error has occured inside the class Exists, string doesn't start with Exists(")
        self.variable = variable
        for i in range(7, len(word)-1):
            self.statement += word[i]
        self.statement += ')'
        print(self.statement)

    def changeVariable(self, nVariable: str):
        self.statement = self.statement.replace(self.variable, nVariable)

