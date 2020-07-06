## Dictionary of OP-codes
legv8 = {
    "ADD": "10001011000",
    "SUB": "11001011000",
    "AND": "10001010000",
    "ORR": "10101010000",
    "EOR": "11101010000",
    "LSL": "11010011011",
    "LSR": "11010011010",
    "ADDI": "1001000100",
    "SUBI": "1101000100",
    "ANDI": "1001001000",
    "ORRI": "1011001000",
    "EORI": "1101001000",
    "SUBS": "11101011000",
    "SUBIS": "11110001000",
    "LDUR": "11111000010",
    "STUR": "11111000000",
    "CBZ": "10110100",
    "CBNZ": "10110101",
    "B": "000101",
    "B.EQ": "010101000000",
    "B.NE": "010101000001",
    "B.GT": "010101001100",
    "B.GTE": "010101001010",
    "B.LT": "010101001011",
    "B.LTE": "010101001101"
}

rCodes =  ["ADD", "AND", "ORR", "ADDS", "EOR", "SUB", "LSR", "LSL", "BR", "ANDS", "SUBS"]
iCodes =  ["ORRI", "EORI", "ADDI", "ANDI", "ADDIS", "SUBI", "SUBIS", "ANDIS"]
dCodes =  ["STUR", "LDUR"]
bCodes =  ["B"]
cbCodes = ["CBZ", "CBNZ", "B.EQ", "B.NE", "B.GT", "B.GTE", "B.LT", "B.LTE"]

## Function for taking in raw string from file and returning array of each part of the instruction.
## Function also needs to strip the commas and Xs from the string as they aren't needed
## Used info from: https://docs.python.org/2.5/lib/string-methods.html
def parseInstruction(instruction):
    returnArray = []
    returnArray = instruction.split()
    for i in range(0, len(returnArray)):
        returnArray[i] = returnArray[i].strip('X,#[]')
    return returnArray


## Function that takes file variable and returns array of each part of the instruction
def setupInstruction(file):
    temp_firstFile = file.readlines()
    returnValue = []
    for i in range(0, len(temp_firstFile)):
        returnValue.append(parseInstruction(temp_firstFile[i]))
    return returnValue

## Function for taking in instruction as an array and turning all decimals to binary values
def instructionToBinary(instruction):
    for i in range(0, len(instruction)):
        for j in range(1,len(instruction[i])):
            if(instruction[i][j] == "ZR"):
                instruction[i][j] = "0"
            instruction[i][j] = bin(int(instruction[i][j]))
            instruction[i][j] = instruction[i][j].lstrip('0b')
            if(instruction[i][j] == ''):
                instruction[i][j] = '0'
    return instruction

## Function to keep leading zeros. Will help with binary codes that are 4 bits but need to be 5 or something similar
def leadingZeros(length, string):
    returnValue = ""
    stringAsList = list(string)
    numOfZeros = length - len(stringAsList)
    for i in range(numOfZeros):
        stringAsList.insert(0, "0")
    for i in range(0, len(stringAsList)):
        returnValue += stringAsList[i]
    return returnValue


def rFormat(instruction):
    if(instruction[0] == "LSL" or instruction[0] == "LSR" or instruction[0] == "BR"):
        opcode = leadingZeros(11, legv8[instruction[0]])
        rm = leadingZeros(5, "0")
        shamt = leadingZeros(6, instruction[3])
        rn = leadingZeros(5, instruction[2])
        rd = leadingZeros(5, instruction[1])
        returnValue = opcode + " " + rm + " " +  shamt + " " + rn + " " + rd
    else:
        opcode = leadingZeros(11, legv8[instruction[0]])
        rm = leadingZeros(5, instruction[3])
        shamt = leadingZeros(6, "0")
        rn = leadingZeros(5, instruction[2])
        rd = leadingZeros(5, instruction[1])
        returnValue = opcode + " " + rm + " " +  shamt + " " + rn + " " + rd
    return returnValue

def iFormat(instruction):
    pass

def dFormat(instruction):
    pass

def bFormat(instruction):
    pass

def cbFormat(instruction):
    pass




## Need to open, read, and write text files
## https://www.geeksforgeeks.org/reading-writing-text-files-python/

code1 = open("code1.txt", "r")
code2 = open("code2.txt", "r")
code3 = open("code3.txt", "r")


firstInstruction = setupInstruction(code1)
firstInstruction = instructionToBinary(firstInstruction)
#print(firstInstruction)

for i in firstInstruction:
    print(rFormat(i))