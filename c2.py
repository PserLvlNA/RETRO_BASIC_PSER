import sys
filename = sys.argv[1]
############################################
##############  Declaration  ###############
############################################
bcode= []
out = []
out2 = []
pars = []
ii = 0
isPass = 0
s_pgm = 1
s_line =2
s_stmt =3
s_asgmnt =4
s_exp =5
s_expp= 6
s_term =7
s_if =8
s_cond =9
s_condp =10
s_print =11
s_goto= 12
s_stop =13
s_line_num =14
s_id =15
s_IF =16
s_PRINT =17
s_GOTO =18
s_STOP =19
s_plus =20
s_minus =21
s_const =22
s_less =23
s_equal =24
s_goto_num =25
ch = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

############################################
###########  Parsing function  #############
############################################

def pushstk(k):
    #print k
    if k == 1:
        pars.append(s_pgm)
        pars.append(s_line)
    elif k==3:
        pars.append(s_stmt)
        pars.append(s_line_num)
    elif k==4:
        pars.append(s_asgmnt)
    elif k==5:
        pars.append(s_if)
    elif k==6:
        pars.append(s_print)
    elif k==7:
        pars.append(s_goto)
    elif k==8:
        pars.append(s_stop)
    elif k==9:
        pars.append(s_exp)
        pars.append(s_equal)
        pars.append(s_id)
    elif k==10:
        pars.append(s_expp)
        pars.append(s_term)
    elif k==11:
        pars.append(s_term)
        pars.append(s_plus)
    elif k==12:
        pars.append(s_term)
        pars.append(s_minus)
    elif k==14:
        pars.append(s_id)
    elif k==15:
        pars.append(s_const)
    elif k==16:
        pars.append(s_goto)
        pars.append(s_cond)
        pars.append(s_IF)
    elif k==17:
        pars.append(s_condp)
        pars.append(s_term)
    elif k==18:
        pars.append(s_term)
        pars.append(s_less)
    elif k==19:
        pars.append(s_term)
        pars.append(s_equal)
    elif k==20:
        pars.append(s_id)
        pars.append(s_PRINT)
    elif k==21:
        pars.append(s_line_num)
        pars.append(s_GOTO)
    elif k==22:
        pars.append(s_STOP)

def isLineNum(s):
    if 1<= int(s) <= 1000:
        return 1
    else:
        return 0
    return 1
def isConst(s):
    x = int(s)
    if 0<=x<=100:
        return 1
    return 0
def isID(s):
    if len(s)!= 1 :
        return 0
    if s in ch:
        return 1
    return 0
def d_pgm():
    if ii < len(out):
        a = isLineNum(out[ii])
    if ii == len(out):
        return 1
    elif a==1:
        pushstk(1)
    return 1
def d_line():
    if isLineNum(out[ii]):
        pushstk(3)
    else:
        return 0
    return 1
def d_stmt():
    if(isID(out[ii])) :
        pushstk(4)
    elif out[ii] == "IF" :
        pushstk(5)
    elif out[ii] == "PRINT":
        pushstk(6)
    elif out[ii] == "GOTO":
        pushstk(7)
    elif out[ii] == "STOP":
        pushstk(8)
    else :
        return 0
    return 1
def d_asgmnt():
    if isID(out[ii]):
        pushstk(9)
    else:
        return 0;
    return 1
def d_exp():
    if isID(out[ii]) or isConst(out[ii]):
        pushstk(10)
    else:
        return 0
    return 1
def d_expp():
    if ii<len(out):
        if out[ii]=="+":
            pushstk(11)
        elif out[ii]=="-":
            pushstk(12)
        return 1;
def d_term():
    if(isID(out[ii])) :
        pushstk(14)
    elif(isConst(out[ii])):
        pushstk(15)
    else:
        return 0
    return 1
def d_if():
    if(out[ii]=="IF"):
        pushstk(16)
    else:
        return 0
    return 1
def d_cond():
    if(isID(out[ii]) or isConst(out[ii])):
        pushstk(17)
    else:
        return 0
    return 1
def d_condp():
    if(out[ii]=="<") :
        pushstk(18)
    elif(out[ii]=="="):
        pushstk(19)
    else:
        return 0
    return 1
def d_print():
    if(out[ii]=="PRINT"):
        pushstk(20)
    else:
        return 0
    return 1
def d_goto():
    """if(out[ii]=="GOTO"):
        pushstk(21)
    else:
        return 0"""
    pushstk(21)
    return 1
def d_stop():
    if(out[ii]=="STOP"):
        pushstk(22)
    else:
        return 0
    return 1
def d_line_num():
    if(isLineNum(out[ii])):
        bcode.append("10")
        bcode.append(out[ii])
        return 1
    else :
        return 0
    return 1
def d_id():
    if(isID(out[ii])):
        bcode.append("11")
        a = ord(out[ii])-64
        bcode.append(str(a))
        return 1
    else:
        return 0
def d_IF():
    if(out[ii]=="IF"):
        bcode.append("13")
        bcode.append("0")
        return 1
    else:
        return 0
def d_PRINT():
    if(out[ii]=="PRINT"):
        bcode.append("15")
        bcode.append("0")
        return 1
    else:
        return 0
def d_GOTO():
    global ii
    if out[ii]=="GOTO" and isLineNum(out[ii+1]):
        pars.pop()
        bcode.append("14")
        bcode.append(str(out[ii+1]))
        ii=ii+1
    elif isLineNum(out[ii]):
        pars.pop()
    else:
        return 0
    return 1
