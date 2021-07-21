

from Parser.Parser import Parser

inputPath = "C:\\Users\\koyam\\PycharmProjects\\Interpreter\\declareTest"
outputPath = "ParserTestOutput.txt"

# Output file
testFile = open(outputPath, "w")

# Creates SCL_Parser object
parser = Parser(inputPath)

# Performs syntax analysis
parseTree = parser.parse()

testFile.write("="*50 + "\n")
for printLine in parser.printLines:
	testFile.write(printLine + "\n")