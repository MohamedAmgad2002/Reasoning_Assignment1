class ForAll():
    def __init__(self, variable: str, word: str, skol: list):
        if not word.startswith("ForAll("):
            raise Exception(f"An Error has occured inside the class ForAll, string doesn't start with ForAll(")
        self.variable = variable
        self.statement = word
        print(self.statement)

    def changeVariable(self, nVariable: str):
        self.statement = self.statement.replace(self.variable, nVariable)
        self.variable = nVariable