def d_STOP():
    if(out[ii]=="STOP") :
        bcode.append("16")
        bcode.append("0")
        return 1
    else:
        return 0
def d_plus():
    if ii < len(out):
        if(out[ii]=="+"):
            bcode.append("17")
            bcode.append("1")
            return 1
        else:
            return 0
def d_minus():
    if(out[i]=="-"):
        bcode.append("17")
        bcode.append("2")
        return 1
    else:
        return 0
def d_const():
    if(isConst(out[ii])):
        bcode.append("12")
        bcode.append(str(out[ii]))
        return 1
    else:
        return 0
def d_less():
    if(out[ii]=="<"):
        bcode.append("17")
        bcode.append("3")
        return 1
    else:
        return 0
def d_equal():
    if(out[ii]=="="):
        bcode.append("17")
        bcode.append("4")
        return 1
    else:
        return 0
def d_goto_num():
    if(isLineNum(out[ii])):
        return 1
    else:
        return 0
    return 1
def reject():
    return 0
def accept():
    return 1     

#######################################
#########  Translate function  ########
#######################################

"""
def apStart(stmt):
    apLINE(stmt[0],stmt)

def apLINE(numL,stmt):
    bcode.append("10")
    bcode.append(numL)
    if stmt[1] == "IF":
        apIF(stmt[1:])
    elif stmt[1] == "PRINT":
        apPrint(stmt[1:])
    elif stmt[1] == "GOTO":
        apGOTO(stmt[-1])
    elif stmt[1] == "STOP":
        apStop(stmt[1:])
    else:
        apAsgmnt(stmt[1:])

def apAsgmnt(stmt):
    for i in stmt:
        if i in ch:
            apID(i)
        elif i in "+-<=":
            apOP(i)
        else :
            apConst(i)
    
def apID(ID):
    bcode.append("11")
    a = ord(ID)-64
    bcode.append(str(a))
    
def apConst(con):
    bcode.append("12")
    bcode.append(con)

def apIF(stmt):
    bcode.append("13")
    bcode.append("0")
    apCOND(stmt[1:-1])
    apGOTO(stmt[-1])
    
def apCOND(stmt):
    for i in stmt:
        if i in ch:
            apID(i)
        elif i in "+-<=":
            apOP(i)
        else:
            apConst(i);
    
def apGOTO(stmt):
    bcode.append("14")
    bcode.append(stmt)
    
def apPrint(stmt):
    bcode.append("15")
    bcode.append("0")
    apID(stmt[-1])
    
def apStop(stmt):
    bcode.append("16")
    bcode.append("0")
    
def apOP(si):
    bcode.append("17")
    if si == "+" :
        bcode.append("1")
    elif si == "-" :
        bcode.append("2")
    elif si == "<" :
        bcode.append("3")
    elif si == "=" :
        bcode.append("4")
"""
#############################################
#################  Get Input  ###############
#############################################
infile = open(filename,"r")

for line in infile:
    a = line.strip().split(" ")
    out2.append(line.strip().split(" "))
    for i in a:
        out.append(i)

infile.close()
print(out)

############################################
##############  Parsing Part  ##############
############################################
pars.append(s_pgm)
ret = 1
while (len(pars)!=0) and ii <= len(out):
        top = pars.pop()
        if top ==(s_pgm):
            ret = d_pgm()
        elif top ==(s_line):
            ret = d_line()
        elif top ==(s_stmt):
            ret = d_stmt()
        elif top ==(s_asgmnt):
            ret = d_asgmnt()
        elif top ==(s_exp):
            ret = d_exp()
        elif top ==(s_expp):
            ret = d_expp()
        elif top ==(s_term):
            ret = d_term()
        elif top ==(s_if):
            ret = d_if()
        elif top ==(s_cond):
            ret = d_cond()
        elif top ==(s_condp):
            ret = d_condp()
        elif top ==(s_print):
            ret = d_print()
        elif top ==(s_goto):
            ret = d_goto()
        elif top ==(s_stop):
            ret = d_stop()
        elif top ==(s_line_num):
            ret = d_line_num();
            ii=ii+1
        elif top ==(s_id):
            ret = d_id();
            ii=ii+1
        elif top ==(s_IF):
            ret = d_IF();
            ii=ii+1
        elif top ==(s_PRINT):
            ret = d_PRINT();
            ii=ii+1
        elif top ==(s_GOTO):
            ret = d_GOTO();
            ii=ii+1
        elif top ==(s_STOP):
            ret = d_STOP();
            ii=ii+1
        elif top ==(s_plus):
            ret = d_plus();
            ii=ii+1
        elif top ==(s_minus):
            ret = d_minus();
            ii=ii+1
        elif top ==(s_const):
            ret = d_const();
            ii=ii+1
        elif top ==(s_less):
            ret = d_less();
            ii=ii+1
        elif top ==(s_equal):
            ret = d_equal();
            ii=ii+1
        elif top ==(s_goto_num):
            ret = d_goto_num();
            ii=ii+1

        if(ret == 0):
            isPass = reject()
            break
        

if len(pars)!=0 or ii!=len(out):
    isPass = reject()
else:
    isPass = accept()

############################################
###########  Translate Part  ###############
############################################
if isPass:
    print("\nPARSING SUCCESSFUL")
    """for i in out2:
        apStart(i)"""
    bcode.append(str(0))
    bcodestr = " ".join(bcode)
    print(bcode)
    print(bcodestr)
    outFile = open("MyBCODE.txt","w")
    outFile.write(bcodestr)
    outFile.close()
else:
    print("\nPARSING FAILED: incorrect syntax")
