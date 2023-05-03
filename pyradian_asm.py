#this module is used to seperate the technical stuff from the gui stuff 

#import a module to call a function every second
import time

class ReversibleDict:
    """
    A dictionary that can be easily be reversed.
    there is a better way to do this but i haven't looked into it yet
    and this works for now there is only 32 opcodes , not millions of them
    """
    def __init__(self,from_dict=None):
        if from_dict:
            self.dict=from_dict
            self.reverse_dict={v:k for k,v in from_dict.items()}
        else:
            self.dict = {}
            self.reverse_dict = {}
    def __setitem__(self, key, value):
        self.dict[key] = value
        self.reverse_dict[value] = key

    def __getitem__(self, key):
        return self.dict[key]

    def get_key(self, value):
        return self.reverse_dict[value]

#this is a dictionary of all the opcodes and their corresponding binary values with a description in the comments 
opcodes = {
    "HLT"  :"00000",#halt the program                                                           special opcode
    "LOAD" :"00001",#load a value into a register                                               special opcode                         
    "STORE":"00010",#store a value from a register into memory                                  special opcode

    "ADD"  :"00011",#add two registers and store the result in a register
    "SUB"  :"00100",#subtract two registers and store the result in a register
    "MUL"  :"00101",#multiply two registers and store the result in a register
    "DIV"  :"00110",#divide two registers and store the result in a register
    "MOD"  :"00111",#modulus two registers and store the result in a register
    "AND"  :"01000",#bitwise and two registers and store the result in a register
    "OR"   :"01001",#bitwise or two registers and store the result in a register
    "XOR"  :"01010",#bitwise xor two registers and store the result in a register
    "NOT"  :"01011",#bitwise not a register and store the result in a register
    "SHL"  :"01100",#bitwise shift left a register and store the result in a register its a 
    "SHR"  :"01101",#bitwise shift right a register and store the result in a register its a 
    "INC"  :"01110",#increment a register by one
    "DEC"  :"01111",#decrement a register by one
    "CMP"  :"10000",#compare two registers and store the result in a register
    "BIT"  :"10001",#get a bit from a register and store the result in a register
    "SET"  :"10010",#set a bit in a register
    "SWAP" :"10011",#swap two registers
    "REV"  :"10100",#reverse the bits in a register
    "CALL" :"10101",#call a subroutine                                                           special opcode
    "RET"  :"10110",#return from a subroutine                                                    special opcode
    "JMP"  :"10111",#jump to a specific memory address
    "JZ"   :"11000",#jump to a specific memory address if the zero flag is set
    "JNZ"  :"11001",#jump to a specific memory address if the zero flag is not set
    "JC"   :"11010",#jump to a specific memory address if the carry flag is set
    "JNC"  :"11011",#jump to a specific memory address if the carry flag is not set
    "PUSH" :"11100",#push a value onto the memory stack                                         special opcode
    "POP"  :"11101",#pop a value off the memory stack                                           special opcode
    "NOP"  :"11110",#do nothing very useful
    "EASTEREGG":"11111"#easter egg opcode                                                      special opcode
}

special_opcodes = {
    #these are the opcodes that have to be handled differently
    "HLT"  :"00000",#halt the program
    "LOAD" :"00001",#load a value into a register
    "STORE":"00010",#store a value from a register into memory
    "CALL" :"10101",#call a subroutine
    "RET"  :"10110",#return from a subroutine
    "PUSH" :"11100",#push a value onto the memory stack
    "POP"  :"11101",#pop a value off the memory stack
    "EASTEREGG":"11111"#easter egg opcode
}
opcodes_rdict=ReversibleDict(opcodes) 
special_opcodes_rdict=ReversibleDict(special_opcodes)
#this is a reverse dictionary tm of all the opcodes and their corresponding binary values
def HLT():
    clock.stop()
def LOAD(address,register):
    register = memory[address]
def STORE(address,register):
    memory[address] = register
def CALL(address):
    #these are exta hard to implement
    pass
def RET():
    #these are exta hard to implement
    pass
def PUSH(register):
    memory[stack_pointer] = register
    stack_pointer += 1
def POP(register):
    stack_pointer -= 1
    register = memory[stack_pointer]
    memory[stack_pointer] = 0
def EASTEREGG():
    print("Felicitation vous avez trouvé l'easter egg")
class Word:
    def __init__(self, value=0, size=16):
        self.value = value
        self.size = size
        self.bits = [0]*size
    def __getitem__(self, key):
        return self.bits[key]
    def __setitem__(self, bit, value:bool):
        self.bits[bit] = value
        self.value = int("".join([str(i) for i in self.bits]),2)
    def __repr__(self):
        return str(self.value)
    def set_value(self, value):
        self.value = value
        self.bits = [0]*(self.size-len(self.bits))+[int(i) for i in bin(value)[2:]]

class Register(Word):
    """docstring for Register.
    this is a register class that inherits from the word class
    it has a size and a value and has methods to do operations on it

    """
    def add(self,other,target):
        target.value=(self.value+other.value)%(2**self.size)
    def sub(self,other,target):
        target.value=(self.value-other.value)%(2**self.size)
    def mul(self,other,target):
        target.value=(self.value*other.value)%(2**self.size)
    def div(self,other,target):
        target.value=self.value//other.value
    def mod(self,other,target):
        target.value=self.value%other.value
    def and_(self,other,target):
        target.value=self.value&other.value
    def or_(self,other,target):
        target.value=self.value|other.value
    def xor(self,other,target):
        target.value=self.value^other.value
    def not_(self,target):
        target.value=~self.value
    def shl(self,target):
        target.div(self.value,2)
    def shr(self,target):
        target.mul(self.value,2)
    def inc(self,target):
        target.add(self,1)
    def dec(self,target):
        target.sub(self,1)
    def cmp(self,other,target):
        if self.value==other.value:
            target.value=1
        elif self.value>other.value:
            target.value=2
        else:
            target.value=1
    def bit(self,other,target):
        target.value=self.and_()
    

    #opcodes
class clock:
    def __init__(self,pc_register,delay=1):
        self.running = False
        self.delay = delay
        self.pc_register = pc_register
    def start(self):
        self.running = True
        while self.running:

            #call the function to increment the program counter and execute the instruction
            time.sleep(self.delay)
            


class memory:
    def __init__(self, size=256):
        self.memory = [Word() for i in range(size)]

    def __getitem__(self, key):
        return self.memory[-key]

def compile (code: str):
    #this function will compile the code into machine code

    #first we will split the code into lines
    lines = code.splitlines()
    #then we will split the lines into words

def compile_line(line: str):
    #this function will compile a line of code into machine code
    global opcodes_rdict
    