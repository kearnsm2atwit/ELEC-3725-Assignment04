## Dictionary of OP-codes
legv8 = {
    "10001011000" : "ADD",
    "11001011000" : "SUB",
    "10001010000" : "AND",
    "10101010000" : "ORR",
    "11101010000" : "EOR",
    "11010011011" : "LSL",
    "11010011010" : "LSR",
    "1001000100" : "ADDI",
    "1101000100" : "SUBI",
    "1001001000" : "ANDI",
    "1011001000" : "ORRI",
    "1101001000" : "EORI",
    "11101011000" : "SUBS",
    "11110001000" : "SUBIS",
    "11111000010" : "LDUR",
    "11111000000" : "STUR",
    "10110100" : "CBZ",
    "10110101" : "CBNZ",
    "000101" : "B",

    ## Need to fix b.cond opcodes
    "B.EQ": "0000",
    "B.NE": "0001",
    "B.GT": "1100",
    "B.GE": "1010",
    "B.LT": "1011",
    "B.LE": "1101"
}

rCodes =  ["ADD", "AND", "ORR", "EOR", "SUB", "LSR", "LSL", "SUBS"]
iCodes =  ["ORRI", "ADDI", "ANDI", "SUBI", "SUBIS", "EORI"]
dCodes =  ["STUR", "LDUR"]
bCodes =  ["B"]
cbCodes = ["CBZ", "CBNZ", "B.EQ", "B.NE", "B.GT", "B.GE", "B.LT", "B.LE"]

code1 = open("code3_dec.txt", "r")  #input binary file
lines = 0
PC = 0
IR = ""
for line in code1:
    lines += 1
code1.seek(0)
reg = [0]
for i in range(31):
    reg.append(0)
#print(len(reg))
dmem = [0,0,0,0,0,0,0,0,0,0]
#       0 1 2 3 4 5 6 7 8 9 use this for presetting dmem values
#print(dmem, len(dmem))
imem = ["0"]
imem[0] = code1.readline()
imem[0] = imem[0].strip("\n")
for i in range(lines - 1):
    imem.append(code1.readline())
    imem[i + 1] = imem[i + 1].strip("\n")
def printRegs(yes):
    if yes == 1:
       for i in range(len(imem)):
          print("IMEM[",i,"]=",imem[i], end='\t', sep="")
          if (((i+1)%3 == 0) & (i > 1)):
              print("")
       print('\n')
    for i in range(len(dmem)):
        print("DMEM[", i, "]=", dmem[i], end='\t', sep="")
    print('\n')

    for i in range(len(reg)):
        print("REG[", i, "]=", reg[i], end='\t', sep="")
        if (((i+1)%11 == 0) & (i > 1)):
            print("")
    print("")

def instructionType(opcode):
    for i in range(0, len(rCodes)):
        if (opcode == rCodes[i]):
            return (rCodes[i] + ' R')
    for i in range(0, len(iCodes)):
        if (opcode == iCodes[i]):
            return (iCodes[i] + ' I')
    for i in range(0, len(dCodes)):
        if (opcode == dCodes[i]):
            return (dCodes[i] + ' D')
    for i in range(0, len(bCodes)):
        if (opcode == bCodes[i]):
            return (bCodes[i] + ' B')
    for i in range(0, len(cbCodes)):
        if (opcode == cbCodes[i]):
            return (cbCodes[i] + ' CB')
def decode(IR, type):
    print(IR)
    global reg
    if type[1] == 'R':
        reg[0] = int(IR[1],2)  #Rm         rm = 0
        reg[1] = int(IR[2],2)  #shamt      shamt = 1
        reg[2] = int(IR[3],2)  #Rn         rn = 2
        reg[3] = int(IR[4],2)  #Rd         rd = 3
    elif type[1] == 'I':       #immediate = 4
        reg[4] = int(IR[1],2)  #immediate  address = 5
        reg[2] = int(IR[2],2)  #Rn         op2 = 6
        reg[3] = int(IR[3],2)  #Rd         rt = 7
    elif type[1] == 'D':
        reg[5] = int(IR[1],2)  #address
        reg[6] = int(IR[2],2)  #op2
        reg[2] = int(IR[3],2)  #Rn
        reg[7] = int(IR[4],2)  #Rt
    elif type[1] == 'B':
        temp = IR[1]
        if temp[0] == '1':
            temp = int(IR[1],2) - 67108864
            IR[1] = bin(temp)
        reg[5] = int(IR[1],2)  #address
    elif type[1] == 'CB':
        print("cb value", IR[1])
        temp = IR[1]
        if temp[0] == '1':
            temp = int(IR[1], 2) - 524288
            IR[1] = bin(temp)
        reg[5] = int(IR[1],2)  #address
        reg[7] = int(IR[2],2)  #Rt

