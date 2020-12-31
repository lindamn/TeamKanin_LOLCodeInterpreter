import re, lexical_analyzer3,syntax_analyzer as sa, operator, copy

arithmetic_keywords = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]
comparison_keywords = ["BOTH SAEM", "DIFFRINT", "BIGGR OF", "SMALLR OF"]
boolean_keywords = ["BOTH OF", "EITHER OF", "WON OF"]
unary_keywords = ["NOT"]
infinite_keywords = ["ALL OF", "ANY OF"]
io_keywords = ["VISIBLE", "GIMMEH"]

all_keywords = ["HAI", "KTHXBYE", "I HAS A", "ITZ", "VISIBLE", "GIMMEH", "IT", "SMOOSH", "ALL OF", "ANY OF", "MKAY","NOT", "AN", "SUM OF", "DIFF OF", "PRODUKT OF",
"QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF", "BOTH SAEM", "DIFFRINT", "FAIL", "WIN", "R", "O RLY?", "YA RLY", "NO WAI",
"OIC", "MEBBE", "WTF?", "OMG", "OMGWTF"]

# credits to https://stackoverflow.com/a/40775654
def evaluate(nested_list,legit_symbol_table):

    if isinstance(nested_list, str):

        #dito ichecheck kung valid ba yung format ng operands
        if sa.checkInt(nested_list) or sa.checkFloat(nested_list) or sa.checkVar(nested_list):
            
            if sa.checkVar(nested_list):
                for elements in legit_symbol_table:
                    if nested_list == elements[0]:
                        if sa.checkInt(elements[2]):
                            return int(elements[2])
                        elif sa.checkFloat(nested_list):
                            return float(elements[2])
                        else:
                            return None

            if sa.checkInt(nested_list):
                return int(nested_list)
            elif sa.checkFloat(nested_list):
                return float(nested_list)
            else:
                return None

    op, operand1, an, operand2 = nested_list
    ops = {
        "SUM OF":ADDoperator,
        "PRODUKT OF":MULTIPLYoperator,
        "DIFF OF":SUBTRACToperator,
        "QUOSHUNT OF":DIVIDEoperator,
        "MOD OF":MODULOoperator,
        "BIGGR OF":MAXoperator,
        "SMALLR OF":MINoperator
    }
    return ops[op](evaluate(operand1,legit_symbol_table), evaluate(operand2,legit_symbol_table))

def NOToperator(op1):
    if op1 == None:
        return None
    return not op1

def MAXoperator(op1, op2):
    if op1 == None or op2 == None:
        return None
    if op1 >= op2:
        return op1
    else:
        return op2

def MINoperator(op1, op2):
    if op1 == None or op2 == None:
        return None
    if op1 <= op2:
        return op1
    else:
        return op2   

def ADDoperator(op1,op2):
    if op1 == None or op2 == None:
        return None
    return op1 + op2

def MULTIPLYoperator(op1,op2):
    if op1 == None or op2 == None:
        return None
    return op1 * op2

def SUBTRACToperator(op1,op2):
    if op1 == None or op2 == None:
        return None
    return op1 - op2

def DIVIDEoperator(op1,op2):
    if op1 == None or op2 == None:
        return None
    return op1 / op2

def MODULOoperator(op1,op2):
    if op1 == None or op2 == None:
        return None
    return op1 % op2

def ANDoperator(op1,op2):
    if op1 == None or op2 == None:
        return None
    return op1 and op2

def ORoperator(op1,op2):
    if op1 == None or op2 == None:
        return None
    return op1 or op2

def XORoperator(op1, op2):
    if op1 == None or op2 == None:
        return None
    return (op1 or op2) and (not op1 or not op2)

def EQUALSoperator(op1, op2):
    if op1 == None or op2 == None:
        return None
    return op1 == op2

def NOTEQUALoperator(op1, op2):
    if op1 == None or op2 == None:
        return None
    return op1 != op2

