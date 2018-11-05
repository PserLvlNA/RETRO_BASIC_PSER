# RETRO_BASIC_PSER
Input example
- 10 A = 1
- 20 B = 2
- 30 C = A + B
- 40 PRINT C
- 50 STOP

use:
1) C:\>c1.py "input file name"
    - ex. C:\>c1.py INPUT.txt
    - get output on screen and output file MyBCODE.txt
    - seperate parsing and converting
    - has some bug if input like this
        - 10 A = 1 20 A = A - 1 30 PRINT A 40 STOP
        - It doesn’t work

2) C:\>c2.py "input file name"
    - ex. C:\>c2.py INPUT.txt
    - get output on screen and output file MyBCODE.txt
    - parsing and converting at the same time
    - fixing bug above
