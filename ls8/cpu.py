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

        address = 0  # Address

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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
        # determines whether or not this function is "running"
        running = True
        
        # IR = _Instruction Register_
        IR = self.ram_read(self.pc)
        
        # operand_a = self.ram_read(self.pc + 1)
        # operand_b = self.ram_read(self.pc + 2)
        
        # while (running):
        #     command = self.ram[self.pc]
            
        #     if command == None: 
        #         print ("Jake, what do software developers do?")
        #     else:
        #         pass
        #     self.pc += 1
        
        # return IR
        
        
        
        
        
    
cpu = CPU()
print(f'RAM (BEFORE write):\n {cpu.ram} \n')
print(f'REGISTER (BEFORE write):\n {cpu.reg} \n')
print(f'Value at Address 5 (BEFORE write):\n {cpu.ram_read(5)} \n')  # Should return None

cpu.ram_write(200, 5)
print(f'RAM (AFTER write):\n {cpu.ram} \n')
print(f'REGISTER (AFTER write):\n {cpu.reg} \n')
print(f'Value at Address 5 (AFTER write):\n {cpu.ram_read(5)} \n')  # Should return '200'

print(f'run() returns:\n {cpu.run()} \n')
