import re, lexical_analyzer3,syntax_analyzer as sa, operator, copy

arithmetic_keywords = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]
comparison_keywords = ["BOTH SAEM", "DIFFRINT", "BIGGR OF", "SMALLR OF"]
boolean_keywords = ["BOTH OF", "EITHER OF", "WON OF"]
unary_keywords = ["NOT"]
infinite_keywords = ["ALL OF", "ANY OF"]
io_keywords = ["VISIBLE", "GIMMEH"]

######## PUTANGINA DAPAT MAPAGANA NATIN YUNG COMPARISON TAPOS BIGLANG MAY ARITHMETIC PUTANGINA!!!!
######## OKAY NA SER WAG NA GALET


def evaluate(nested_list,legit_symbol_table):


    if isinstance(nested_list, str):

        #dito ichecheck kung valid ba yung format ng operands
        if sa.checkInt(nested_list) or sa.checkFloat(nested_list) or sa.checkVar(nested_list):

            if sa.checkVar(nested_list):
                for elements in legit_symbol_table:
                    if nested_list == elements[0]:
                        if sa.checkInt(elements[2]):
                            return int(elements[2])
                        else:
                            return float(elements[2])

            if sa.checkInt(nested_list):
                return int(nested_list)
            else:
                return float(nested_list)

    op, operand1, an, operand2 = nested_list
    ops = {
        "SUM OF":operator.add,
        "PRODUKT OF":operator.mul,
        "DIFF OF":operator.sub,
        "QUOSHUNT OF":operator.truediv,
        "MOD OF":operator.mod,
        "BIGGR OF":max,
        "SMALLR OF":min
    }


    return ops[op](evaluate(operand1,legit_symbol_table), evaluate(operand2,legit_symbol_table))




def ANDoperator(op1,op2):
    return op1 and op2

def ORoperator(op1,op2):
    return op1 or op2

def XORoperator(op1, op2):
  return (op1 or op2) and (not op1 or not op2)


def evaluateComparison(nested_list,legit_symbol_table):
    if isinstance(nested_list, str):
        #dito ichecheck kung valid ba yung format ng operands
        if sa.checkInt(nested_list) or sa.checkFloat(nested_list) or sa.checkVar(nested_list):
            if sa.checkVar(nested_list):
                for elements in legit_symbol_table:
                    if nested_list == elements[0]:
                        if sa.checkInt(elements[2]):
                            return int(elements[2])
                        elif sa.checkFloat(elements[2]):
                            return float(elements[2])
                        elif elements[2]=="WIN":
                            return True
                        elif elements[2]=="FAIL":
                            return False

            if sa.checkInt(nested_list):
                return int(nested_list)
            elif sa.checkFloat(nested_list):
                return float(nested_list)
            elif nested_list=="WIN":
                return True
            elif nested_list=="FAIL":
                return False
    
    op, operand1, an, operand2 = nested_list
    ops = {
        "BOTH SAEM":operator.eq,
        "DIFFRINT":operator.ne,
        "BIGGR OF":max,
        "SMALLR OF":min
    }

    if isinstance(operand1, list) and operand1[0] in arithmetic_keywords:
        operand1 = str(evaluate(operand1, legit_symbol_table))
    if isinstance(operand2, list) and operand2[0] in arithmetic_keywords:
        operand2 = str(evaluate(operand2, legit_symbol_table))

    return ops[op](evaluateComparison(operand1,legit_symbol_table), evaluateComparison(operand2,legit_symbol_table))



