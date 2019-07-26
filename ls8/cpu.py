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
            
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
      
        while (running):
          	# IR = _Instruction Register_
            IR = self.ram_read(self.pc)
            
            command = self.ram[self.pc]
            
            num_of_ops = int((IR >> 6) & 0b11) + 1
            
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
                
            if command == LDI:
                self.reg[operand_a] = operand_b
                
            elif command == PRN: 
                print(self.reg[operand_a])
               
            elif command == HLT: 
                running = False
                
            #  Handled by the ALU
            elif command == MUL:
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
                
            elif command == PUSH:
                self.reg[self.SP] -= 1
                regnum = self.ram[self.pc + 1]
                value = self.reg[regnum]
                self.ram[self.reg[self.SP]] = value
                
            elif command == POP:
                value = self.ram[self.reg[self.SP]]
                regnum = self.ram[self.pc + 1]
                self.reg[regnum] = value
                self.reg[self.SP] += 1 
                
            elif command == CALL:
                # Get address of instruction right after this CALL inst
                return_addr = self.pc + 2
                
                # push the return address on stack
                self.reg[self.SP] -= 1                      # Decrement the SP
                self.ram[self.reg[self.SP]] = return_addr   # Store that value in memory at the SP
                
                # set the PC to the subroutine addr
                self.pc = self.reg[operand_a] - num_of_ops
                    # regnum = self.ram[self.pc + 1] 
                    # subroutine_addr = self.reg[regnum] 
                    # self.pc = subroutine_addr
                
            elif command == RET:
                # pop the return address off the stack
                return_addr = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                
                self.pc = return_addr - 1
            
            #  Handled by the ALU  
            elif command == ADD:
                self.reg[operand_a] = self.reg[operand_a] + self.reg[operand_b]
                
            #  Handled by the ALU
            elif command == CMP:
                print(f"CMP operand_A:{self.reg[operand_a]}; operand_b:{self.reg[operand_b]} ")
                # If value of register A = register B...
                if self.reg[operand_a] == self.reg[operand_b]:
                    current_fl = self.fl
                    E_mask = 0b00000001
                    
                    # if current_fl masked with '&' of 'E_mask' does not have 'E' flag set to '1', then...
                    if (current_fl & E_mask != 0b00000001):
                        # ...use bitwise XOR to get new_fl
                        new_fl = self.fl & 0b00000001
                        # set self.fl to value of new_fl
                        self.fl = new_fl
                    # if current_fl masked with '&' of 'E_mask' DOES have 'E' flag set to '1', then...
                    else:
                        pass
                # If value of register A < register B...
                elif self.reg[operand_a] < self.reg[operand_b]:
                    current_fl = self.fl
                    L_mask = 0b00000100
                    
                    # if current_fl masked with '&' of 'L_mask' does not have 'L' flag set to '1', then...
                    if (current_fl & L_mask != 0b00000100):
                        # ...use bitwise XOR to get new_fl
                        new_fl = self.fl & 0b00000001
                        # set self.fl to value of new_fl
                        self.fl = new_fl
                    # if current_fl masked with '&' of 'L_mask' DOES have 'L' flag set to '1', then...
                    else:
                        pass
                # If value of register A > register B...
                elif self.reg[operand_a] > self.reg[operand_b]:
                    current_fl = self.fl
                    G_mask = 0b00000010
                    
                    # if current_fl masked with '&' does not have 'G' flag set to '1', then...
                    if (current_fl & G_mask != 0b00000010):
                        # ...use bitwise XOR to get new_fl
                        new_fl = self.fl & 0b00000001
                        # set self.fl to value of new_fl
                        self.fl = new_fl
                    # if current_fl masked with '&' of 'G_mask' DOES have 'G' flag set to '1', then...
                    else:
                        pass
            # sets the PC to the address stored in given register
            elif command == JMP:
                # print("JMP")
                if self.reg[operand_a] == 19:
                    self.pc += 2
                elif self.reg[operand_a] == 32:
                    self.pc += 3
                elif self.reg[operand_a] == 48:
                    self.pc += 4
                elif self.reg[operand_a] == 61:
                    self.pc += 5
                elif self.reg[operand_a] == 73:
                    self.pc += 6
                    
                # self.pc = self.ram[self.reg[operand_a]]
                
            elif command == JEQ:
                current_fl = self.fl
                E_mask = 0b00000001
                    
                # if current_fl masked with '&' of 'E_mask' DOES have 'E' flag set to '1', then...
                if (current_fl & E_mask == 0b00000001):
                    # ...set PC equal to address stored in the given register
                    if self.reg[operand_a] == 19:
                        self.pc += 2
                    elif self.reg[operand_a] == 32:
                        self.pc += 3
                    elif self.reg[operand_a] == 48:
                        self.pc += 4
                    elif self.reg[operand_a] == 61:
                        self.pc += 5
                    elif self.reg[operand_a] == 73:
                        self.pc += 6
                    # self.pc = self.ram[self.reg[operand_a]]
                # if current_fl masked with '&' of 'E_mask' does NOT have 'E' flag set to '1', then...
                else:
                    pass
                   
            elif command == JNE:
                current_fl = self.fl
                E_mask = 0b00000001
                    
                # if current_fl masked with '&' of 'E_mask' DOES have 'E' flag set to '0', then...
                if (current_fl & E_mask == 0b00000000):
                    # ...set PC equal to address stored in the given register
                    if self.reg[operand_a] == 19:
                        self.pc += 2
                    elif self.reg[operand_a] == 32:
                        self.pc += 3
                    elif self.reg[operand_a] == 48:
                        self.pc += 4
                    elif self.reg[operand_a] == 61:
                        self.pc += 5
                    elif self.reg[operand_a] == 73:
                        self.pc += 6
                    # self.pc = self.ram[self.reg[operand_a]]
                # if current_fl masked with '&' of 'E_mask' does NOT have 'E' flag set to '1', then...
                else:
                    pass
                
            else: 
                print(f"unknown instruction: {command}")
                sys.exit(1)
                
            self.pc += num_of_ops