A   B          A XOR B    (Exclusive OR; shows up in bitwise operations)
----------------------    (only ONE of the choices is True; not both)
0   0             0
0   1             1
1   0             1
1   1             0




A   B          A And B
----------------------
0   0             0
0   1             0
1   0             0
1   1             1

  1101011
& 1010010
---------
  1000010


          Boolean   Bitwise
OR          OR         |
AND         and        &
XOR         N/A        ^
NOT         not        ~  (turns 1s into 0s and 0s into -1)


-"AND" Masking (similar to spray painting with a stencil, except this uses numbers)

  10100101
& 11110000   <- AND mask
-----------
  1010

-The AND mask allows us to SELECT a few bits in a number and ignore the others.

-Use the "&".

-"1" will allow a number to "shine" through.
-"0" will ignore any number.


  10100000   <- ADD
& 11000000   <- use AND mask to pull only the first 2 numbers out.
-----------
  10000000   (Our goal: shift bits to the right to extract "2" out of 
  ^^          the ADD opcode; we want to shift because we want "2", NOT
              "128")

  00000010
        ^^

  7635463   <-example
  0035000   <-AND mask to only get 35 out of the top number
  0000035   <-Goal: try to shift those numbers all the way to the right

            Boolean   Bitwise
OR          OR         |
AND         and        &
XOR         N/A        ^
NOT         not        ~  (turns 1s into 0s and 0s into -1)
LEFT shift             <<
RIGHT shift            >>

  10100000   <- ADD
& 11000000   <- use AND mask to pull only the first 2 numbers out.
-----------
  10000000   (Our goal: shift bits to the right to extract "2" out of 
  ^^          the ADD opcode)

   1000000
    100000
     10000
      1000
       100
  00000010
        ^^

ir = 0b10100000   ADD
num_operands = (ir & 0b11000000) >> 6 (right shift by 6 places; tells                                          us that the ADD instruction has                                         2 operands )