def evaluateBoolean(nested_list,legit_symbol_table):
    if isinstance(nested_list, str) or isinstance(nested_list,bool):
        if isinstance(nested_list,bool):
            print("Nested list")
            print(nested_list)
            return nested_list
        else:
            print("nested")
            print(nested_list)
            if nested_list=="WIN":
                return True
            elif nested_list=="FAIL":
                return False

            for elements in legit_symbol_table:
                print(elements)
                print("ele")
                if elements[0]==nested_list:
                    print("pumasok??")
                    if elements[2]=="WIN":
                        return True
                    elif elements[2]=="FAIL":
                        return False
                else:
                    print("Hello")

    op, operand1, an, operand2 = nested_list
    ops = {
        "BOTH OF":ANDoperator,
        "EITHER OF":ORoperator,
        "WON OF":XORoperator
    }

    if len(operand1)==2:
        print(operand1)
        print("DITO SA OP1")
        operand1 = evaluateNot(operand1,legit_symbol_table)

    if len(operand2)==2:
        print(operand2)
        print("op2")
        operand2 = evaluateNot(operand2,legit_symbol_table)

    return ops[op](evaluateBoolean(operand1,legit_symbol_table), evaluateBoolean(operand2,legit_symbol_table))

def evaluateNot(nested_list,legit_symbol_table):
    if isinstance(nested_list, str):

        #dito ichecheck kung valid ba yung format ng operands
        if sa.checkVar(nested_list):

            if sa.checkVar(nested_list):
                for elements in legit_symbol_table:
                    if nested_list == elements[0]:
                        if elements[2]=="WIN":
                            return True
                        elif elements[2]=="FAIL":
                            return False

            if nested_list=="WIN":
                return True
            elif nested_list=="FAIL":
                return False


    op, operand1 = nested_list
    ops = {
        "NOT":operator.not_
    }
    return ops[op](evaluateComparison(operand1,legit_symbol_table))

def evaluateInfinite(infiList, legit_symbol_table):
    if infiList[0] == "ALL OF":
        failPresent = False
        for elem in infiList:
            if elem == 'AN' or elem == "ALL OF":
                continue
            else:
                if elem == "FAIL":
                    failPresent = True
                    break
                elif isinstance(elem, list):
                    if not evaluateBoolean(elem, legit_symbol_table):
                        failPresent = True
                        break
                elif sa.checkVar(elem):
                    for el in legit_symbol_table:
                        if el[0] == elem:
                            if el[2] == "FAIL":
                                failPresent = True
                                break
        if failPresent:
            return False
        return True
    else:
        winPresent = False
        for elem in infiList:
            if elem == 'AN' or elem == "ANY OF":
                continue
            else:
                if elem == "WIN":
                    winPresent = True
                    break
                elif isinstance(elem, list):
                    if not evaluateBoolean(elem, legit_symbol_table):
                        winPresent = True
                        break
                elif sa.checkVar(elem):
                    for el in legit_symbol_table:
                        if el[0] == elem:
                            if el[2] == "WIN":
                                winPresent = True
                                break
        if not winPresent:
            return False
        return True 

