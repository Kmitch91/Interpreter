
from enum import Enum
import re

class Token(Enum):

    # Not Defined
    NOT_DEFINED = ["", 1]

    # Identifiers (variable name = identifier ex: int x; x = identifier) ASSIGNMENT
    INTEGER_IDENTIFIER = ["", 2]
    DOUBLE_IDENTIFIER = ["", 3]
    STRING_IDENTIFIER = ["", 4]
    BOOLEAN_IDENTIFIER = ["", 5]

    # Literals (value = literal)
    INTEGER_LITERAL = ["^[-+]?[0-9]+$", 6]
    DOUBLE_LITERAL = ["^[-+]?\d+(\.\d+)?$", 7]
    STRING_LITERAL = ["\".*\"", 8]
    BOOLEAN_LITERAL = ["^true|false$", 9]

    # Operators
    ASSIGNMENT_OPERATOR = ["=", 10]
    LESSEQUAL_OPERATOR = ["<=", 11]
    LESS_OPERATOR = ["<", 12]
    GREATEQUAL_OPERATOR = [">=", 13]
    GREAT_OPERATOR = [">", 14]
    EQUALEQUAL_OPERATOR = ["==", 15]
    NOTEQUAL_OPERATOR = ["!=", 16]
    ADD_OPERATOR = ["\\+", 17]
    SUBTRACT_OPERATOR = ["-", 18]
    MULTIPLY_OPERATOR = ["\\*", 19]
    DIVIDE_OPERATOR = ["/", 20]

    # Keywords 29-32 = DECLARE
    IF_KEYWORD = ["if", 21]
    ELSE_KEYWORD = ["else", 22]
    THEN_KEYWORD = ["then", 23]
    ENDIF_KEYWORD = ["endIf", 24]
    WHILE_KEYWORD = ["while", 25]
    DO_KEYWORD = ["do", 26]
    ENDWHILE_KEYWORD = ["endWhile", 27]
    PRINT_KEYWORD = ["print", 28]
    INT_KEYWORD = ["int", 29]
    DOUBLE_KEYWORD = ["double", 30]
    STRING_KEYWORD = ["string", 31]
    BOOL_KEYWORD = ["bool", 32]

    # Other
    SEMICOLON = [";", 33]


    # Returns lexeme string
    def getLexemePattern(self):
        return self.value[0]

    # Returns numeric code int
    def getNumCode(self):
        return self.value[1]

    # Returns numeric code of token of corresponding regex match
    @staticmethod
    def findNumCode(word):
        for token in Token:
            tokenLexemeMatcher = token.getLexemePattern()
            if len(re.findall(tokenLexemeMatcher, word)) == 1:
                return token.getNumCode()
        return  -1

    # If no regex match is found then returns Token.py.NOT_DEFINED
    @staticmethod
    def findToken(word):
        for token in Token:
            tokenLexemeMatcher = token.getLexemePattern()
            if len(re.findall(tokenLexemeMatcher, word)) == 1:
                return token
        return Token.NOT_DEFINED


