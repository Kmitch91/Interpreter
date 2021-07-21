

class ScanLine:

    # Constructor
    def __init__(self, linenum, lineStr, lexemes):
        self.lineNum = linenum
        self.lineStr = lineStr
        self.lexemes = lexemes

    def getLineNum(self):
        return self.lineNum

    def getLineStr(self):
        return self.lineStr

    def getLexemes(self):
        return self.lexemes

    def setLineNum(self, lineNum):
        self.lineNum = lineNum

    def setLineStr(self, lineStr):
        self.lineStr = lineStr

    def setLexemes(self, lexemes):
        self.lexemes = lexemes