def SemanticsAnalyzer(symbol_table, lexemes_table,legit_symbol_table,line_table_without_groupings):

    for line in range(len(symbol_table)):

        print(symbol_table[line])

        if symbol_table[line] != []:
            if isinstance(symbol_table[line][0],list):
                if symbol_table[line][0][0] in arithmetic_keywords:

                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluate(symbol_table[line][0], legit_symbol_table)
                            elem[2] = value
                            if isinstance(value,int):
                                elem[1] = "NUMBR"
                            else:
                                elem[1] = "NUMBAR"
                    
                    print(legit_symbol_table)
                    print(">>>>>ARITHMETIC VALUE: ", value)

                elif symbol_table[line][0][0] in comparison_keywords:
                    flag = 0

                    for idx in range(len(line_table_without_groupings[line])):
                        for el in legit_symbol_table:
                            if line_table_without_groupings[line][idx] == el[0]:
                                if el[1] == "YARN Literal":
                                    flag = 1
                                elif el[1] == "Variable Identifier":
                                    for le in legit_symbol_table:
                                        if el[0] == le[0]:
                                            if le[1] == "YARN Literal":
                                                flag = 1

                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluateComparison(symbol_table[line][0], legit_symbol_table)
                            if flag == 1:
                                elem[2] = "FAIL"
                            else:
                                if value:
                                    elem[2] = "WIN"
                                else:
                                    elem[2] = "FAIL"

                            elem[1] = "TROOF"

                    print(legit_symbol_table)
                    print(">>>>>COMPARISON VALUE: ", value)


                elif symbol_table[line][0][0] in boolean_keywords:

                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluateBoolean(symbol_table[line][0], legit_symbol_table)
                            if value:
                                elem[2] = "WIN"
                            else:
                                elem[2] = "FAIL"
                            elem[1] = "TROOF"
                    print(legit_symbol_table)
                    print(">>>>>BOOLEAN VALUE: ", value)

                elif symbol_table[line][0][0] in unary_keywords:

                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluateNot(symbol_table[line][0], legit_symbol_table)
                            if value:
                                elem[2] = "WIN"
                            else:
                                elem[2] = "FAIL"
                            elem[1] = "TROOF"
                    print(legit_symbol_table)
                    print(">>>>>UNARY VALUE: ",value)

                elif symbol_table[line][0][0] in infinite_keywords:
                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluateInfinite(symbol_table[line][0], legit_symbol_table)
                            if value:
                                elem[2] = "WIN"
                            else:
                                elem[2] = "FAIL"
                            elem[1] = "TROOF"
                    
                    print(legit_symbol_table)
                    print(">>>>>INFINITE VALUE: ",value)

            else:
                for el in legit_symbol_table:
                    if el[0] == "IT":
                        el[1] = "TROOF"
                        el[2] = "FAIL"

            if symbol_table[line][0]=="VISIBLE":
                if isinstance(symbol_table[line][1],list):

                    if symbol_table[line][1][0] in arithmetic_keywords:

                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluate(symbol_table[line][1], legit_symbol_table)
                                elem[2] = value
                                if isinstance(value, int):
                                    elem[1] = "NUMBR"
                                else:
                                    elem[1] = "NUMBAR"

                        print(legit_symbol_table)
                        print(">>>>>ARITHMETIC VALUE: ",value)
                        #print("Pumasok dito")
                        # print(symbol_table[line])

                    elif symbol_table[line][1][0] in comparison_keywords:

                        flag = 0
                        #print("comparison")
                        #print("symbol table")
                        #print(symbol_table[line])
                        for idx in range(len(line_table_without_groupings[line])):
                            for el in legit_symbol_table:
                                if line_table_without_groupings[line][idx] == el[0]:
                                    if el[1] == "YARN Literal":
                                        flag = 1
                                    elif el[1] == "Variable Identifier":
                                        for le in legit_symbol_table:
                                            if el[0] == le[0]:
                                                if le[1] == "YARN Literal":
                                                    flag = 1
                            print(line_table_without_groupings[line][idx])

                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluateComparison(symbol_table[line][1], legit_symbol_table)
                                if flag == 1:
                                    elem[2] = "FAIL"
                                else:
                                    if value:
                                        elem[2] = "WIN"
                                    else:
                                        elem[2] = "FAIL"

                                elem[1] = "TROOF"

                        print(legit_symbol_table)
                        print(">>>>>COMPARISON VALUE: ",value)

                    elif symbol_table[line][1][0] in boolean_keywords:

                        print("symbol table")
                        print(symbol_table[line])

                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluateBoolean(symbol_table[line][1], legit_symbol_table)
                                if value:
                                    elem[2] = "WIN"
                                else:
                                    elem[2] = "FAIL"
                                elem[1] = "TROOF"
                        print(legit_symbol_table)
                        print(">>>>>BOOLEAN VALUE: ",value)

                    elif symbol_table[line][1][0] in unary_keywords:

                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluateNot(symbol_table[line][1], legit_symbol_table)
                                if value:
                                    elem[2] = "WIN"
                                else:
                                    elem[2] = "FAIL"
                                elem[1] = "TROOF"
                        print(legit_symbol_table)
                        print(">>>>>UNARY VALUE: ",value)

                    elif symbol_table[line][1][0] in infinite_keywords:
                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluateInfinite(symbol_table[line][0], legit_symbol_table)
                                if value:
                                    elem[2] = "WIN"
                                else:
                                    elem[2] = "FAIL"
                                elem[1] = "TROOF"
                        
                        print(legit_symbol_table)
                        print(">>>>>INFINITE VALUE: ",value)

                elif len(symbol_table[line]) == 2:
                    if symbol_table[line][1] not in arithmetic_keywords and symbol_table[line][1] not in comparison_keywords and symbol_table[line][1] not in boolean_keywords and symbol_table[line][1] not in infinite_keywords and symbol_table[line][1] not in unary_keywords and symbol_table[line][1] not in io_keywords:
                        varflag = 0
                        for ele in legit_symbol_table:
                            if symbol_table[line][1] == ele[0]:
                                storevalue = ele[2]
                                print(ele[2])
                                varflag = 1
                                for le in legit_symbol_table:
                                    if le[0] == "IT":
                                        le[2] = storevalue
                                        break

                        if varflag == 0:
                            for le in legit_symbol_table:
                                if le[0] == "IT":
                                    le[2] = symbol_table[line][1]
                                    break


                    else:
                        print("NOT VALID. STATEMENT AFTER VISIBLE IS A KEYWORD")

                elif len(symbol_table[line]) > 2:
                    printstr = ""
                    for idx in range(1,len(symbol_table[line])):
                        if symbol_table[line][idx] not in arithmetic_keywords and symbol_table[line][idx] not in comparison_keywords and symbol_table[line][idx] not in boolean_keywords and symbol_table[line][idx] not in infinite_keywords and symbol_table[line][idx] not in unary_keywords and symbol_table[line][idx] not in io_keywords:
                            varflag = 0
                            for ele in legit_symbol_table:
                                if symbol_table[line][idx] == ele[0]:
                                    storevalue = ele[2]
                                    print(ele[2])
                                    if not storevalue == None:
                                        printstr += storevalue
                                    varflag = 1
                                    # for le in legit_symbol_table:
                                    #     if le[0] == "IT":
                                    #         le[2] = storevalue
                                    #         break

                            if varflag == 0:
                                if symbol_table[line][idx] == None:
                                    print("no value yet")
                                else:
                                    printstr += symbol_table[line][idx]
                                # for le in legit_symbol_table:
                                #     if le[0] == "IT":
                                #         le[2] = symbol_table[line][1]
                                #         break


                        else:
                            print("NOT VALID. STATEMENT AFTER VISIBLE IS A KEYWORD")

                        #printstr += symbol_table[line][idx]
                    print("pumasok dito")
                    print(printstr)
                    for le in legit_symbol_table:
                        if le[0] == "IT":
                            le[2] = printstr
                            break

                print("nahanap visible")
                print(symbol_table[line])

            print(legit_symbol_table)

    for element in legit_symbol_table:
        print(element)





