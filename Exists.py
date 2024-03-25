class Exists():
    statement = '('
    variable = ''

    def __init__(self, word: str, skol: list):
        if not word.startswith("Exists("):
            raise Exception(f"An Error has occured inside the class Exists, string:{word} doesn't start with Exists(")
        
        self.variable = word[7:word.find(',')]
        self.statement = word[word.find(', ')+2:-1]
        print(self.statement)

    def changeVariable(self, nVariable: str):
        self.statement = self.statement.replace(self.variable, nVariable)
        self.variable = nVariable

