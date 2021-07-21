from Lexical_Analyzer.Scanner import Scanner

# Enter absolute path of testCase.txt file location here
inputPath = "C:\\Users\\koyam\\Desktop\\testCase.txt"

#Path of output file
outputPath = "ScannerTestOutput.txt"

#Output file
testFile = open(outputPath, "w")




# Creates Scanner object which contains Lexical Analysis data on  file input
scanner = Scanner(inputPath)

# Performs Lexical Analysis
testFile.write("="*50)
for scanLine in scanner.getScanLines():
	lexemes = scanLine.getLexemes()
	lineNumber = scanLine.getLineNum()
	lineString = scanLine.getLineStr()
	testFile.write("\n" + "-"*40)
	labelText = "\nLine " + str(lineNumber) + ": " + lineString + "\n"
	testFile.write(labelText)
	for lexeme in lexemes:
		lexemeStr = lexeme.getLexemeString()
		token = lexeme.getToken()
		testFile.write("Lexeme: {:15} \t Token: {}\n".format(lexemeStr, token.name))
	bottomFormatText = "-"*40 + "\n\n"
	testFile.write(bottomFormatText)