code7 = '''
BTW for switch
HAI
  IT R 18
  WTF?
    OMG 1
      VISIBLE "I'm the only oneeeee"
      GTFO
    OMG 3
      VISIBLE "third time's a charm"
    OMG 5
      VISIBLE "no one wants a five"
      GTFO
    OMG 7
      VISIBLE "why is six afraid of seven?"
      VISIBLE "7 8 " SUM OF IT AN 2
      GTFO
    OMG 11
      VISIBLE "Friends don't lie. -Eleven"
      GTFO
    OMG 13
      VISIBLE "birthday ni taylor swift, dec 13"
    OMG 17
      VISIBLE "seventeen right here"
    OMGWTF
      VISIBLE "ano na"
      VISIBLE IT
    OIC
KTHXBYE
'''

code6 = '''
BTW for if-else statements
HAI
  I HAS A a ITZ 12
  I HAS A b ITZ 5

  BOTH SAEM 18 AN "b"
  O RLY?
    YA RLY
      VISIBLE IT
      VISIBLE "it is the same"
      b R 17
      SUM OF b AN 5
      VISIBLE IT
    NO WAI
      VISIBLE IT
      VISIBLE "it is not!"
      b R 18
      DIFFRINT 18 AN "HELLO"
      VISIBLE IT
  OIC

KTHXBYE
'''