def evaluateComparison(nested_list,legit_symbol_table):
    if isinstance(nested_list, str):

        #dito ichecheck kung valid ba yung format ng operands
        if sa.checkInt(nested_list) or sa.checkFloat(nested_list) or sa.checkVar(nested_list):

            if sa.checkVar(nested_list):
                for elements in legit_symbol_table:
                    if nested_list == elements[0]:
                        # # print("nahanap niya sa symbol table legit")
                        # # print(nested_list)
                        # # print(elements[2])
                        if sa.checkInt(elements[2]):
                            return int(elements[2])
                        elif sa.checkFloat(elements[2]):
                            return float(elements[2])
                        elif elements[2]=="WIN":
                            return True
                        elif elements[2]=="FAIL":
                            return False
                        elif re.match(r"[\"]([^\"]*?)[\"]",elements[2]):
                            return False
                        else:
                            return none

            if sa.checkInt(nested_list):
                return int(nested_list)
            elif sa.checkFloat(nested_list):
                return float(nested_list)
            elif nested_list=="WIN":
                return True
            elif nested_list=="FAIL":
                return False
            else:
                return None


    op, operand1, an, operand2 = nested_list
    ops = {
        "BOTH SAEM":EQUALSoperator,
        "DIFFRINT":NOTEQUALoperator,
        "BIGGR OF":MAXoperator,
        "SMALLR OF":MINoperator
    }

    if isinstance(operand1, list) and operand1[0] in arithmetic_keywords:
        operand1 = str(evaluate(operand1, legit_symbol_table))
    if isinstance(operand2, list) and operand2[0] in arithmetic_keywords:
        operand2 = str(evaluate(operand2, legit_symbol_table))

    return ops[op](evaluateComparison(operand1,legit_symbol_table), evaluateComparison(operand2,legit_symbol_table))

def evaluateBoolean(nested_list,legit_symbol_table):

    if isinstance(nested_list, str) or isinstance(nested_list,bool):
        if isinstance(nested_list,bool):
            return nested_list
        else:
            if nested_list=="WIN":
                return True
            elif nested_list=="FAIL":
                return False
            else:
                return None

            for elements in legit_symbol_table:
                if elements[0]==nested_list:
                    if elements[2]=="WIN":
                        return True
                    elif elements[2]=="FAIL":
                        return False
                    else:
                        return None

    op, operand1, an, operand2 = nested_list
    ops = {
        "BOTH OF":ANDoperator,
        "EITHER OF":ORoperator,
        "WON OF":XORoperator
    }

    if len(operand1)==2:
        operand1 = evaluateNot(operand1,legit_symbol_table)

    if len(operand2)==2:
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
                        else:
                            return None

            if nested_list=="WIN":
                return True
            elif nested_list=="FAIL":
                return False
            else:
                return None


    op, operand1 = nested_list
    ops = {
        "NOT":NOToperator
    }
    return ops[op](evaluateComparison(operand1,legit_symbol_table))

def evaluateInfinite(infiList, legit_symbol_table):

    if infiList[0] == "ALL OF":
        failPresent = False
        for elem in infiList:
            if elem == 'AN' or elem == "ALL OF" or elem == "MKAY":
                continue
            else:
                if elem == "FAIL":
                    failPresent = True
                    break
                elif elem == "WIN":
                    continue
                elif isinstance(elem, list):
                    value = evaluateBoolean(elem, legit_symbol_table)
                    if value == None:
                        return None
                    if not value:
                        failPresent = True
                        break
                elif sa.checkVar(elem):
                    for el in legit_symbol_table:
                        if el[0] == elem:
                            if el[2] == "FAIL":
                                failPresent = True
                                break
                            elif el[2] == "WIN":
                                continue
                            else:
                                return None
                else:
                    return None
        if failPresent:
            return False
        return True
    else:
        winPresent = False
        for elem in infiList:
            if elem == 'AN' or elem == "ANY OF" or elem == "MKAY":
                continue
            else:
                if elem == "WIN":
                    winPresent = True
                    break
                elif elem == "FAIL":
                    continue
                elif isinstance(elem, list):
                    value = evaluateBoolean(elem, legit_symbol_table)
                    if value == None:
                        return None
                    if value:
                        winPresent = True
                        break
                elif sa.checkVar(elem):
                    for el in legit_symbol_table:
                        if el[0] == elem:
                            if el[2] == "WIN":
                                winPresent = True
                                break
                            elif el[2] == "FAIL":
                                continue
                            else:
                                return None
                else:
                    return None
        if not winPresent:
            return False
        return True


