# Base 10 (digits: 0-9)

#   7
#   8
#   9
#  10 (1 ten, and 0 ones)
# 123 (1 hundred, 2 tens, and 3 ones) => 1 _ 100 + 2 _ 10 + 3 \* 1

# Base 2 (digits: 0-1)

#  0
#  1
# 10 (1 twos, 0 ones)

# Base 16 (digits: 0-9, A-F)

#  8
#  9
#  A
#  B
#  C
#  D
#  E 
#  F
# 10

# Base 64 (digits: A-Z, a-z, 0-9, +, /)

# Examples in Python
x = 0b101011 # use "0b" in front to inform python of a binary number
y = x + 10

print(x, y) # 43 53
print("{:b} {}".format(x, y)) # 101011 53 // Prints 1st number in binary; 2nd in decimal

x = "1010110"
y = int(x, 2) # converts 'x' (a string) into an integer with a base of 2

print(y)

#--------------------------------------------------------------------------


# 1000s  10^3 == 1000
# |100s  10^2 == 100
# ||10s  10^1 == 10
# |||1s  10^0 == 1
# 1234

# 8s     2^3 == 8
# |4s    2^2 == 4
# ||2s   2^1 == 2
# |||1s  2^0 == 1
# 1101   base 2

# 0b1101 == 13 decimal (base 10)
# 8 + 4 + 1 == 13


# 0b10101011 == 171 decimal
# 128 + 32 + 8 + 2 + 1 == 171


# 17 decimal == ?? binary
# 16 + 1 == 17

# 0b10000 + 0b1 = 0b10001



