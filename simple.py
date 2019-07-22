import sys

PRINT_BEEJ      = 1
HALT            = 2
PRINT_NUM       = 3
SAVE_REGISTER   = 4
PRINT_REGISTER  = 5

memory = [
    PRINT_BEEJ,
    SAVE_REGISTER,
    77,     # store 77
    2,      # in register 2
    PRINT_REGISTER,
    2,      # Print value in register 2
    HALT,
]

register = [0] * 8  # 8 registers

pc = 0 # Program Counter, points to currently-executing instruction

running = True

while (running):
    command = memory[pc]
    if command == PRINT_BEEJ:
        print("Beej!")
        
    elif command == HALT:
        running == False
    
    else: 
        print(f"unknown instruction {command}")
        sys.exit(1)
        
    pc += 1
        
        