from Parser.Parser import Parser
from Parser.NodeType import NodeType
from Parser.Node import Node
from Lexical_Analyzer.Token import Token
from Lexical_Analyzer.Lexeme import Lexeme
import re

class Interpreter(Parser):

    def __init__(self, filePath):
        Parser.__init__(self, filePath)

    def interpret(self):
        print("Parsing SCL File", "\n")
        parseTree = super().parse()
        print("\nFinished Parsing File")
        print("="*50, "\n")

        # Iterate through all of <program> node's direct children
        for node in parseTree.getRoot().getChildren():
            if Node.getNodeType() is NodeType.DECLARE:
                self.interpretDeclare(node)
            if Node.getNodeType() is NodeType.ASSIGNMENT:
                self.interpretAssignment(node)
            if Node.getNodeType() is NodeType.PRINT_METHOD:
                pass
            if Node.getNodeType() is NodeType.IF_STMT:
                self.interpretIf(node)
            if Node.getNodeType() is NodeType.WHILE_LOOP:
                self.interpretWhile(node)

    def interpretDeclare(self, node):
        for child in node.getChildren():
            if node.getNodeType() is NodeType.TERM:
                self.interpretTerm(child)

    def interpretTerm(self, node):
        for child in node.getChildren():
            if node.getNodeType() is NodeType.FACTOR:
                self.interprettFactor(child)

    def interpretAssignment(self, node):
        for child in node.getChildren():
            if node.getNodeType() is NodeType.TERM:
                self.interpretTerm(child)

    def interpretIf(self, node):
        for child in node.getChildren():
            if node.getNodeType() is NodeType.ASSIGNMENT:
                self.interpretAssignment(child)

    def interpretWhile(self, node):
        for child in node.getChildren():
            if node.getNodeType() is NodeType.ASSIGNMENT:
                self.interpretAssignment(child)

    def interpretPtint(self, node):
        lexemes = node.getScanLine().getLexmes()
        if lexemes[0].getToken() is Token.PRINT_KEYWORD:
           val = Token.INTEGER_IDENTIFIER
           print(val)

    # Multiplies the two top elements in postFixList
    def mulOper(self, postFixList):
        varTwo = postFixList.pop()
        varOne = postFixList.pop()

        valOne = None
        valTwo = None

        # Find value of first variable
        if Token.findToken(varOne) is Token.INTEGER_LITERAL:
            valOne = int(varOne)
        elif Token.findToken(varOne) is Token.DOUBLE_LITERAL:
            valOne = float(varOne)
        else:
            varOneType = self.getVarType(varOne)
            if varOneType is Token.INT_KEYWORD:
                valOne = int(self.getVarValue(varOne))
            elif varOneType is Token.DOUBLE_KEYWORD:
                valOne = float(self.getVarValue(varOne))

        # Find value of second variable
        if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
            valTwo = int(varTwo)
        elif Token.findToken(varTwo) is Token.DOUBLE_LITERAL:
            valTwo = float(varTwo)
        else:
            varTwoType = self.getVarType(varTwo)
            if varTwoType is Token.INT_KEYWORD:
                valTwo = int(self.getVarValue(varTwo))
            elif varTwoType is Token.DOUBLE_KEYWORD:
                valTwo = float(self.getVarValue(varTwo))

        result = valOne * valTwo
        postFixList.append(str(result))

    # Divides the two top elements in postFixList
    def divOper(self, postFixList):
        varTwo = postFixList.pop()
        varOne = postFixList.pop()

        valOne = None
        valTwo = None

        # Find value of first variable
        if Token.findToken(varOne) is Token.INTEGER_LITERAL:
            valOne = int(varOne)
        elif Token.findToken(varOne) is Token.DOUBLE_LITERAL:
            valOne = float(varOne)
        else:
            varOneType = self.getVarType(varOne)
            if varOneType is Token.INT_KEYWORD:
                valOne = int(self.getVarValue(varOne))
            elif varOneType is Token.DOUBLE_KEYWORD:
                valOne = float(self.getVarValue(varOne))

        # Find value of second variable
        if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
            valTwo = int(varTwo)
        elif Token.findToken(varTwo) is Token.DOUBLE_LITERAL:
            valTwo = float(varTwo)
        else:
            varTwoType = self.getVarType(varTwo)
            if varTwoType is Token.INT_KEYWORD:
                valTwo = int(self.getVarValue(varTwo))
            elif varTwoType is Token.DOUBLE_KEYWORD:
                valTwo = float(self.getVarValue(varTwo))

        result = valOne / valTwo
        postFixList.append(str(result))

    # Adds
    def addOper(self, postFixList):
        varTwo = postFixList.pop()
        varOne = postFixList.pop()

        valOne = None
        valTwo = None

        # Find value of first variable
        if Token.findToken(varOne) is Token.INTEGER_LITERAL:
            valOne = int(varOne)
        elif Token.findToken(varOne) is Token.DOUBLE_LITERAL:
            valOne = float(varOne)
        else:
            varOneType = self.getVarType(varOne)
            if varOneType is Token.INT_KEYWORD:
                valOne = int(self.getVarValue(varOne))
            elif varOneType is Token.DOUBLE_KEYWORD:
                valOne = float(self.getVarValue(varOne))

        # Find value of second variable
        if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
            valTwo = int(varTwo)
        elif Token.findToken(varTwo) is Token.DOUBLE_LITERAL:
            valTwo = float(varTwo)
        else:
            varTwoType = self.getVarType(varTwo)
            if varTwoType is Token.INT_KEYWORD:
                valTwo = int(self.getVarValue(varTwo))
            elif varTwoType is Token.DOUBLE_KEYWORD:
                valTwo = float(self.getVarValue(varTwo))

        result = valOne + valTwo
        postFixList.append(str(result))

    # Subtracts
    def dsubOper(self, postFixList):
        varTwo = postFixList.pop()
        varOne = postFixList.pop()

        valOne = None
        valTwo = None

        # Find value of first variable
        if Token.findToken(varOne) is Token.INTEGER_LITERAL:
            valOne = int(varOne)
        elif Token.findToken(varOne) is Token.DOUBLE_LITERAL:
            valOne = float(varOne)
        else:
            varOneType = self.getVarType(varOne)
            if varOneType is Token.INT_KEYWORD:
                valOne = int(self.getVarValue(varOne))
            elif varOneType is Token.DOUBLE_KEYWORD:
                valOne = float(self.getVarValue(varOne))

        # Find value of second variable
        if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
            valTwo = int(varTwo)
        elif Token.findToken(varTwo) is Token.DOUBLE_LITERAL:
            valTwo = float(varTwo)
        else:
            varTwoType = self.getVarType(varTwo)
            if varTwoType is Token.INT_KEYWORD:
                valTwo = int(self.getVarValue(varTwo))
            elif varTwoType is Token.DOUBLE_KEYWORD:
                valTwo = float(self.getVarValue(varTwo))

        result = valOne - valTwo
        postFixList.append(str(result))

