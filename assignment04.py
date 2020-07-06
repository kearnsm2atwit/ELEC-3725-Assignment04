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

    ## Need to fix b.cond opcodes
    "B.EQ": "0000",
    "B.NE": "0001",
    "B.GT": "1100",
    "B.GE": "1010",
    "B.LT": "1011",
    "B.LE": "1101"
}

rCodes =  ["ADD", "AND", "ORR", "ADDS", "EOR", "SUB", "LSR", "LSL", "BR", "ANDS", "SUBS"]
iCodes =  ["ORRI", "EORI", "ADDI", "ANDI", "ADDIS", "SUBI", "SUBIS", "ANDIS"]
dCodes =  ["STUR", "LDUR"]
bCodes =  ["B"]
cbCodes = ["CBZ", "CBNZ", "B.EQ", "B.NE", "B.GT", "B.GE", "B.LT", "B.LE"]

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
                instruction[i][j] = "31"
            instruction[i][j] = bin(int(instruction[i][j]))
            instruction[i][j] = instruction[i][j].lstrip('0b')
            if(instruction[i][j] == ''):
                instruction[i][j] = '0'
    return instruction

## Function to keep leading zeros. Will help with binary codes that are 4 bits but need to be 5 or something similar
def leadingZeros(length, string, signed):
    ## Do twos complement for signed bin
    if (signed):
        invertBin = 0xFFFFFFFFFFFF
        tempString = int(string)
        bitString = str(length) + "b"
        print(invertBin)
        print(bitString)
        temp_returnValue = (tempString & invertBin)
        return bin(tempString & invertBin)

    else:
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
        opcode = leadingZeros(11, legv8[instruction[0]], False)
        rm = leadingZeros(5, "0", False)
        shamt = leadingZeros(6, instruction[3], False)
        rn = leadingZeros(5, instruction[2], False)
        rd = leadingZeros(5, instruction[1], False)
        returnValue = opcode + " " + rm + " " +  shamt + " " + rn + " " + rd
    else:
        opcode = leadingZeros(11, legv8[instruction[0]], False)
        rm = leadingZeros(5, instruction[3], False)
        shamt = leadingZeros(6, "0", False)
        rn = leadingZeros(5, instruction[2], False)
        rd = leadingZeros(5, instruction[1], False)
        returnValue = opcode + " " + rm + " " +  shamt + " " + rn + " " + rd
    return returnValue

def iFormat(instruction):
    opcode = leadingZeros(10, legv8[instruction[0]], False)
    immediate = leadingZeros(12, instruction[3], False)
    rn = leadingZeros(5, instruction[2], False)
    rd = leadingZeros(5, instruction[1], False)
    returnValue = opcode + " " + immediate + " " + rn + " " + rd
    return returnValue

def dFormat(instruction):
    opcode = leadingZeros(11, legv8[instruction[0]], False)
    address = leadingZeros(9, instruction[3], False)
    rn = leadingZeros(5, instruction[2], False)
    rt = leadingZeros(5, instruction[1], False)
    returnValue = opcode + " " + address + " " + "00" + " " + rn + " " + rt
    return returnValue

def bFormat(instruction):
    opcode = leadingZeros(6, legv8[instruction[0]], False)
    address = leadingZeros(26, instruction[1], True)
    returnValue = opcode + " " + address
    return returnValue

def cbFormat(instruction):
    if (instruction[0][0] == "B"):
        opcode = leadingZeros(8, "01010100", False)
        address = leadingZeros(19, instruction[1], True)
        rt = leadingZeros(5, legv8[instruction[0]], False)
        returnValue = opcode + " " + address + " " + rt
    else:
        opcode = leadingZeros(8, legv8[instruction[0]], False)
        address = leadingZeros(19, instruction[2], True)
        rt = leadingZeros(5, instruction[1], False)
        returnValue = opcode + " " + address + " " + rt
    return returnValue


def selectFormat(instruction):
    for i in range(0, len(rCodes)):
        if (instruction[0] == rCodes[i]):
            return rFormat(instruction)
    for i in range(0, len(iCodes)):
        if (instruction[0] == iCodes[i]):
            return iFormat(instruction)
    for i in range(0, len(dCodes)):
        if (instruction[0] == dCodes[i]):
            return dFormat(instruction)
    for i in range(0, len(bCodes)):
        if (instruction[0] == bCodes[i]):
            return bFormat(instruction)
    for i in range(0, len(cbCodes)):
        if (instruction[0] == cbCodes[i]):
            return cbFormat(instruction)


## Need function for exit and loop. Parameter is a list of lists
def firstPass(instructions):
    for i in range(0, len(instructions)):
        if (instructions[i][0] == "Loop:"):
            j = i
            while(instructions[j][1] != "Loop"):
                j += 1
            instructions[i].pop(0)
            instructions[j][1] = str(bin(j).lstrip('-0b'))
        if (instructions[i][1] == "Exit"):
            j = i
            while(instructions[j][0] != "Exit:"):
                j += 1
            instructions[j].pop(0)
            instructions[i][1] = str(bin(j).lstrip('0b'))
    return instructions


## Need to open, read, and write text files
## https://www.geeksforgeeks.org/reading-writing-text-files-python/

code1 = open("code1.txt", "r")
code2 = open("code2.txt", "r")
code3 = open("code3.txt", "r")


firstInstruction = setupInstruction(code3)
firstInstruction = firstPass(firstInstruction)
firstInstruction = instructionToBinary(firstInstruction)


for i in range(0, len(firstInstruction)):
    #selectFormat(firstInstruction[i])
    print(firstInstruction[i])
    print(selectFormat(firstInstruction[i]))