def SemanticsAnalyzer(starting_line,symbol_table, lexemes_table,legit_symbol_table,line_table_without_groupings):

    visible_list = []

    obtw_flag = False

    orly_flag = False
    yarly_chosen = False
    nowai_chosen = False
    yarly_flag = False
    nowai_flag = False
    goeval_flag = False

    wtf_flag = False
    omg_flag = False
    omgwtf_flag = False
    switch_flag = False

    current_line = starting_line

    for line in range(starting_line, len(symbol_table)):
        ## print("HELLLLLLLLLLLLLLLLLLLLLLLLLL")
        ## print(symbol_table[line][0])
        ## print("marker")
        # print(symbol_table[line])
        if symbol_table[line] != []:

            if symbol_table[line][0] == "WTF?": 
                wtf_flag = True

            if symbol_table[line][0] == "GTFO":
                switch_flag = False

            if symbol_table[line][0] == "OMGWTF" and switch_flag == False and omg_flag == False:
                switch_flag = True
                omg_flag = True

            if symbol_table[line][0] == "OMG" and wtf_flag == True:
                # print("Hello OMG")
                # print(symbol_table[line][1])
                for ele in legit_symbol_table:
                    if ele[0] == "IT":
                        # print(ele[2])
                        if ele[2] == symbol_table[line][1]:
                            switch_flag = True
                            omg_flag = True
                            

            if symbol_table[line][0] == "OIC" and orly_flag == False and wtf_flag == True:
                wtf_flag = False

            if symbol_table[line][0]=="O RLY?":
                # print("PUMASOK SA ORLY")
                orly_flag = True
                for ele in legit_symbol_table:
                    if ele[0] == "IT":
                        if ele[2] =="WIN":
                            yarly_chosen = True
                            goeval_flag = True
                        else:
                            nowai_chosen = True
                            goeval_flag = False

                # print("goeval flag")
                # print(goeval_flag)

            if symbol_table[line][0] == "YA RLY" and yarly_chosen == True:
                yarly_flag = True

            if symbol_table[line][0] == "NO WAI":
                if nowai_chosen:
                    goeval_flag = True
                    nowai_flag = True
                else:
                    goeval_flag = False

            if symbol_table[line][0] == "OIC" and orly_flag == True:
                orly_flag = False
                nowai_flag = False
                goeval_flag = False

            if (orly_flag == True and goeval_flag == True) or (orly_flag == False and wtf_flag == False) or (switch_flag == True and wtf_flag == True):

                # print("pumasok dito sa pag evaluate")
                # print("orly flag: ",end="")
                # print(orly_flag)
                # print('goeval_flag: ',end="")
                # print(goeval_flag)
                
                #check if there are variables that do not exist in the symbol table
                for index in range(0,len(line_table_without_groupings[line])):
                    #if keyword is a reserved keyword/int/float/str, just skip
                    if isinstance(line_table_without_groupings[line][index], int) or isinstance(line_table_without_groupings[line][index], float):
                        continue
                    elif line_table_without_groupings[line][index] in all_keywords or re.match(r"\-{0,1}[0-9]{1,}$",line_table_without_groupings[line][index]) or re.match(r"\-{0,1}[0-9]{1,}\.[0-9]{1,}$", line_table_without_groupings[line][index]) or re.match(r"[\"]([^\"]*?)[\"]", line_table_without_groupings[line][index]):
                        continue
                    else: #if it is a varident
                        initialized_flag = False
                        for k in range(0,len(legit_symbol_table)):
                            if legit_symbol_table[k][0] == line_table_without_groupings[line][index]:
                                initialized_flag = True
                                break
                        if initialized_flag == False:
                            visible_list.append("ERROR: Semantic error, variable has not been initialized yet but still used at line " + str(current_line+1))
                            return visible_list, legit_symbol_table

                if isinstance(symbol_table[line][0],list):
                    if symbol_table[line][0][0] in arithmetic_keywords:

                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluate(symbol_table[line][0], legit_symbol_table)
                                if value == None:
                                    # # print("?!?!?!JDSKJDKSJDKSJD")
                                    visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                    return visible_list, legit_symbol_table
                                elem[2] = value
                                if isinstance(value,int):
                                    elem[1] = "NUMBR"
                                else:
                                    elem[1] = "NUMBAR"

                        # print(value)

                    elif symbol_table[line][0][0] in comparison_keywords:
                        flag = 0
                        # print(symbol_table[line])
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
                            # print(line_table_without_groupings[line][idx])


                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluateComparison(symbol_table[line][0], legit_symbol_table)
                                if value == None:
                                    visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                    return visible_list, legit_symbol_table
                                if flag == 1:
                                    elem[2] = "FAIL"
                                else:
                                    if value:
                                        elem[2] = "WIN"
                                    else:
                                        elem[2] = "FAIL"

                                elem[1] = "TROOF"

                        # print("help")
                        # print(symbol_table[line][0])
                        # print(legit_symbol_table)
                        # print(value)

                    elif symbol_table[line][0][0] in boolean_keywords:


                        # print("symbol table")
                        # print(symbol_table[line])

                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluateBoolean(symbol_table[line][0], legit_symbol_table)
                                if value == None:
                                    visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                    return visible_list, legit_symbol_table
                                if value:
                                    elem[2] = "WIN"
                                else:
                                    elem[2] = "FAIL"
                                elem[1] = "TROOF"
                        # print(legit_symbol_table)
                        # print(value)

                    elif symbol_table[line][0][0] in unary_keywords:

                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluateNot(symbol_table[line][0], legit_symbol_table)
                                if value == None:
                                    visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                    return visible_list, legit_symbol_table
                                if value:
                                    elem[2] = "WIN"
                                else:
                                    elem[2] = "FAIL"
                                elem[1] = "TROOF"
                        # print(legit_symbol_table)
                        # print(value)

                    elif symbol_table[line][0][0] in infinite_keywords:

                        for elem in legit_symbol_table:
                            if elem[0] == "IT":
                                value = evaluateInfinite(symbol_table[line][0], legit_symbol_table)
                                if value == None:
                                    visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                    return visible_list, legit_symbol_table
                                if value:
                                    elem[2] = "WIN"
                                else:
                                    elem[2] = "FAIL"
                                elem[1] = "TROOF"

                        # print(legit_symbol_table)
                        # print(">>>>>INFINITE VALUE: ", value)

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
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    elem[2] = value
                                    if isinstance(value, int):
                                        elem[1] = "NUMBR"
                                    else:
                                        elem[1] = "NUMBAR"


                            # print(value)
                            # print("Pumasok dito")
                            # # print(symbol_table[line])

                        elif symbol_table[line][1][0] in comparison_keywords:

                            flag = 0
                            # print("comparison")
                            # print("symbol table")
                            # print(symbol_table[line])
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
                                # print(line_table_without_groupings[line][idx])

                            for elem in legit_symbol_table:
                                if elem[0] == "IT":
                                    value = evaluateComparison(symbol_table[line][1], legit_symbol_table)
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    if flag == 1:
                                        elem[2] = "FAIL"
                                    else:
                                        if value:
                                            elem[2] = "WIN"
                                        else:
                                            elem[2] = "FAIL"

                                    elem[1] = "TROOF"

                            # print(legit_symbol_table)
                            # print(value)

                        elif symbol_table[line][1][0] in boolean_keywords:

                            # print("symbol table")
                            # print(symbol_table[line])

                            for elem in legit_symbol_table:
                                if elem[0] == "IT":
                                    value = evaluateBoolean(symbol_table[line][1], legit_symbol_table)
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    if value:
                                        elem[2] = "WIN"
                                    else:
                                        elem[2] = "FAIL"
                                    elem[1] = "TROOF"
                            # print(legit_symbol_table)
                            # print(value)

                        elif symbol_table[line][1][0] in unary_keywords:

                            for elem in legit_symbol_table:
                                if elem[0] == "IT":
                                    value = evaluateNot(symbol_table[line][1], legit_symbol_table)
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    if value:
                                        elem[2] = "WIN"
                                    else:
                                        elem[2] = "FAIL"
                                    elem[1] = "TROOF"
                            # print(legit_symbol_table)
                            # print(value)

                        elif symbol_table[line][1][0] in infinite_keywords:

                            for elem in legit_symbol_table:
                                if elem[0] == "IT":
                                    value = evaluateInfinite(symbol_table[line][1], legit_symbol_table)
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    if value:
                                        elem[2] = "WIN"
                                    else:
                                        elem[2] = "FAIL"
                                    elem[1] = "TROOF"

                            # print(legit_symbol_table)
                            # print(">>>>>INFINITE VALUE: ", value)

                        visible_list.append(value)

                    elif len(symbol_table[line]) == 2:
                        if symbol_table[line][1] not in arithmetic_keywords and symbol_table[line][1] not in comparison_keywords and symbol_table[line][1] not in boolean_keywords and symbol_table[line][1] not in infinite_keywords and symbol_table[line][1] not in unary_keywords and symbol_table[line][1] not in io_keywords:
                            varflag = 0
                            for ele in legit_symbol_table:
                                if symbol_table[line][1] == ele[0]:
                                    storevalue = ele[2]
                                    # print(ele[2])
                                    varflag = 1
                                  #  for le in legit_symbol_table:
                                   #     if le[0] == "IT":
                                    #        le[2] = storevalue
                                     #       break
                            if varflag == 0:
                                if re.match(r"[\"]([^\"]*?)[\"]", symbol_table[line][1]):
                                    visible_list.append(symbol_table[line][1][1:-1])
                                else:
                                    visible_list.append(symbol_table[line][1])
                            else:
                                visible_list.append(storevalue)

                           #if varflag == 0:
                            #    # print("para lang may laman")
                                # for le in legit_symbol_table:
                                #     if le[0] == "IT":
                                #         le[2] = symbol_table[line][1]
                                #         break


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
                                        # print(ele[2])
                                        if not storevalue == None:
                                            if re.match(r"[\"]([^\"]*?)[\"]", storevalue):
                                                printstr += storevalue[1:-1]
                                            else:
                                                printstr += storevalue
                                        varflag = 1

                                if varflag == 0:
                                    if symbol_table[line][idx] == None:
                                        print("no value yet")
                                    else:
                                        if isinstance(symbol_table[line][idx],list):
                                            if symbol_table[line][idx][0] in arithmetic_keywords:
                                                value = evaluate(symbol_table[line][idx],legit_symbol_table)
                                            elif symbol_table[line][idx][0] in comparison_keywords:
                                                value = evaluateComparison(symbol_table[line][idx],legit_symbol_table)
                                            elif symbol_table[line][idx][0] in boolean_keywords:
                                                value = evaluateBoolean(symbol_table[line][idx],legit_symbol_table)
                                            elif symbol_table[line][idx][0] in unary_keywords:
                                                value = evaluateNot(symbol_table[line][idx],legit_symbol_table)
                                            elif symbol_table[line][idx][0] in infinite_keywords:
                                                value = evaluateInfinite(symbol_table[line][idx],legit_symbol_table)

                                            printstr += str(value)
                                        else:
                                            if re.match(r"[\"]([^\"]*?)[\"]",symbol_table[line][idx]):
                                                printstr += symbol_table[line][idx][1:-1]
                                            else:
                                                printstr += symbol_table[line][idx]

                            else:
                                print("NOT VALID. STATEMENT AFTER VISIBLE IS A KEYWORD")

                            #printstr += symbol_table[line][idx]
                        # print"pumasok dito")
                        visible_list.append(printstr)
                        # printprintstr)

                        # for le in legit_symbol_table:
                        #     if le[0] == "IT":
                        #         le[2] = printstr
                        #         break

                    # print"nahanap visible")
                    # printsymbol_table[line])

                if symbol_table[line][0]=="I HAS A":
                    # printsymbol_table[line])

                    if len(symbol_table[line]) == 4:

                        if symbol_table[line][2] == "ITZ":

                            #ETO NA PO PAG MAY VARIABLE ASSIGNMENT DITO GAGAWEN
                            if isinstance(symbol_table[line][3], list):
                                # print"LIST NAMAN PO LAMAN. DAPAT NAG EVALUATE")
                                if symbol_table[line][3][0] in arithmetic_keywords:

                                    for elem in legit_symbol_table:
                                        if elem[0] == symbol_table[line][1]:
                                            value = evaluate(symbol_table[line][3], legit_symbol_table)
                                            if value == None:
                                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                                return visible_list, legit_symbol_table
                                            elem[2] = value
                                            if isinstance(value, int):
                                                elem[1] = "NUMBR"
                                            else:
                                                elem[1] = "NUMBAR"

                                    # printvalue)

                                elif symbol_table[line][3][0] in comparison_keywords:
                                    flag = 0
                                    # printsymbol_table[line])
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
                                        # printline_table_without_groupings[line][idx])

                                    for elem in legit_symbol_table:
                                        if elem[0] == symbol_table[line][1]:
                                            value = evaluateComparison(symbol_table[line][3], legit_symbol_table)
                                            if value == None:
                                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                                return visible_list, legit_symbol_table
                                            if flag == 1:
                                                elem[2] = "FAIL"
                                            else:
                                                if value:
                                                    elem[2] = "WIN"
                                                else:
                                                    elem[2] = "FAIL"

                                            elem[1] = "TROOF"

                                    # print"help")
                                    # printsymbol_table[line][0])
                                    # printlegit_symbol_table)
                                    # printvalue)

                                elif symbol_table[line][3][0] in boolean_keywords:

                                    # print"symbol table")
                                    # printsymbol_table[line])

                                    for elem in legit_symbol_table:
                                        if elem[0] == symbol_table[line][1]:
                                            value = evaluateBoolean(symbol_table[line][3], legit_symbol_table)
                                            if value == None:
                                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                                return visible_list, legit_symbol_table
                                            if value:
                                                elem[2] = "WIN"
                                            else:
                                                elem[2] = "FAIL"
                                            elem[1] = "TROOF"
                                    # printlegit_symbol_table)
                                    # printvalue)

                                elif symbol_table[line][3][0] in unary_keywords:

                                    for elem in legit_symbol_table:
                                        if elem[0] == symbol_table[line][1]:
                                            value = evaluateNot(symbol_table[line][3], legit_symbol_table)
                                            if value == None:
                                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                                return visible_list, legit_symbol_table
                                            if value:
                                                elem[2] = "WIN"
                                            else:
                                                elem[2] = "FAIL"
                                            elem[1] = "TROOF"
                                    # printlegit_symbol_table)
                                    # print"NANDITOOOO")
                                    # printvalue)

                                elif symbol_table[line][0][0] in infinite_keywords:

                                    for elem in legit_symbol_table:
                                        if elem[0] == symbol_table[line][1]:
                                            value = evaluateInfinite(symbol_table[line][3], legit_symbol_table)
                                            if value == None:
                                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                                return visible_list, legit_symbol_table
                                            if value:
                                                elem[2] = "WIN"
                                            else:
                                                elem[2] = "FAIL"
                                            elem[1] = "TROOF"

                                    # printlegit_symbol_table)
                                    # print">>>>>INFINITE VALUE: ", value)

                            else:
                                # print"DAPAT DITO KA PAPASOK VAR6")
                                for ele in legit_symbol_table:
                                    if ele[0] == symbol_table[line][1]:
                                        indexofdest = legit_symbol_table.index(ele)

                                for ele in legit_symbol_table:
                                    if ele[0] == symbol_table[line][3]:
                                        legit_symbol_table[indexofdest][1] = ele[1]
                                        legit_symbol_table[indexofdest][2] = ele[2]
                                        #ele[2] = symbol_table[line][2]
                                        break


                if symbol_table[line][0] in arithmetic_keywords:

                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluate(symbol_table[line], legit_symbol_table)
                            if value == None:
                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                return visible_list, legit_symbol_table
                            elem[2] = value
                            if isinstance(value, int):
                                elem[1] = "NUMBR"
                            else:
                                elem[1] = "NUMBAR"

                    # printvalue)
                    # print"Pumasok dito")
                    # # printsymbol_table[line])

                elif symbol_table[line][0] in comparison_keywords:

                    flag = 0
                    # print"comparison")
                    # print"symbol table nonoo")
                    # printsymbol_table[line])
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
                        # print(line_table_without_groupings[line][idx])

                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluateComparison(symbol_table[line], legit_symbol_table)
                            if value == None:
                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                return visible_list, legit_symbol_table
                            if flag == 1:
                                elem[2] = "FAIL"
                            else:
                                if value:
                                    elem[2] = "WIN"
                                else:
                                    elem[2] = "FAIL"

                            elem[1] = "TROOF"

                    # print(legit_symbol_table)
                    # print(value)

                elif symbol_table[line][0] in boolean_keywords:

                    # print("symbol table")
                    # print(symbol_table[line])

                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluateBoolean(symbol_table[line], legit_symbol_table)
                            if value == None:
                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                return visible_list, legit_symbol_table
                            if value:
                                elem[2] = "WIN"
                            else:
                                elem[2] = "FAIL"
                            elem[1] = "TROOF"
                    # print(legit_symbol_table)
                    # print(value)

                elif symbol_table[line][0] in unary_keywords:

                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluateNot(symbol_table[line], legit_symbol_table)
                            if value == None:
                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                return visible_list, legit_symbol_table
                            if value:
                                elem[2] = "WIN"
                            else:
                                elem[2] = "FAIL"
                            elem[1] = "TROOF"
                    # print(legit_symbol_table)
                    # print(value)

                elif symbol_table[line][0] in infinite_keywords:

                    for elem in legit_symbol_table:
                        if elem[0] == "IT":
                            value = evaluateInfinite(symbol_table[line], legit_symbol_table)
                            if value == None:
                                visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                return visible_list, legit_symbol_table
                            if value:
                                elem[2] = "WIN"
                            else:
                                elem[2] = "FAIL"
                            elem[1] = "TROOF"

                    # print(legit_symbol_table)
                    # print(">>>>>INFINITE VALUE: ", value)

                elif len(symbol_table[line]) > 2 and symbol_table[line][1] == "R":
                    if isinstance(symbol_table[line][2],list):

                        if symbol_table[line][2][0] in arithmetic_keywords:

                            for elem in legit_symbol_table:
                                if elem[0] == symbol_table[line][0]:
                                    value = evaluate(symbol_table[line][2], legit_symbol_table)
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    elem[2] = value
                                    if isinstance(value, int):
                                        elem[1] = "NUMBR"
                                    else:
                                        elem[1] = "NUMBAR"

                            # print(value)
                            # print("Pumasok dito")
                            # # print(symbol_table[line])

                        elif symbol_table[line][2][0] in comparison_keywords:

                            flag = 0
                            # print("comparison")
                            # print("symbol table nonoo")
                            # print(symbol_table[line])
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
                                # print(line_table_without_groupings[line][idx])

                            for elem in legit_symbol_table:
                                if elem[0] == symbol_table[line][0]:
                                    # print("BAGO PUMASOK WAIT LANG")
                                    # print(symbol_table[line][2])
                                    value = evaluateComparison(symbol_table[line][2], legit_symbol_table)
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    if flag == 1:
                                        elem[2] = "FAIL"
                                    else:
                                        if value:
                                            elem[2] = "WIN"
                                        else:
                                            elem[2] = "FAIL"

                                    elem[1] = "TROOF"

                            # print(legit_symbol_table)
                            # print(value)

                        elif symbol_table[line][2][0] in boolean_keywords:

                            # print("symbol table")
                            # print(symbol_table[line])

                            for elem in legit_symbol_table:
                                if elem[0] == symbol_table[line][0]:
                                    value = evaluateBoolean(symbol_table[line][2], legit_symbol_table)
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    if value:
                                        elem[2] = "WIN"
                                    else:
                                        elem[2] = "FAIL"
                                    elem[1] = "TROOF"
                            # print(legit_symbol_table)
                            # print(value)

                        elif symbol_table[line][2][0] in unary_keywords:

                            for elem in legit_symbol_table:
                                if elem[0] == symbol_table[line][0]:
                                    value = evaluateNot(symbol_table[line][2], legit_symbol_table)
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    if value:
                                        elem[2] = "WIN"
                                    else:
                                        elem[2] = "FAIL"
                                    elem[1] = "TROOF"
                            # print(legit_symbol_table)
                            # print(value)

                        elif symbol_table[line][2][0] in infinite_keywords:

                            for elem in legit_symbol_table:
                                if elem[0] == symbol_table[line][0]:
                                    value = evaluateInfinite(symbol_table[line][2], legit_symbol_table)
                                    if value == None:
                                        visible_list.append("ERROR: Semantic error, incorrect data type to evaluate at line " + str(current_line+1))
                                        return visible_list, legit_symbol_table
                                    if value:
                                        elem[2] = "WIN"
                                    else:
                                        elem[2] = "FAIL"
                                    elem[1] = "TROOF"

                            # print(legit_symbol_table)
                            # print(">>>>>INFINITE VALUE: ", value)

                    else:
                        for ele in legit_symbol_table:
                            if ele[0] == symbol_table[line][0]:
                                ele[2] = symbol_table[line][2]

                elif symbol_table[line][0] == "GIMMEH":
                    return visible_list, current_line, lexemes_table, legit_symbol_table, line_table_without_groupings
            # print(legit_symbol_table)
        current_line += 1
    # for element in legit_symbol_table:
    #     print(element)

    return visible_list, current_line, lexemes_table, legit_symbol_table, line_table_without_groupings