code5 = '''
BTW test case for variables
HAI
  BTW variable declarations
  BTW initialization of literal values
  I HAS A var1
  I HAS A var2 ITZ 17
  I HAS A var3 ITZ "seventeen"
  I HAS A var4 ITZ 5.26
  I HAS A var5 ITZ WIN

  BTW initialization of variable using variable
  I HAS A var6 ITZ var2
  BTW initialization of variable using expressions
  I HAS A var7 ITZ DIFF OF 1 AN 2
  I HAS A var8 ITZ QUOSHUNT OF 14 AN SUM OF 3 AN 9
  I HAS A var9 ITZ DIFFRINT 1 AN 1
  I HAS A var10 ITZ DIFFRINT 2 AN 1
  I HAS A var11 ITZ NOT WIN

  BTW printing for validation
  OBTW
    if your interpreter cannot print variables
    but can support variables,
    make sure that the values are updated in the symbol table
  TLDR
  BTW VISIBLE var1  // cannot be printed coz NOOB
  VISIBLE var2
  VISIBLE var3
  VISIBLE var4
  VISIBLE var5
  VISIBLE var6
  VISIBLE var7
  VISIBLE var8
  VISIBLE var9
  VISIBLE var10
  VISIBLE var11
KTHXBYE
'''

code = '''BTW for arithmetic operations
HAI
    OBTW
        if your interpreter does not implement IT,
        move the expressions to the VISIBLE statement
    TLDR
    PRODUKT OF 1 AN 2
    VISIBLE IT
    QUOSHUNT OF 1.0 AN 2
    VISIBLE IT
    MOD OF 1 AN 2
    VISIBLE IT
    BIGGR OF 1 AN 2
    VISIBLE IT
    SMALLR OF 1 AN 2
    VISIBLE IT
    BTW compound expressions
    SUM OF PRODUKT OF 3 AN 5 AN BIGGR OF DIFF OF 17 AN 2 AN 5
    VISIBLE IT
    BIGGR OF PRODUKT OF 11 AN 2 AN QUOSHUNT OF SUM OF 3 AN 5 AN 2
    VISIBLE IT
    BTW arithmetic with variables
    I HAS A var1 ITZ 5
    I HAS A var2 ITZ 3
    DIFF OF var2 AN var1
    VISIBLE IT
    MOD OF var2 AN var1
    VISIBLE IT
    BIGGR OF SUM OF var2 AN var1 AN PRODUKT OF var1 AN var2
    VISIBLE IT
    SUM OF var1 AN 12.0
    VISIBLE IT
KTHXBYE
'''

code2 = '''
BTW for assignment to variables
HAI
  I HAS A var1
  I HAS A var2
  I HAS A var3
  I HAS A var4
  I HAS A var5
  I HAS A var6
  I HAS A var7
  I HAS A var8

  BTW assignment of literals
  var1 R 17
  var2 R "seventeen"
  var3 R FAIL
  var4 R 2.18
  BTW printing...
  VISIBLE var1
  VISIBLE var2
  VISIBLE var3
  VISIBLE var4
  BTW assignment of expressions
  var5 R PRODUKT OF 1 AN 7
  var6 R WON OF WIN AN FAIL
  var7 R BOTH SAEM var1 AN var2
  var8 R EITHER OF FAIL AN FAIL
  BTW IT!!!!
  IT R "am IT"
  BTW printing...
  VISIBLE "var5 HELLO"
  VISIBLE var6
  VISIBLE var7
  VISIBLE var8
  VISIBLE IT
KTHXBYE
'''

