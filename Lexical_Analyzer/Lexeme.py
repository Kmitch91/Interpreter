class Lexeme:

    # Constructor
    def __init__(self, lexStr, token):
        self.lexStr = lexStr
        self.token = token

    def getLexemeString(self):
        return self.lexStr

    def getToken(self):
        return self.token
