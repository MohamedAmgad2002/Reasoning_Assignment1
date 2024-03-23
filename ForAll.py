class ForAll():
    def __init__(self, word: str):
        if not word.startswith("ForAll("):
            raise Exception(f"An Error has occured inside the class ForAll, string doesn't start with ForAll(")
        for i in range(7, len(word)-1):
            print(i, end='')