code3 = '''
BTW for boolean and comparison operations
HAI
  BTW basic expressions
  BOTH OF WIN AN FAIL
  VISIBLE IT
  BOTH OF FAIL AN FAIL
  VISIBLE IT
  EITHER OF FAIL AN FAIL
  VISIBLE IT
  WON OF FAIL AN WIN
  VISIBLE IT
  NOT WIN
  VISIBLE IT
  ALL OF WIN AN WIN AN WIN AN FAIL AN WIN
  VISIBLE IT
  ANY OF WIN AN WIN AN WIN AN FAIL AN WIN
  VISIBLE IT
  BTW compound expressions
  BOTH OF NOT WIN AN NOT WIN
  VISIBLE IT
  EITHER OF NOT WIN AN WIN
  VISIBLE IT
  WON OF BOTH OF WIN AN WIN AN EITHER OF WIN AN FAIL
  VISIBLE IT
  ALL OF WIN AN BOTH OF WIN AN NOT FAIL AN WIN AN WON OF WIN AN NOT WIN
  VISIBLE IT
  BTW with variables
  I HAS A var1 ITZ WIN
  I HAS A var2 ITZ FAIL

  NOT var1
  VISIBLE IT
  ALL OF var1 AN WIN AN WIN AN var2 AN WIN
  VISIBLE IT
KTHXBYE
'''

code4 = '''
BTW for comparison operations
HAI
  BTW basic expressions
  BOTH SAEM 1 AN 1
  VISIBLE IT
  BOTH SAEM 1 AN 2
  VISIBLE IT
  BOTH SAEM 2 AN 2.0
  VISIBLE IT
  DIFFRINT 3 AN 4
  VISIBLE IT
  DIFFRINT 4 AN 4
  VISIBLE IT
  BTW compound expressions
  DIFFRINT 2 AN BIGGR OF 1 AN 2
  VISIBLE IT
  DIFFRINT BIGGR OF 1 AN 2 AN SMALLR OF 3 AN 2
  VISIBLE IT
  DIFFRINT SUM OF 1 AN 2 AN DIFF OF 1 AN 2
  VISIBLE IT
  BTW with variables
  I HAS A var1 ITZ WIN
  I HAS A var2 ITZ FAIL
  DIFFRINT var1 AN var2
  VISIBLE IT
  BOTH SAEM var1 AN var2
  VISIBLE IT
  NOT FAIL
  DIFFRINT BOTH SAEM var1 AN var2 AN DIFFRINT var1 AN var1
  VISIBLE IT
KTHXBYE
'''

code8 = '''
BTW for USER INPUT/OUTPUT
HAI
  BTW printing of literals
  VISIBLE "henlo"
  VISIBLE 17
  VISIBLE 1.7
  VISIBLE WIN
  BTW infinite arity printing (concat)
  VISIBLE "hi, I'm pi. My value is " 3.14
  VISIBLE "brrr " "baaa " "fa la la," " la la"
  BTW printing of expressions
  VISIBLE SUM OF 2 AN PRODUKT OF 3 AN 5
  VISIBLE BOTH SAEM 2 AN 3
  VISIBLE EITHER OF WIN AN FAIL
  BTW printing of variables and use of GIMMEH
  I HAS A input 
  VISIBLE "gif imput "
  GIMMEH input
  VISIBLE input
  VISIBLE "u gif meh " input "!"
KTHXBYE
'''


symbol_table, lexemes_table = lexical_analyzer3.LexicalAnalyzer(code2)

symbol_table,lexemes_table,legit_symbol_table,line_table_without_groupings = sa.SyntaxAnalyzer(symbol_table, lexemes_table)

SemanticsAnalyzer(symbol_table,lexemes_table,legit_symbol_table,line_table_without_groupings)

#guys tulog na tayo,
#tama na siguro to
#kung ano ano nalang problema nahahanap natin
#para tayong nag iinfinite loop
#na puro problema
#tangina
#GOODNIGHT
#MATULOG NA TAYO AWAT NA MUNA
