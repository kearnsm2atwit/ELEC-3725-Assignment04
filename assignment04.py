
## Function for taking in raw string from file and returning array of each part of the instruction.
## Function also needs to strip the commas and Xs from the string as they aren't needed
## Used info from: https://docs.python.org/2.5/lib/string-methods.html

def parseInstruction(instruction):
    returnArray = []
    returnArray = instruction.split()
    for i in range(0, len(returnArray)):
        returnArray[i] = returnArray[i].strip('X,')
    return returnArray


## Function that takes file variable and returns array of each part of the instruction
def setupInstruction(file):
    temp_firstFile = code1.readlines()
    returnValue = []
    for i in range(0, len(temp_firstFile)):
        returnValue.append(parseInstruction(temp_firstFile[i]))
    return returnValue




## Need to open, read, and write text files
## https://www.geeksforgeeks.org/reading-writing-text-files-python/

code1 = open("code1.txt", "r")
code2 = open("code2.txt", "r")
code3 = open("code3.txt", "r")


firstInstruction = setupInstruction(code1)

for i in range(0, len(firstInstruction)):
    for j in range(1,len(firstInstruction[i])):
        firstInstruction[i][j] = bin(int(firstInstruction[i][j]))
        firstInstruction[i][j] = firstInstruction[i][j].lstrip('0b')

print(firstInstruction)
## Function for creating binary for ADD function

