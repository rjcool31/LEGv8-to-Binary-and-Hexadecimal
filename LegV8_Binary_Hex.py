# ELET3405: LEGv8 to Binary and Hexadecimal Encoder
# Author: Ryan Jochims-Torres, 1928645

# TODO: branch address calculation or random num gen for address
import os

# Needed list and dictionaries to convert
ISA_to_opcode = {
    "ADD"  : "10001011000", "ADDS" : "10101011000", "ADDI" : "1001000100", "ADDIS" : "1011000100",
    "FADDS" : "00011110001", "FADDD" : "00011110011",
	"SUB"  : "11001011000", "SUBS" : "11101011000", "SUBI" : "1101000100", "SUBIS" : "1111000100",
    "FSUBS" : "00011110001", "FSUBD" : "00011110011",
    "MUL"  : "10011011000", "SMULH": "10011011010", "UMULH" : "10011011110",
    "FMULS" : "00011110001", "FMULD" : "00011110011",
    "UDIV" : "10011010110", "SDIV" : "10011010110",
    "FDIVS" : "00011110001", "FDIVD" : "00011110011",

    "FCMPS" : "00011110001", "FCMPD" : "00011110011",
	"AND" : "10001010000", "ANDI" : "1001001000", "ANDS" : "11101010000", "ANDIS" : "1111001000",
	"ORR" : "10101010000", "ORRI" : "1011001000",
	"EOR" : "11001010000", "EORI" : "1101001000",

	"LDUR" : "11111000010", "STXR" : "11001000000", "STURS" : "10111100000", "STURB" : "00111000000",
    "STURH" : "01111000000", "STURW"  : "10111000000", "STURD" : "11111100000",
	"STUR" : "11111000000", "LDXR" : "11001000010", "LDURS" : "10111100010", "LDURB" : "00111000010",
    "LDURH" : "01111000010", "LDURSW" : "10111000100", "LDURD" : "11111100010",

    "MOVZ" : "110100101", "MOVK" : "111100101",
    "LSR"  : "11010011010", "LSL" : "11010011011",

    "B" : "000101", "BL" : "100101", "BR" : "11010110000", "B." : "01010100",
    "CBZ" : "10110100", "CBNZ" : "10110101"
}

register_list = {
    "X0" : "00000",	"X1" : "00001",	"X2" : "00010",	"X3" : "00011",	"X4" : "00100",
	"X5" : "00101",	"X6" : "00110",	"X7" : "00111",	"X8" : "01000",	"X9" : "01001",
	"X10" : "01010", "X11" : "01011", "X12" : "01100", "X13" : "01101",	"X14" : "01110",
	"X15" : "01111", "X16" : "10000", "IP0" : "10000", "X17" : "10001", "IP1" : "10001", 
    "X18" : "10010", "X19" : "10011", "X20" : "10100", "X21" : "10101", "X22" : "10110",
    "X23" : "10111", "X24" : "11000", "X25" : "11001", "X26" : "11010", "X27" : "11011",
    "X28" : "11100", "SP"  : "11100", "X29" : "11101", "FP"  : "11101", "X30" : "11110",
    "LR"  : "11110", "X31" : "11111", "XZR" : "11111"}

special_shamt = {
    'FMULS' : '000010', 'FDIVS' : '000110', 'FCMPS' : '001000', 'FADDS' : '001010', 'FSUBS' : '001110',
    'FMULD' : '000010', 'FDIVD' : '000110', 'FCMPD' : '001000', 'FADDD' : '001010', 'FSUBD' : '001110',
    'SDIV'  : '000010', 'UDIV'  : '000011', 'MUL'   : '011111'}


type_R  = ['ADD', 'ADDS', 'SUB', 'SUBS', 'AND', 'ANDS' 'ORR', 'EOR', 'LSL', 'LSR', 'BR',
    'FADDS', 'FADDD', 'FCMPS', 'FCMPD', 'FDIVS', 'FDIVD', 'FMULS', 'FMULD', 'FSUBS', 'FSUBD',
    'LDURS', 'LDURD', 'MUL', 'SDIV', 'SMULH', 'STURS', 'STURD', 'UDIV', 'UMULH']
type_I  = ['ADDI','ADDIS' 'SUBI', 'SUBIS', 'ANDI', 'ANDIS', 'EORI', 'ORRI', ]
type_D  = ['LDUR', 'LDURB', 'LDURH', 'LDURSW', 'LDXR',
    'STUR', 'STURB', 'STURH', 'STURW', 'STXR']
