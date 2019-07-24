# This is the program that is running all of our programs

#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()

print(f'RAM (BEFORE):\n {cpu.ram} \n')
print(f'REGISTER (BEFORE):\n {cpu.reg} \n')

print(f'RAM (AFTER):\n {cpu.ram} \n')
print(f'REGISTER (AFTER):\n {cpu.reg} \n')

# print(sys.argv[0])
# print(sys.argv[1])