 # Place where instructions are processed
"""CPU functionality."""
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010    #  Handled by the ALU
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000    #  Handled by the ALU
CMP = 0b10100111    #  Handled by the ALU
JMP = 0b01010100    #  Sets the PC
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7
        self.fl = 0b00000000
        
    def __str__(self):
        return f"RAM: {self.ram}, REGISTER: {self.reg}, PC: {self.pc}"
    
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value
        
    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print(f"Error: Proper Usage = {sys.argv[0]} filename")
            sys.exit(1)
         
        try:
            with open(sys.argv[1]) as program:
                address = 0
                
                for line in program:
                    num = line.split("#", 1)[0]
                    
                    if num.strip() == '':  # ignores comment-only lines
                        continue
                    self.ram[address] = int(num, 2)
                    address += 1
                    
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)
            
    def alu(self, op, operand_a, operand_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[operand_a] = self.reg[operand_a] + self.reg[operand_b]
            self.pc += 3
        elif op == "MUL":
            # print("MUL, ~PC~: Line", int(self.pc) + 1, "\n")
            self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
            self.pc += 3
        elif op == "CMP":
            # print("CMP, ~PC~: Line", int(self.pc) + 1)
            print(f"CMP, op_a: {self.reg[operand_a]}  vs.  op_b: {self.reg[operand_b]}")
            # If value of register A = register B...
            if self.reg[operand_a] == self.reg[operand_b]:
                print("CMP, op_a EQUAL TO op_b")
                current_fl = self.fl
                E_mask = 0b00000001
                
                # if current_fl masked with '&' of 'E_mask' does not have 'E' flag set to '1', then...
                if (current_fl & E_mask != 0b00000001):
                    # ...use bitwise XOR to get new_fl
                    new_fl = self.fl ^ 0b00000001
                    # set self.fl to value of new_fl
                    self.fl = new_fl
                    print("CMP, E FLAG changed:", bin(self.fl), "\n")
                # if current_fl masked with '&' of 'E_mask' DOES have 'E' flag set to '1', then...
                else:
                    print("CMP, E FLAG already changed:", bin(self.fl), "\n")
            # If value of register A < register B...
            elif self.reg[operand_a] < self.reg[operand_b]:
                print("CMP, op_a LESS THAN op_b")
                current_fl = self.fl
                L_mask = 0b00000100
                
                # if current_fl masked with '&' of 'L_mask' does not have 'L' flag set to '1', then...
                if (current_fl & L_mask != 0b00000100):
                    # ...use bitwise XOR to get new_fl
                    new_fl = self.fl ^ 0b00000100
                    # set self.fl to value of new_fl
                    self.fl = new_fl
                    print("CMP, L FLAG changed:", bin(self.fl), "\n")
                # if current_fl masked with '&' of 'L_mask' DOES have 'L' flag set to '1', then...
                else:
                    print("CMP, L FLAG already changed:", bin(self.fl), "\n")
            # If value of register A > register B...
            elif self.reg[operand_a] > self.reg[operand_b]:
                print("CMP, op_a GREATER THAN op_b")
                current_fl = self.fl
                G_mask = 0b00000010
                
                # if current_fl masked with '&' does not have 'G' flag set to '1', then...
                if (current_fl & G_mask != 0b00000010):
                    # ...use bitwise XOR to get new_fl
                    new_fl = self.fl ^ 0b00000010
                    # set self.fl to value of new_fl
                    self.fl = new_fl
                    print("CMP, G FLAG changed:", bin(self.fl), "\n")
                # if current_fl masked with '&' of 'G_mask' DOES have 'G' flag set to '1', then...
                else:
                    print("CMP, G FLAG already changed:", bin(self.fl), "\n")
            self.pc += 3
            
        else:
            raise Exception("Unsupported ALU operation")
          
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
            
    def run(self):
        """Run the CPU."""
        # determines whether or not this function is "running"
        running = True
        
        # SP pointing at 244 in RAM
        self.reg[self.SP] = 244
      
        print("\n***---------------------------START OF TICO'S PROGRAM------------------------***")
        while (running):
          	# IR = _Instruction Register_
            # IR = self.ram_read(self.pc)
            
            command = self.ram[self.pc]
            
            # num_of_ops = int((IR >> 6) & 0b11) + 1
            
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
                
            if command == LDI:
                # print("LDI, ~PC~: Line", int(self.pc) + 1)
                
                if operand_a == 0b00000000:
                    self.reg[operand_a] = operand_b
                    print("LDI, R0: ***", self.reg[0], "***")
                    print("LDI, R1:", self.reg[1])
                    print("LDI, R2:", self.reg[2])
                    print("LDI, R3:", self.reg[3], "\n")

                elif operand_a == 0b00000001:
                    self.reg[operand_a] = operand_b
                    print("LDI, R0:", self.reg[0])
                    print("LDI, R1: ***", self.reg[1], "***")
                    print("LDI, R2:", self.reg[2])
                    print("LDI, R3:", self.reg[3], "\n")

                elif operand_a == 0b00000010:
                    self.reg[operand_a] = operand_b
                    print("LDI, R0:", self.reg[0])
                    print("LDI, R1:", self.reg[1])
                    print("LDI, R2: ***", self.reg[2], "***")
                    print("LDI, R3:", self.reg[3], "\n")

                elif operand_a == 0b00000011:
                    self.reg[operand_a] = operand_b
                    print("LDI, R0:", self.reg[0])
                    print("LDI, R1:", self.reg[1])
                    print("LDI, R2:", self.reg[2])
                    print("LDI, R3: ***", self.reg[3], "***\n")

                else:
                    print("LDI, unknown register \n")
                self.pc += 3
                
            elif command == PRN: 
                # print("PRN, ~PC~: Line", int(self.pc) + 1)
                print("*----------PRN---------->", self.reg[operand_a], "<----------PRN----------*\n")
                self.pc += 2
                # print("PRN, ~PC~: Line", int(self.pc) + 3, "\n")
               
            elif command == HLT: 
                print("HLT!!\n")
                print("***---------------------------END OF TICO'S PROGRAM!-------------------------***\n")
                running = False
                
            #  Handled by the ALU
            elif command == MUL:
                self.alu("MUL", operand_a, operand_b)
                
            elif command == PUSH:
                # print("PUSH, ~PC~: Line", int(self.pc) + 1, "\n")
                self.reg[self.SP] -= 1
                regnum = self.ram[self.pc + 1]
                value = self.reg[regnum]
                self.ram[self.reg[self.SP]] = value
                self.pc += 2
                
            elif command == POP:
                # print("POP, ~PC~: Line", int(self.pc) + 1, "\n")
                value = self.ram[self.reg[self.SP]]
                regnum = self.ram[self.pc + 1]
                self.reg[regnum] = value
                self.reg[self.SP] += 1 
                self.pc += 2
                
            elif command == CALL:
                # print("CALL, ~PC~: Line", int(self.pc) + 1, "\n")
                # Get address of instruction right after this CALL inst
                return_addr = self.pc + 2
                
                # push the return address on stack
                self.reg[self.SP] -= 1                      # Decrement the SP
                self.ram[self.reg[self.SP]] = return_addr   # Store that value in memory at the SP
                
                # set the PC to the subroutine addr
                # self.pc = self.reg[operand_a] - num_of_ops
                regnum = self.ram[self.pc + 1] 
                subroutine_addr = self.reg[regnum] 
                self.pc = subroutine_addr
                
            elif command == RET:
                # print("RET, ~PC~: Line", int(self.pc) + 1, "\n")
                # pop the return address off the stack
                return_addr = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                
                self.pc = return_addr - 1
            
            #  Handled by the ALU  
            elif command == ADD:
                self.alu("ADD", operand_a, operand_b)
                
            #  Handled by the ALU
            elif command == CMP:
                self.alu("CMP", operand_a, operand_b)
                
            # sets the PC to the address stored in given register
            elif command == JMP:
                # print("JMP, ~PC~: Line", int(self.pc) + 5)
                self.pc = self.reg[operand_a]
                print("JUMPED to Line:", int(self.pc) + 6, "\n")
                
            elif command == JEQ:
                # print("JEQ, ~PC~: Line", int(self.pc) + 1)
                current_fl = self.fl
                E_mask = 0b00000001
                    
                # if current_fl masked with '&' of 'E_mask' DOES have 'E' flag set to '1', then...
                if (current_fl & E_mask != 0b00000000):
                    # ...set PC equal to address stored in the given register
                    if self.reg[operand_a] == 0b00010011: # 19
                        print("JEQ: E FLAG = TRUE =", bin(current_fl), "= JUMPED to TEST 1! \n")
                        # print("JEQ, R2:", self.reg[2])
                        # self.pc = self.reg[operand_a]
                        
                    elif self.reg[operand_a] == 0b00100000: # 32
                        print("JEQ: E FLAG = TRUE =", bin(current_fl), "= JUMPED to TEST 2! \n")
                        # print("JEQ, R2:", self.reg[2])
                        # self.pc = self.reg[operand_a]
                        
                    elif self.reg[operand_a] == 0b00110000: # 48
                        print("JEQ: E FLAG = TRUE =", bin(current_fl), "= JUMPED to TEST 3! \n")
                        # print("JEQ, R2:", self.reg[2])
                        # self.pc = self.reg[operand_a]
                        
                    elif self.reg[operand_a] == 0b00111101: # 61
                        print("JEQ: E FLAG = TRUE =", bin(current_fl), "= JUMPED to TEST 4! \n")
                        # print("JEQ, R2:", self.reg[2])
                        # self.pc = self.reg[operand_a]
                        
                    elif self.reg[operand_a] == 0b01001001: # 73
                        print("JEQ: E FLAG = TRUE =", bin(current_fl), "= JUMPED to TEST 5! \n")
                        # print("JEQ, R2:", self.reg[2])
                    
                    self.pc = self.reg[operand_a]
                        
                    # print("JEQ, ~PC~: Line", int(self.pc) + 1, "\n")
                    # self.pc = self.ram[self.reg[operand_a]]
                # if current_fl masked with '&' of 'E_mask' does NOT have 'E' flag set to '1', then...
                else:
                    self.pc += 2
                    print("JEQ: E FLAG = FALSE =", bin(current_fl), "= NO JUMP!\n")

                   
            elif command == JNE:
                # print("JNE, ~PC~: Line", int(self.pc) + 1)
                current_fl = self.fl
                E_mask = 0b00000001
                    
                # if current_fl masked with '&' of 'E_mask' DOES have 'E' flag set to '0', then...
                if (current_fl & E_mask != 0b00000001):
                    # ...set PC equal to address stored in the given register
                    if self.reg[operand_a] == 0b00010011: # 19
                        print("JNE: E FLAG CLEAR =", bin(current_fl), " = JUMPED TO TEST 1! \n")
                        # self.pc = self.reg[operand_a]
                        # print("JNE, R2:", self.reg[operand_a])
                        
                    elif self.reg[operand_a] == 0b00100000: # 32
                        print("JNE: E FLAG CLEAR =", bin(current_fl), " = JUMPED TO TEST 2! \n")
                        # self.pc = self.reg[operand_a]
                        # print("JNE, R2:", self.reg[operand_a])
                        
                    elif self.reg[operand_a] == 0b00110000: # 48
                        print("JNE: E FLAG CLEAR =", bin(current_fl), " = JUMPED TO TEST 3! \n")
                        # self.pc = self.reg[operand_a]
                        # print("JNE, R2:", self.reg[operand_a])
                        
                    elif self.reg[operand_a] == 0b00111101: # 61
                        print("JNE: E FLAG CLEAR =", bin(current_fl), " = JUMPED TO TEST 4! \n")
                        # self.pc = self.reg[operand_a]
                        # print("JNE, R2:", self.reg[operand_a])
                        
                    elif self.reg[operand_a] == 0b01001001: # 73
                        print("JNE: E FLAG CLEAR =", bin(current_fl), " = JUMPED TO TEST 5! \n")
                        
                    self.pc = self.reg[operand_a]
                    # print("JNE, R2:", self.reg[operand_a])   
                    # print("JNE, ~PC~: Line", int(self.pc), "\n")
                    # self.pc = self.ram[self.reg[operand_a]]
                # if current_fl masked with '&' of 'E_mask' does NOT have 'E' flag set to '1', then...
                else:
                    self.pc += 2
                    print("JNE: E FLAG NOT CLEAR =", bin(current_fl), "= NO JUMP\n")
                
            else: 
                print(f"unknown instruction: {command}")
                sys.exit(1)
                
            # self.pc += num_of_ops