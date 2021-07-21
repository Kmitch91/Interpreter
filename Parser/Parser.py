from Lexical_Analyzer.Scanner import Scanner
from Lexical_Analyzer.Token import Token
from Parser.Node import Node
from Parser.NodeType import NodeType
from Parser.Tree import Tree


class Parser(Scanner):

    def __init__(self, filePath):
        Scanner.__init__(self, filePath)
        self.currentLineNum = 0
        self.lexemeNumber = 0
        self.currentToken = None
        self.scanLines = super().getScanLines()
        self.printLines = []

    def parse(self):
        root = Node(None, None, NodeType.PROGRAM)
        self.modPrint("Parsing " + str(root.getNodeType().value))
        lexeme = self.nextLexeme()

        self.currentToken = lexeme.getToken()
        while self.currentLineNum < len(self.scanLines) - 1:
            if 29 <= self.currentToken.getNumCode() <= 32:
                self.parseDeclare(root)
                continue
            elif 2 <= self.currentToken.getNumCode() <= 5:
                self.parseAssignment(root)
                continue
            elif self.currentToken is Token.PRINT_KEYWORD:
                self.parsePrint(root)
                continue
            elif self.currentToken is Token.IF_KEYWORD:
                self.parseIfStmt(root)
                continue
            elif self.currentToken is Token.WHILE_KEYWORD:
                self.parseWhile(root)
                continue
            elif self.currentToken is Token.NOT_DEFINED:
                # todo make this
                continue

            else:
                self.nextToken()

        self.modPrint("Finished parsing " + str(root.getNodeType().value))
        return Tree(root)

    def modPrint(self, txt):
        print(str(txt))
        self.printLines.append(str(txt))

    def nextLexeme(self):
        # If lexeme number is more than the index length -1 then increment line by 1 and reset lexeme number
        if self.lexemeNumber >= len(self.scanLines[self.currentLineNum].getLexemes()):
            self.currentLineNum += 1
            self.lexemeNumber = 0
            # If the current line number is more than the index amount length of lines then stop
            if self.currentLineNum >= len(self.scanLines):
                return
        result = self.scanLines[self.currentLineNum].getLexemes()[self.lexemeNumber]
        self.lexemeNumber += 1
        return result

    def nextToken(self):
        self.currentToken = self.nextLexeme().getToken()

    def errorMsg(self, reason=""):
        msg = "Error at line " + str(self.currentLineNum) + ": \n"
        msg += "Reason: " + str(reason) + "\n\t\""
        msg += self.scanLines[self.currentLineNum].getLineStr()[0:-1] + "\""
        self.modPrint(msg)

    def parseFactor(self, node):
        factorNode = Node(node, self.scanLines[self.currentLineNum], NodeType.FACTOR)
        node.addChildNode(factorNode)
        self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(factorNode.getNodeType().value))

        if 2 <= self.currentToken.getNumCode() <= 9:
            self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(factorNode.getNodeType().value))
            return True

        else:
            self.errorMsg("Invalid Factor")
            node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
            return False

    def parseTerm(self, node):
        termNode = Node(node, self.scanLines[self.currentLineNum], NodeType.TERM)
        node.addChildNode(termNode)
        self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(termNode.getNodeType().value))
        self.parseFactor(termNode)

        if len(termNode.getChildren()) == 0:
            self.errorMsg("Invalid Term")
            node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
            return False

        self.nextToken()
        if 19 <= self.currentToken.getNumCode() <= 20:
            while 19 <= self.currentToken.getNumCode() <= 20:
                self.nextToken()
                if self.parseFactor(termNode) == True:
                    self.nextToken()
                else:
                    self.errorMsg("Missing Factor")
                    node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                    return False

        self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(termNode.getNodeType().value))
        return True

    def parseExpr(self, node):
        exprNode = Node(node, self.scanLines[self.currentLineNum], NodeType.EXPR)
        node.addChildNode(exprNode)
        self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(exprNode.getNodeType().value))
        self.parseTerm(exprNode)

        if len(exprNode.getChildren()) == 0:
            self.errorMsg("Invalid Expression")
            node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
            return False

        if 17 <= self.currentToken.getNumCode() <= 18:
            while 17 <= self.currentToken.getNumCode() <= 18:
                self.nextToken()
                if self.parseTerm(exprNode) == True:
                    self.nextToken()
                else:
                    self.errorMsg("Missing Term")
                    node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                    return False

        self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(exprNode.getNodeType().value))
        return True

    def parseDeclare(self, node):
        declareNode = Node(node, self.scanLines[self.currentLineNum], NodeType.DECLARE)
        node.addChildNode(declareNode)
        self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(declareNode.getNodeType().value))

        typeNumCode = self.currentToken.getNumCode()
        self.nextToken()
        if typeNumCode - self.currentToken.getNumCode() == 27:
            self.nextToken()
            if self.currentToken is Token.ASSIGNMENT_OPERATOR:
                self.nextToken()
                if self.parseExpr(declareNode) == True:
                    if self.currentToken is Token.SEMICOLON:
                        self.nextToken()
                    else:
                        self.errorMsg("Missing Semicolon")
                        node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                        return False
                else:
                    self.errorMsg("Invalid Expression")
                    node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                    return False
            else:
                self.errorMsg("Missing '='")
                node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                return False
        else:
            self.errorMsg("Miss-matching Identifier vs Type")
            node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
            return False

        self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(declareNode.getNodeType().value))

    def parseAssignment(self, node):
        assignNode = Node(node, self.scanLines[self.currentLineNum], NodeType.DECLARE)
        node.addChildNode(assignNode)
        self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(assignNode.getNodeType().value))

        if 2 <= self.currentToken.getNumCode() <= 9:
            self.nextToken()
            if self.currentToken is Token.ASSIGNMENT_OPERATOR or 17 <= self.currentToken.getNumCode() <= 20:
                self.nextToken()
                if self.parseExpr(assignNode) == True:
                    if self.currentToken is Token.SEMICOLON:
                        self.nextToken()
                    else:
                        self.errorMsg("Missing Semicolon")
                        node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                        return False
                else:
                    self.errorMsg("Invalid Expression")
                    node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                    return False
            else:
                self.errorMsg("Missing '='")
                node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                return False
        else:
            self.errorMsg("Miss-matching Identifier")
            node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
            return False

    def parsePrint(self, node):
        printNode = Node(node, self.scanLines[self.currentLineNum], NodeType.PRINT_METHOD)
        node.addChildNode(printNode)
        self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(printNode.getNodeType().value))

        if self.currentToken is Token.PRINT_KEYWORD:
            self.nextToken()
            if 2 <= self.currentToken.getNumCode() <= 5:
                self.nextToken()
                if self.currentToken is Token.SEMICOLON:
                    self.nextToken()
                else:
                    self.errorMsg("Missing Semicolon")
                    node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                    return False
            else:
                self.errorMsg("Missing Print Statement")
                node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                return False
        else:
            self.errorMsg("Missing Print")
            node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
            return False

        self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(printNode.getNodeType().value))

    def parseIfStmt(self, node):
        ifNode = Node(node, self.scanLines[self.currentLineNum], NodeType.PRINT_METHOD)
        node.addChildNode(ifNode)
        self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(ifNode.getNodeType().value))

        if self.currentToken is Token.IF_KEYWORD:
            self.nextToken()
            if 2 <= self.currentToken.getNumCode() <= 9:
                self.nextToken()
                if 11 <= self.currentToken.getNumCode() <= 16:
                    self.nextToken()
                    if 2 <= self.currentToken.getNumCode() <= 9:
                        self.nextToken()
                        if self.currentToken is Token.THEN_KEYWORD:
                            self.nextToken()
                        else:
                            self.errorMsg("Missing Then")
                            node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                            return False
                    else:
                        self.errorMsg("Missing Argument")
                        node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                        return False
                else:
                    self.errorMsg("Missing Operator")
                    node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                    return False
            else:
                self.errorMsg("Missing Argument")
                node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                return False
        else:
            self.errorMsg("Missing If")
            node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
            return False

        self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(ifNode.getNodeType().value))

    def parseElseStmt(self, node):
        ifNode = Node(node, self.scanLines[self.currentLineNum], NodeType.PRINT_METHOD)
        node.addChildNode(ifNode)
        self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(ifNode.getNodeType().value))

        if self.currentToken is Token.ELSE_KEYWORD:
            self.nextToken()

        self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(ifNode.getNodeType().value))
    def parseWhileStmt(self, node):
        whileNode = Node(node, self.scanLines[self.currentLineNum], NodeType.PRINT_METHOD)
        node.addChildNode(whileNode)
        self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(whileNode.getNodeType().value))

        if self.currentToken is Token.WHILE_KEYWORD:
            self.nextToken()
            if 2 <= self.currentToken.getNumCode() <= 9:
                self.nextToken()
                if 11 <= self.currentToken.getNumCode() <= 16:
                    self.nextToken()
                    if 2 <= self.currentToken.getNumCode() <= 9:
                        self.nextToken()
                        if self.parseExpr(whileNode) == True:
                            if self.currentToken is Token.DO_KEYWORD:
                                self.nextToken()
                            else:
                                self.errorMsg("Missing Do")
                                node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                                return False
                    else:
                        self.errorMsg("Missing Argument")
                        node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                        return False
                else:
                    self.errorMsg("Missing Operator")
                    node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                    return False
            else:
                self.errorMsg("Missing Argument")
                node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
                return False
        else:
            self.errorMsg("Missing While")
            node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
            return False

        self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(whileNode.getNodeType().value))
