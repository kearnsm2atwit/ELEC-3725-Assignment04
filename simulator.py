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

rCodes =  ["ADD", "AND", "ORR", "ADDS", "EOR", "SUB", "LSR", "LSL", "BR", "ANDS", "SUBS"]
iCodes =  ["ORRI", "EORI", "ADDI", "ANDI", "ADDIS", "SUBI", "SUBIS", "ANDIS"]
dCodes =  ["STUR", "LDUR"]
bCodes =  ["B"]
cbCodes = ["CBZ", "CBNZ", "B.EQ", "B.NE", "B.GT", "B.GE", "B.LT", "B.LE"]

code1 = open("code1_dec.txt", "r")  #input binary file
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
dmem = [0]
for i in range(9):
    dmem.append(0)
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
def Fetch():
    global IR, PC, imem
    IR = imem[PC]
    IR = IR.split(" ")
    PC = PC+1
    print(IR)
    print(IR[0])
    opcode = legv8[IR[0]]
    type = instructionType(opcode)
    print(type)
    type = type.split(" ")
    decode(IR)

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
def decode(IR):
    global reg
    if IR[1] == 'R':
        reg[0] = IR[1]  #Rm         rm = 0
        reg[1] = IR[2]  #shamt      shamt = 1
        reg[2] = IR[3]  #Rn         rn = 2
        reg[3] = IR[4]  #Rd         rd = 3
    elif IR[1] == 'I':              #immediate = 4
        reg[4] = IR[1]  #immediate  address = 5
        reg[2] = IR[2]  #Rn         op2 = 6
        reg[3] = IR[3]  #Rd         rt = 7
    elif IR[1] == 'D':
        reg[5] = IR[1]  #address
        reg[6] = IR[2]  #op2
        reg[2] = IR[3]  #Rn
        reg[7] = IR[4]  #Rt
    elif IR[1] == 'B':
        reg[5] = IR[1]  #address
    elif IR[1] == 'CB':
        reg[5] = IR[1]  #address
        reg[7] = IR[2]  #Rt


Fetch()
#printRegs(1)