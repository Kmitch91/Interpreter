


from Evaluator.Interpreter import Interpreter

inputPath = "C:\\Users\\koyam\\PycharmProjects\\Interpreter\\declareTest"

outputPath = "InterpreterTestOutput.txt"

# Output file
testFile = open(outputPath, "w")

# Creates Parser object
interpreter = Interpreter(inputPath)

print("="*50, "\n")

# Performs python interpretation
interpreter.interpret()
