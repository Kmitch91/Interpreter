from Lexical_Analyzer.Token import Token
from Lexical_Analyzer.Lexeme import Lexeme
from Lexical_Analyzer.ScanLine import ScanLine


class Scanner(object):

    # Constructor
    def __init__(self, filePath):
        self.filePath = filePath
        self.scanLines = []
        self.scan()

    def addScanLine(self, newScanLine):
        self.scanLines.append(newScanLine)

    def clearScanLine(self):
        return self.scanLines

    def getScanLines(self):
        return self.scanLines

    @staticmethod
    def modSplitLine(line):
        originalSplitLine = line.split()

        currentWordIndex = 0
        beginQuoteIndex = None
        endQuoteIndex = None

        newSplitLine = []

        for word in originalSplitLine:
            if word.find("\"") != -1:
                # If the word is a str literal with no whitespace
                if word[0] == "\"" and word[len(word) - 1] == "\"":
                    newSplitLine.append(word)
                # If no string literal construction has been detected yet
                elif beginQuoteIndex is None:
                    beginQuoteIndex = currentWordIndex
                # If string literal construction has been detected but not finished
                elif endQuoteIndex is None:
                    endQuoteIndex = currentWordIndex

                    # Append a joined string of every element from beginQuoteIndex to endQuoteIndex + 1
                    newSplitLine.append(" ".join(originalSplitLine[beginQuoteIndex: endQuoteIndex + 1]))
                    beginQuoteIndex = None
                    endQuoteIndex = None


            # If there is not an ongoing string detection
            elif beginQuoteIndex is None and endQuoteIndex is None:
                # If current word is the last word on the line
                if word == originalSplitLine[len(originalSplitLine) - 1]:
                    # If there is a ';' at the end of the word
                    if word[len(word) - 1] == ";":
                        newSplitLine.append(word[:-1])
                        newSplitLine.append(";")
                    else:
                        newSplitLine.append(word)
                else:
                    newSplitLine.append(word)


            currentWordIndex += 1

        return newSplitLine

    def scan(self):

        # Opens file in read-only mode
        File = open(self.filePath, "r")

        variables = {}

        if(File.mode == "r"):
            lines = File.readlines()
            lineNumber = 1

            for line in lines:
                splitLine = Scanner.modSplitLine(line)

                lexemes = []

                trimmedLine = line.strip('    ')

                lineSize = len(splitLine)

                firstWord = splitLine[0] if lineSize >= 1 else ""
                secondWord = splitLine[1] if lineSize >= 2 else ""

                for word in splitLine:
                    detectedToken = Token.findToken(word)

                    # Detection for second word
                    if word == secondWord:
                        if detectedToken is not Token.NOT_DEFINED:
                            lexemes.append(Lexeme(word, detectedToken))

                        else:
                            if Token.findToken(firstWord) == Token.INT_KEYWORD:
                                lexemes.append(Lexeme(word, Token.INTEGER_IDENTIFIER))
                                variables[word] = Token.INTEGER_IDENTIFIER
                            elif Token.findToken(firstWord) == Token.DOUBLE_KEYWORD:
                                lexemes.append(Lexeme(word, Token.DOUBLE_IDENTIFIER))
                                variables[word] = Token.DOUBLE_IDENTIFIER
                            elif Token.findToken(firstWord) == Token.STRING_KEYWORD:
                                lexemes.append(Lexeme(word, Token.STRING_IDENTIFIER))
                                variables[word] = Token.STRING_IDENTIFIER
                            elif Token.findToken(firstWord) == Token.BOOL_KEYWORD:
                                lexemes.append(Lexeme(word, Token.BOOLEAN_IDENTIFIER))
                                variables[word] == Token.BOOLEAN_IDENTIFIER
                            else:
                                if word in variables:
                                    lexemes.append(Lexeme(word, variables[word]))
                                else:
                                    lexemes.append(Lexeme(word, Token.NOT_DEFINED))

                        continue

                    if Token.findToken(word) != Token.NOT_DEFINED:
                        lexemes.append(Lexeme(word, Token.findToken(word)))
                        continue

                    if Token.findToken(word) == Token.NOT_DEFINED:
                        if word in variables:
                            lexemes.append(Lexeme(word, variables[word]))
                        else:
                            lexemes.append(Lexeme(word, Token.NOT_DEFINED))
                        continue

                scanLine = ScanLine(lineNumber, trimmedLine, lexemes)
                self.addScanLine(scanLine)
                lineNumber += 1

        self.variables = variables
        File.close()