def Fetch():    #main
    global IR, PC, imem
    printRegs(1)
    while PC < len(imem):
        IR = imem[PC]
        IR = IR.split(" ")
        PC = PC+1
        #print(IR)
        #print(IR[0])
        opcode = legv8[IR[0]]
        type = instructionType(opcode)
        print(type)
        type = type.split(" ")
        decode(IR, type)
        if type[1] == 'R':
            rType(type)
        elif type[1] == 'I':
            iType(type)
        elif type[1] == 'D':
            dType(type)
        elif type[1] == 'B':
            bType(type)
        elif type[1] == 'CB':
            cbType(type)
        if type[1] == 'D' :
            accessMem(type)
    printRegs(1)
def rType(type):
    global reg
    if type[0] == 'ADD':
        reg[reg[3]] = reg[reg[0]] + reg[reg[2]]
    elif type[0] == 'AND':
        reg[reg[3]] = reg[reg[0]] & reg[reg[2]]
    elif type[0] == 'ORR':
        reg[reg[3]] = reg[reg[0]] | reg[reg[2]]
    elif type[0] == 'EOR':
        reg[reg[3]] = reg[reg[0]] ^ reg[reg[2]]
    elif type[0] == 'SUB':
        reg[reg[3]] = reg[reg[2]] - reg[reg[0]]
    elif type[0] == 'LSR':
        reg[reg[3]] = reg[reg[0]] >> reg[1]
    elif type[0] == 'LSL':
        reg[reg[3]] = reg[reg[0]] << reg[1]
    elif type[0] == 'SUBS':
        if  (reg[reg[0]] - reg[reg[2]] < 0):
            reg[8] = -1
        elif  (reg[reg[0]] - reg[reg[2]] > 0):
            reg[8] = 1
        elif  (reg[reg[0]] - reg[reg[2]] == 0):
            reg[8] = 0
def iType(type):
    if type[0] == 'ADDI':
        reg[reg[3]] = reg[reg[2]] + reg[4]
    elif type[0] == 'ORRI':
        reg[reg[3]] = reg[reg[2]] | reg[4]
    elif type[0] == 'EORI':
        reg[reg[3]] = reg[reg[2]] ^ reg[4]
    elif type[0] == 'ANDI':
        reg[reg[3]] = reg[reg[2]] & reg[4]
    elif type[0] == 'SUBI':
        reg[reg[3]] = reg[reg[2]] - reg[4]
    elif type[0] == 'SUBIS':
        if (reg[reg[0]] - reg[4] < 0):
            reg[8] = -1
        elif (reg[reg[0]] - reg[4] > 0):
            reg[8] = 1
        elif (reg[reg[0]] - reg[4] == 0):
            reg[8] = 0
def dType(type):
    if type[0] == 'LDUR':
        reg[8] = reg[reg[2]] + reg[5]
    elif type[0] == 'STUR':
        reg[8] = reg[reg[2]] + reg[5]
def bType(type):
    global PC
    if type[0] == 'B':
        PC = PC + reg[5]
def cbType(type):
    global PC
    if type[0] == 'CBZ':
        print("")
        print("")
        print("")
        print("")
        print("")
        print("SUBI", reg[reg[9]], "=", reg[21], "-", reg[4])
        print("")
        print("")
        print("")
        print("")

        if reg[reg[7]] == 0:
            PC = PC + reg[5]
    elif type[0] == 'CBNZ':
        if reg[7] != 0:
            PC = PC + reg[5]
    elif type[0] == 'B.EQ':
        if reg[8] == 0:
            PC = PC + reg[5]
    elif type[0] == 'B.NE':
        if reg[8] != 0:
            PC = PC + reg[5]
    elif type[0] == 'B.GT':
        if reg[8] == 1:
            PC = PC + reg[5]
    elif type[0] == 'B.GE':
        if reg[8] == 1 or reg[8] == 0:
            PC = PC + reg[5]
    elif type[0] == 'B.LT':
        if reg[8] == -1:
            PC = PC + reg[5]
    elif type[0] == 'B.LE':
        if reg[8] == -1 or reg[8] == 0:
            PC = PC + reg[5]
def accessMem(type):
    if type[0] == 'LDUR':
        reg[reg[7]] = dmem[reg[8]]
    if type[0] == 'STUR':
        dmem[reg[8]] = reg[reg[7]]


Fetch()
#printRegs(1)