type_B  = ['B', 'BL']
type_CB = ['CBNZ', 'CBZ', 'B.EQ', 'B.NE', 'B.LT', 'B.LO',
    'B.LE', 'B.LS', 'B.GT', 'B.HI', 'B.GE', 'B.HS']
type_IM = ['MOVK', 'MOVZ']


# Get user input and Output files
print("Please have desired input and output files in same folder as .py file")
user_in = input("Please enter input file and output file separated by a space.\n")
in_out_files = user_in.split()

# Gets local location of directory to locate user files
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Opens and reads code line by line into a list 
with open(os.path.join(__location__, in_out_files[0]), 'r') as f_in:
    legv8_messy = [line.strip() for line in f_in]

# Gets rid of unneeded characters and splits each line into a iterable list
legv8_code = []
for i in range(len(legv8_messy)):
    line_str = legv8_messy[i].replace(',','').replace('[','').replace(']','').replace('#','')
    legv8_code.append(line_str.split())

# Opens user output file to be written to
f_out = open(os.path.join(__location__, in_out_files[1]), 'w')

# Main script to convert LEGv8 to binary and Hexadecimal, also writes to output file
for line_num in range(len(legv8_code)):
    # Variable strings for each term in line
    line_binary_str = ''
    opcode = ''; Rm = ''; Rn = ''; Rd = ''; Rt = ''
    shamt = ''; address = ''; immediate = ''
    op2 = '00'
    
    # converts ISA to binary and stores into variables for formatting later
    opcode = ISA_to_opcode[legv8_code[line_num][0]]
    
    if legv8_code[line_num][0] in type_R:
        if legv8_code[line_num][0] in special_shamt:
            shamt = special_shamt[legv8_code[line_num][0]]
        else:
            shamt = '000000'
        Rm = register_list[legv8_code[line_num][3]]
        Rn = register_list[legv8_code[line_num][2]]
        Rd = register_list[legv8_code[line_num][1]]
    
    elif legv8_code[line_num][0] in type_I:
        temp = int(legv8_code[line_num][3])
        immediate = format(temp, '012b')
        Rn = register_list[legv8_code[line_num][2]]
        Rd = register_list[legv8_code[line_num][1]]
    
    elif legv8_code[line_num][0]in type_D:
        temp = int(legv8_code[line_num][3])
        address = format(temp, '09b')
        Rn = register_list[legv8_code[line_num][2]]
        Rt = register_list[legv8_code[line_num][1]]
    
    elif legv8_code[line_num][0]in type_B:
        temp = int(legv8_code[line_num][1])
        address = format(temp, '026b')
    
    elif legv8_code[line_num][0]in type_CB:
        temp = int(legv8_code[line_num][2])
        address = format(temp, '019b')
        Rt = register_list[legv8_code[line_num][1]]
    
    elif legv8_code[line_num][0]in type_IM:
        temp = int(legv8_code[line_num][2])
        immediate = format(temp, '016b')
        Rd = register_list[legv8_code[line_num][1]]
    
    # Takes variables stored and formats into single binary string depending on type
    if legv8_code[line_num][0] in type_R:
        line_binary_str = f'{opcode}{Rm}{shamt}{Rn}{Rd}'
    elif legv8_code[line_num][0] in type_I:
        line_binary_str = f'{opcode}{immediate}{Rn}{Rd}'
    elif legv8_code[line_num][0]in type_D:
        line_binary_str = f'{opcode}{address}{op2}{Rn}{Rt}'
    elif legv8_code[line_num][0] in type_B:
        line_binary_str = f'{opcode}{address}'
    elif legv8_code[line_num][0] in type_CB:
        line_binary_str = f'{opcode}{address}{Rt}'
    elif legv8_code[line_num][0] in type_IM:
        line_binary_str = f'{opcode}{immediate}{Rd}'
    else:
        line_binary_str = 'ERROR: Command Type'
    
    # Converts binary string to Hexadecimal with check of 32-Bits
    if (len(line_binary_str) == 32):
        line_hex = hex(int(line_binary_str, 2))
    else:
        line_hex = 'ERROR: HEX Convert Failed'
    
    # Joins LEGv8 line entered, Binary string conversion, and Hexadecimal conversion into single string
    converted = legv8_messy[line_num] + '\t' + line_binary_str + '\t' + line_hex + '\n'
    # Writes joined line to output file
    f_out.write(converted)
# Closes output file
f_out.close()