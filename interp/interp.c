
// retro basic

// interp.c   1 Nov 2018
//    generate listing from B-code, (disassembling)
//	  B-code interpreter
//    P Chongstitvatana

#include "lister.h"

#define head(x) bcode[(x)]
#define tail(x) bcode[(x)+1]
#define sethead(x,v)  bcode[(x)] = (v)
#define settail(x,v)  bcode[(x)+1] = (v)

void dumpvar(int n);

int bcode[MAXCODE];					// b-code stored as array of int
int toktype, tokvalue;				// current token: type, value
int ip;								// current B-code pointer
int runflag;
int var[30];						// variable array A..Z

// read input file into bcode[]
void readinfile(char *fname) {
    FILE *fp;
    int n, i;

    fp = fopen(fname,"rt");
    if( fp == NULL ) {
        printf("cannot open : %s\n",fname);
        exit(-1);
    }
	i = 0;
	while( fscanf(fp,"%d",&n) != (int)EOF ){
		bcode[i] = n;
		i++;
	}
    fclose(fp);
}

void dumpbcode(void){
	int i;
	i = 0;
	while( head(i) != 0 ){
		printf("%d %d ",head(i),tail(i));
		i += 2;
	}
	printf("\n");
}

// print id, check that it is in range A..Z 1..26
// ascii of A is 65
void print_id(int value){
	if( value >= 1 && value <= 26 )
		printf("%c ",value+64);
	else
		printf("undef ");
}

// print if bcode is valid
void listing(void){
	int i, type, value;
	i = 0;
	while( head(i) != 0 ){
		type = head(i);
		value = tail(i);
		switch(type){
		case t_line: printf("\n%d ",value); break;
		case t_id: print_id(value); break;
		case t_const: printf("%d ",value); break;
		case t_if: printf("IF "); break;
		case t_goto: printf("GOTO %d ",value); break;
		case t_print: printf("PRINT "); break;
		case t_stop: printf("STOP ");
		case t_op:
			switch(value){
			case op_plus: printf("+ "); break;
			case op_minus: printf("- "); break;
			case op_lt: printf("< "); break;
			case op_eq: printf("= "); break;
			}
			break;
		}
		i += 2;
	}
	printf("\n");
}

void error(char* msg){
	printf("%s\n",msg);
//	dumpvar(1);			// print variable A...
	exit(1);
}

// scan for line_num n and return index to B-code
int findline(int n){
	int i;
	i = 0;
	while( head(i) != 0 ){
		if( head(i) == t_line && tail(i) == n ) return i;
		i += 2;
	}
	return -1;		// fail
}

// scan for GOTO and convert line_num to index to B-code
void convert_goto(void){
	int i, x, type, value;
	i = 0;
	while( head(i) != 0 ){
		type = head(i);
		value = tail(i);
		if( type == t_goto){
			x = findline(value);
			if( x < 0 )
				error("error GOTO");
			settail(i,x);
		}
		i += 2;
	}
}

// get next token at ip + 2
void nexttoken(void){
	ip += 2;
	toktype = head(ip);
	tokvalue = tail(ip);
//	printf("next token %d %d\n",toktype, tokvalue);
}

// get next token without advancing ip
void lookahead(void){
	toktype = head(ip+2);
	tokvalue = tail(ip+2);
//	printf("lookahead token %d %d\n",toktype,tokvalue);
}

void line_num(void){
	if(toktype != t_line)
		error("expect Line Num");

	printf("# %d\n",tokvalue);
	nexttoken();
}

void setvar(int left, int right){
	printf("set %c with %d\n",left+64,right);
	var[left] = right;
}

int getvar(int idx){
	return var[idx];
}

int term(void){
	nexttoken();
	if(toktype == t_id) return getvar(tokvalue);
	if(toktype == t_const) return tokvalue;
	error("error term");
	return 0;
}

int exp(void){
	int a1, a2;
	a1 = term();
	lookahead();
	if( toktype == t_op && tokvalue == op_plus ){
		nexttoken();	// skip +
		a2 = term();
		return a1 + a2;
	}else if( toktype == t_op && tokvalue == op_minus){
		nexttoken();	// skip -
		a2 = term();
		return a1 - a2;
	}
	return a1;			// only term
}

void asgmt(void){
	int lhs, rhs;
	lhs = tokvalue;
	nexttoken();
	if( toktype != t_op || tokvalue != op_eq )
	   error("error expect =\n");

	rhs = exp();
	setvar(lhs,rhs);	// assign value to variable
	nexttoken();
}

void gotostmt(void){
	ip = tokvalue -2 ;
//	printf("goto %d\n",ip);
	nexttoken();
}

int cond(void){
	int a1, a2;
	a1 = term();
	nexttoken();
	if( toktype == t_op && tokvalue == op_lt ){
		a2 = term();
		return a1 < a2;
	}else if( toktype == t_op && tokvalue == op_eq){
		a2 = term();
		return a1 = a2;
	}
	return 0;
}

void ifstmt(void){
	int flag;
	flag = cond();
	printf("boolean %d\n",flag);
	nexttoken();
	if( toktype == t_goto ){
	   if( flag ) gotostmt();
	   else nexttoken();
	}
	else error("error goto");
}

void printstmt(void){
	nexttoken();
	if( toktype != t_id) error("error expect id");
	printf("<%d>\n",getvar(tokvalue));
	nexttoken();
}

// check the first set and call the correct rule
void stmt(void){
	switch(toktype){
	case t_id: asgmt(); break;
	case t_if: ifstmt(); break;
	case t_goto: gotostmt(); break;
	case t_print: printstmt(); break;
	case t_stop: runflag = 0; printf("stop\n"); break;
	otherwise: printf("error stmt\n"); break;
	}
}

void interp(void){
	if( runflag != 0 ){
		line_num();
		stmt();
		interp();
	}
}
//  for debugging, dump variables
void dumpvar(int n){
	int i;
	for(i = 1; i<=n; i++)
		printf("%c %d\n",i+64,var[i]);
}

char source[80];	// input file name

int main( int argc, char *argv[] ){

	if( argc < 2 ) {
		printf("usage : lister source\n");
		exit(-1);
	}
	strcpy(source,argv[1]);
	readinfile(source);
	dumpbcode();
	listing();
	printf("\nrun\n\n");
	convert_goto();
//	listing();
	ip = -2;
	runflag = 1;
	nexttoken();
	interp();
//	dumpvar(1);
	return 0;
}

