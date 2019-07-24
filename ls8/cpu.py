# Place where instructions are processed
"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        
    def __str__(self):
        return f"RAM: {self.ram}, REGISTER: {self.reg}, PC: {self.pc}"
    
    # MAR = address; _Memory Address Register_
    def ram_read(self, address):
        return self.ram[address]
    
    # MDR = value; _Memory Data Register_
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        program = [] * 256

        if len(sys.argv) != 2:
            print(f"Error: Proper Usage = {sys.argv[0]} filename")
            sys.exit(1)
            
        try:
            with open(sys.argv[1]) as program:
                address = 0
                
                for instruction in program:
                    opcode = instruction.split("#", 1)[0]
                    
                    if opcode.strip() == '':  # ignores comment-only lines
                        continue
                    # print(int(opcode))
                    self.ram[address] = int(opcode)
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
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        HLT = 0b00000001
        PRN = 0b01000111
        
        # determines whether or not this function is "running"
        running = True
        
        # IR = _Instruction Register_
        IR = self.ram_read(self.pc)
        
        while (running):
            command = self.ram[self.pc]
            num_of_ops = int(IR & 0b110000000 >> 6) + 1
            
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            if command == HLT: 
                running = False
                
            elif command == LDI:
                self.reg[operand_a] = operand_b
                
            elif command == PRN:
                print(self.reg[operand_a])
                
            else: 
                print("Command: ", command)
                print("LDI: ", LDI)
                print(f"unknown instruction: {command}")
                sys.exit(1)
                
            self.pc += num_of_ops
