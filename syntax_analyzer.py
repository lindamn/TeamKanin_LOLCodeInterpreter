import re, lexical_analyzer3, operator, copy

arithmetic_keywords = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]
comparison_keywords = ["BOTH SAEM", "DIFFRINT", "BIGGR OF", "SMALLR OF"]
boolean_keywords = ["BOTH OF", "EITHER OF", "WON OF"]
unary_keywords = ["NOT"]
infinite_keywords = ["ALL OF", "ANY OF", "MKAY"]
io_keywords = ["VISIBLE", "GIMMEH"]

all_keywords = ["HAI", "KTHXBYE", "I HAS A", "ITZ", "VISIBLE", "GIMMEH", "IT", "SMOOSH", "ALL OF", "ANY OF", "MKAY","NOT", "AN", "SUM OF", "DIFF OF", "PRODUKT OF",
"QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF", "BOTH SAEM", "DIFFRINT", "FAIL", "WIN", "R", "O RLY?", "YA RLY", "NO WAI",
"OIC", "MEBBE", "WTF?", "OMG", "OMGWTF"]


def SyntaxAnalyzer(symbol_table, lexemes_table):

    line_table_without_groupings = copy.deepcopy(symbol_table)
    legit_symbol_table = []
    
    orly_flag = False
    yarly_flag = False
    nowai_flag = False
    
    wtf_flag = False
    omg_flag = False
    omgwtf_flag = False

    # implicit IT variable initialize
    it_variable = ["IT", "NOOB", None, None]
    legit_symbol_table.append(it_variable)

    #initial checkers
    codeDelimiters = checkCodeDelimiter(symbol_table)
    if codeDelimiters != True:
        return codeDelimiters
    
    soloKeywords = checkSoloKeywords(symbol_table)
    if soloKeywords != True:
        return soloKeywords

    operationsLine = checkOperationsLine(line_table_without_groupings)
    if operationsLine != True:
        return operationsLine

    orderOfConditionalsIfElse = checkOrderOfConditionalsIfElse(line_table_without_groupings)
    if orderOfConditionalsIfElse != True:
        return orderOfConditionalsIfElse

    orderOfConditionalsSwitchCase = checkOrderOfConditionalsSwitchCase(line_table_without_groupings)
    if orderOfConditionalsSwitchCase != True:
        return orderOfConditionalsSwitchCase

    current_line_no = 0

    for line in symbol_table:
        temp = copy.deepcopy(line)

        if len(line) != 0:

            #deals w output (visible)
            idx = 0
            if line[0] == "VISIBLE":
                while True:
                    if line[idx] in arithmetic_keywords:
                        for i in range(idx+1, len(line_table_without_groupings[current_line_no])):
                            current_keyword = line_table_without_groupings[current_line_no][i]
                            # checks if only arithmetic expressions/ints/floats follow
                            if (current_keyword in arithmetic_keywords or re.match(r"\-{0,1}[0-9]{1,}$",current_keyword) or re.match(r"\-{0,1}[0-9]{1,}\.[0-9]{1,}$", current_keyword)):
                                continue
                            else:
                                #checks if is is a variable name or if it is a reserved keyword
                                if current_keyword in all_keywords and current_keyword != "AN" and current_keyword != "IT":
                                    return "ERROR: Syntax error, attempted to evaluate an arithmetic expression with incorrect keyword/data type at line "+ str(symbol_table.index(line)+1)
                        Arithmetic(line)
                    elif line[idx] in comparison_keywords:
                        Comparison(line)
                    elif line[idx] in boolean_keywords:
                        Boolean(line)
                    idx += 1
                    if idx == len(line):
                        break 
                
                if line[1] in arithmetic_keywords:
                    for i in range(2, len(line_table_without_groupings[current_line_no])):
                        current_keyword = line_table_without_groupings[current_line_no][i]
                        # checks if only arithmetic expressions/ints/floats follow
                        if (current_keyword in arithmetic_keywords or re.match(r"\-{0,1}[0-9]{1,}$",current_keyword) or re.match(r"\-{0,1}[0-9]{1,}\.[0-9]{1,}$", current_keyword)):
                            continue
                        else:
                            #checks if is is a variable name or if it is a reserved keyword
                            if current_keyword in all_keywords and current_keyword != "AN" and current_keyword != "IT":
                                return "ERROR: Syntax error, attempted to evaluate an arithmetic expression with incorrect keyword/data type at line "+ str(symbol_table.index(line)+1)
                    Arithmetic(line)
                elif line[1] in comparison_keywords:
                    Comparison(line)
                elif line[1] in boolean_keywords:
                    Boolean(line)

            #deals with infinite expressions
            if (line[0] == "ALL OF" or line[0] == "ANY OF") and line[len(line)-1] == "MKAY":
                #check first if there is MKAY in mid
                mkayCount = 0
                for element in line:
                    if element == "MKAY":
                        mkayCount += 1
                if mkayCount > 1:
                    #ERROR: The line ends with MKAY but contains another MKAY in the middle
                    print("ERROR: Syntax error, expected 1 MKAY in line "+ str(symbol_table.index(line)) +" but found 2")
                    return "ERROR: Syntax error, expected 1 MKAY in line "+ str(symbol_table.index(line)+1) +" but found 2"

                for element in line:
                    if element in boolean_keywords or element in unary_keywords:
                        Boolean(line)
                lineIndex = symbol_table.index(line)
                symbol_table[lineIndex] = [symbol_table[lineIndex]]
            elif (line[0] == "ALL OF" or line[0] == "ANY OF") and line[-1] != "MKAY":
                #ERROR: There should be an MKAY at the end of the line
                # print("ERROR: Syntax error, expected MKAY at the end of line "+ str(symbol_table.index(line)))
                return "ERROR: Syntax error, expected MKAY at the end of line "+ str(symbol_table.index(line)+1)

            #deals w variable initialization
            if line[0] == "I HAS A":

                new_variable = [None,None,None,None]
                new_variable[0] = line[1]

                # if I HAS A <var Ident> ITZ <expression>
                # group the <expression> first to reduce length of line to 4 with the last element as the value
                if len(line) > 4:
                    if line[3] in arithmetic_keywords:
                        Arithmetic(line)
                        
                    elif line[3] in comparison_keywords:
                        Comparison(line)

                    elif line[3] in boolean_keywords or line[3] in unary_keywords:
                        Boolean(line)

                # if I HAS A <var Ident>
                # initialize the variable type into NOOB
                if len(line) == 2:
                    new_variable[1] = "NOOB"

                # if I HAS A <var Ident> ITZ <value>
                if len(line) == 4:
                    #
                    new_variable[2] = line[3]
                    
                    if isinstance(new_variable[2], list):
                        if new_variable[2][0] in arithmetic_keywords:
                            floatflag = 0
                            for items in temp:
                                if checkFloat(items):
                                    floatflag = 1
                                    break
                            if floatflag == 1:
                                new_variable[1] = 'NUMBAR'
                            else:
                                new_variable[1] = "NUMBR"

                        elif new_variable[2][0] in comparison_keywords or new_variable[2][0] in boolean_keywords or new_variable[2][0] in unary_keywords:
                            new_variable[1] = "TROOF"


                    for element in lexemes_table:
                        #print(element.lexeme)
                        if element.lexeme == new_variable[2]:
                            #print("pumasok naman")
                            # string example "YARN LITERAL"
                            store_list = element.type.split()
                            # get only YARN
                            new_variable[1] = store_list[0]
                            break

                legit_symbol_table.append(new_variable)

            #deals w assignment statements
            if len(line) > 1:
                #print("pumasok dito")
                #print(line)
                if line[1] == "R":
                    for idx in range(len(legit_symbol_table)):
                        if legit_symbol_table[idx][0] == line[0]:
                            tableindex = idx
                            break

                    if len(line) > 3:
                        if line[2] in arithmetic_keywords:
                            for i in range(3, len(line_table_without_groupings[current_line_no])):
                                current_keyword = line_table_without_groupings[current_line_no][i]
                                # checks if only arithmetic expressions/ints/floats follow
                                if (current_keyword in arithmetic_keywords or re.match(r"\-{0,1}[0-9]{1,}$",current_keyword) or re.match(r"\-{0,1}[0-9]{1,}\.[0-9]{1,}$", current_keyword)):
                                    continue
                                else:
                                    #checks if is is a variable name or if it is a reserved keyword
                                    if current_keyword in all_keywords and current_keyword != "AN" and current_keyword != "IT":
                                        return "ERROR: Syntax error, attempted to evaluate an arithmetic expression with incorrect keyword/data type at line "+ str(symbol_table.index(line)+1)
                            Arithmetic(line)
                        elif line[2] in comparison_keywords:
                            Comparison(line)
                        elif line[2] in boolean_keywords or line[2] in unary_keywords:
                            Boolean(line)


                    if len(line) == 3:
                        legit_symbol_table[tableindex][2] = line[2]
                        if isinstance(legit_symbol_table[tableindex][2], list):
                            if line[2][0] in arithmetic_keywords:
                                floatflag = 0
                                for items in temp:
                                    if checkFloat(items):
                                        # may float
                                        floatflag = 1
                                if floatflag == 1:
                                    legit_symbol_table[tableindex][1] = 'NUMBAR'
                                else:
                                    legit_symbol_table[tableindex][1] = "NUMBR"

                            elif line[2][0] in comparison_keywords or line[2][0] in boolean_keywords or line[2][0] in unary_keywords:
                                legit_symbol_table[tableindex][1] = "TROOF"
                        elif line[0] == "IT":
                            for elem in legit_symbol_table:
                                if elem[0] == "IT":
                                    elem[2] = line[2]
                                    if checkInt(elem[2]):
                                        elem[1] = "NUMBR"
                                    elif checkFloat(elem[2]):
                                        elem[1] = "NUMBAR"
                                    elif checkBoolean(elem[2]):
                                        elem[1] = "TROOF"
                                    else:
                                        elem[1] = "YARN"

                        for element in lexemes_table:
                            if element.lexeme == legit_symbol_table[tableindex][2]:
                                #string example "YARN LITERAL"
                                store_list = element.type.split()
                                #get only YARN
                                legit_symbol_table[tableindex][1] = store_list[0]


            #deals w if-else
            if line[0] == "OIC" and orly_flag == True:
                nowai_flag = False
                orly_flag = False
            if orly_flag == False:
                if line[0] == "O RLY?":
                    orly_flag = True
            else:
                # look for ya rly and no wai
                if line[0] == "YA RLY":
                    yarly_flag = True
                if line[0] == "NO WAI":
                    yarly_flag = False
                    nowai_flag = True
                if yarly_flag == True:
                    #continue hanggang sa makakita ng no wai
                    if line[0] in arithmetic_keywords:
                        for i in range(1, len(line_table_without_groupings[current_line_no])):
                            current_keyword = line_table_without_groupings[current_line_no][i]
                            # checks if only arithmetic expressions/ints/floats follow
                            if (current_keyword in arithmetic_keywords or re.match(r"\-{0,1}[0-9]{1,}$",current_keyword) or re.match(r"\-{0,1}[0-9]{1,}\.[0-9]{1,}$", current_keyword)):
                                continue
                            else:
                                #checks if is is a variable name or if it is a reserved keyword
                                if current_keyword in all_keywords and current_keyword != "AN" and current_keyword != "IT":
                                    return "ERROR: Syntax error, attempted to evaluate an arithmetic expression with incorrect keyword/data type at line "+ str(symbol_table.index(line)+1)
                        Arithmetic(line)
                        #print(line)
                    if line[0] in comparison_keywords:
                        Comparison(line)
                        #print(line)
                    if line[0] in boolean_keywords or line[0] in unary_keywords:
                        Boolean(line)
                        #print(line)
                if nowai_flag == True:
                    if line[0] in arithmetic_keywords:
                        for i in range(1, len(line_table_without_groupings[current_line_no])):
                            current_keyword = line_table_without_groupings[current_line_no][i]
                            # checks if only arithmetic expressions/ints/floats follow
                            if (current_keyword in arithmetic_keywords or re.match(r"\-{0,1}[0-9]{1,}$",current_keyword) or re.match(r"\-{0,1}[0-9]{1,}\.[0-9]{1,}$", current_keyword)):
                                continue
                            else:
                                #checks if is is a variable name or if it is a reserved keyword
                                if current_keyword in all_keywords and current_keyword != "AN" and current_keyword != "IT":
                                    return "ERROR: Syntax error, attempted to evaluate an arithmetic expression with incorrect keyword/data type at line "+ str(symbol_table.index(line)+1)
                        Arithmetic(line)
                        #print(line)
                    if line[0] in comparison_keywords:
                        Comparison(line)
                        #print(line)
                    if line[0] in boolean_keywords or line[0] in unary_keywords:
                        Boolean(line)
                       #print(line)

            #deals w switch-case
            if line[0] == "OIC" and wtf_flag == True and omg_flag == True:
                omg_flag = False
                wtf_flag = False
                # print("switch case ended w/ omg")
            
            if line[0] == "OIC" and wtf_flag == True and omgwtf_flag == True:
                omgwtf_flag = False
                wtf_flag = False
                # print("switch case ended w/ omgwtf")
            
            if wtf_flag == False:
                #checks if there is wtf
                if line[0] == "WTF?":
                    wtf_flag = True
            else:
                #look for omgs
                if line[0] == "OMG":
                    # print("omg spotted")
                    omg_flag = True
                if omg_flag == True:
                    if line[0] in arithmetic_keywords:
                        for i in range(1, len(line_table_without_groupings[current_line_no])):
                            current_keyword = line_table_without_groupings[current_line_no][i]
                            # checks if only arithmetic expressions/ints/floats follow
                            if (current_keyword in arithmetic_keywords or re.match(r"\-{0,1}[0-9]{1,}$",current_keyword) or re.match(r"\-{0,1}[0-9]{1,}\.[0-9]{1,}$", current_keyword)):
                                continue
                            else:
                                #checks if is is a variable name or if it is a reserved keyword
                                if current_keyword in all_keywords and current_keyword != "AN" and current_keyword != "IT":
                                    return "ERROR: Syntax error, attempted to evaluate an arithmetic expression with incorrect keyword/data type at line "+ str(symbol_table.index(line)+1)
                        Arithmetic(line)
                        #print(line)
                    if line[0] in comparison_keywords:
                        Comparison(line)
                        #print(line)
                    if line[0] in boolean_keywords or line[0] in unary_keywords:
                        Boolean(line)
                        #print(line)
                    if line[0] == "GTFO":
                        # print("omg ended")
                        # omgwtf_flag = False
                        # wtf_flag = False
                        omg_flag = False
                if line[0] == "OMGWTF":
                    # print("default case")
                    if line[0] in arithmetic_keywords:
                        for i in range(1, len(line_table_without_groupings[current_line_no])):
                            current_keyword = line_table_without_groupings[current_line_no][i]
                            # checks if only arithmetic expressions/ints/floats follow
                            if (current_keyword in arithmetic_keywords or re.match(r"\-{0,1}[0-9]{1,}$",current_keyword) or re.match(r"\-{0,1}[0-9]{1,}\.[0-9]{1,}$", current_keyword)):
                                continue
                            else:
                                #checks if is is a variable name or if it is a reserved keyword
                                if current_keyword in all_keywords and current_keyword != "AN" and current_keyword != "IT":
                                    return "ERROR: Syntax error, attempted to evaluate an arithmetic expression with incorrect keyword/data type at line "+ str(symbol_table.index(line)+1)
                        Arithmetic(line)
                        #print(line)
                    if line[0] in comparison_keywords:
                        Comparison(line)
                        #print(line)
                    if line[0] in boolean_keywords or line[0] in unary_keywords:
                        Boolean(line)
                        #print(line)

            #deals w arithmetic
            if line[0] in arithmetic_keywords:
                for i in range(1, len(line_table_without_groupings[current_line_no])):
                    current_keyword = line_table_without_groupings[current_line_no][i]
                    # checks if only arithmetic expressions/ints/floats follow
                    if (current_keyword in arithmetic_keywords or re.match(r"\-{0,1}[0-9]{1,}$",current_keyword) or re.match(r"\-{0,1}[0-9]{1,}\.[0-9]{1,}$", current_keyword)):
                        continue
                    else:
                        #checks if is is a variable name or if it is a reserved keyword
                        if current_keyword in all_keywords and current_keyword != "AN" and current_keyword != "IT":
                            return "ERROR: Syntax error, attempted to evaluate an arithmetic expression with incorrect keyword/data type at line "+ str(symbol_table.index(line)+1)
                Arithmetic(line)

            #deals w comparison
            if line[0] in comparison_keywords:
                Comparison(line)
                #print(line)
            
            #deals w boolean
            if line[0] in boolean_keywords or line[0] in unary_keywords:
                Boolean(line)
                #print(line)

        current_line_no += 1

    #for updating of symbol/lexeme table using operator lists above
    for element in lexemes_table:
        if element.lexeme == "AN":
            element.type = "Operand Separator"
        elif element.lexeme in arithmetic_keywords:
            element.type = "Arithmetic Operator"
        elif element.lexeme in comparison_keywords:
            element.type = "Comparison Operator"
        elif element.lexeme in boolean_keywords or element.lexeme in unary_keywords:
            element.type = "Boolean Operator"
        elif element.lexeme in infinite_keywords:
            element.type = "Infinite Arity Keywords"

    
    #UNCOMMENT TO CHECK THE FINAL lexemes_table AND THE symbol_table (code per line)
    '''for i in range(len(lexemes_table)):
      print([lexemes_table[i].lexeme, lexemes_table[i].type])

    print()

    for elem in symbol_table:
        print(elem)
        
    print()

    for item in legit_symbol_table:
        print(item)'''

    return symbol_table, lexemes_table, legit_symbol_table,line_table_without_groupings

def checkInt(string):
    if re.match(r"^-{0,1}[0-9]{1,}$", string):
        return True
    return False
    
def checkFloat(string):
    if re.match(r"^-{0,1}[0-9]{1,}\.{1}[0-9]{1,}$", string):
        return True
    return False

def checkVar(string):
    if re.match(r"[a-zA-Z]{1}[a-zA-Z0-9_]*", string):
        return True
    return False

def checkBoolean(string):
    if string == "WIN" or string == "FAIL":
        return True
    return False

def Arithmetic(line):
    arithmetic_counter = 0
    for j in range(0, len(line)):
        if line[j] in arithmetic_keywords:
            arithmetic_counter += 1
    while arithmetic_counter > 0:
        for j in range(0, len(line)):
            if line[j] == "AN":
                if isinstance(line[j-1], str) and isinstance(line[j+1], str):
                    if line[j-1] in arithmetic_keywords and line[j+1] in arithmetic_keywords:
                        continue
                    elif line[j-1] not in arithmetic_keywords and line[j+1] in arithmetic_keywords:
                        continue
                    elif line[j-1] in arithmetic_keywords and line[j+1] not in arithmetic_keywords:
                        continue
                    elif line[j-1] not in arithmetic_keywords and line[j+1] not in arithmetic_keywords:
                        if (checkInt(line[j-1]) or checkFloat(line[j-1]) or checkVar(line[j-1])) and (checkInt(line[j+1]) or checkFloat(line[j+1]) or checkVar(line[j+1])):
                            arithmetic_counter -= 1
                            new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                            line[j-2] = new_grouping
                            line.pop(j-1)
                            line.pop(j-1)
                            line.pop(j-1)
                            break
                        else:
                            print("Invalid formats!")
                elif isinstance(line[j-1], list) and isinstance(line[j+1], str):
                    if line[j+1] in arithmetic_keywords:
                        continue
                    else:
                        arithmetic_counter -= 1
                        new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                        line[j-2] = new_grouping
                        line.pop(j-1)
                        line.pop(j-1)
                        line.pop(j-1)
                        break
                elif isinstance(line[j-1], str) and isinstance(line[j+1], list):
                    if line[j-1] in arithmetic_keywords:
                        continue
                    else:
                        arithmetic_counter -= 1
                        new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                        line[j-2] = new_grouping
                        line.pop(j-1)
                        line.pop(j-1)
                        line.pop(j-1)
                        break                                    
                elif isinstance(line[j-1], list) and isinstance(line[j+1], list):
                    arithmetic_counter -= 1
                    new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                    line[j-2] = new_grouping
                    line.pop(j-1)
                    line.pop(j-1)
                    line.pop(j-1)
                    break

def Comparison(line):
    comparison_counter = 0
    for j in range(0, len(line)):
        if line[j] in comparison_keywords or line[j] in arithmetic_keywords:
            comparison_counter += 1
    while comparison_counter > 0:
        for j in range(0, len(line)):
            if line[j] == "AN":
                if isinstance(line[j-1], str) and isinstance(line[j+1], str):

                    if (line[j-1] in comparison_keywords or line[j-1] in arithmetic_keywords) and (line[j+1] in comparison_keywords or line[j+1] in arithmetic_keywords):
                        continue
                    elif (line[j-1] not in comparison_keywords or line[j-1] not in arithmetic_keywords) and (line[j+1] in comparison_keywords or line[j+1] in arithmetic_keywords):
                        continue
                    elif (line[j-1] in comparison_keywords or line[j-1] in arithmetic_keywords) and (line[j+1] not in comparison_keywords or line[j+1] not in arithmetic_keywords):
                        continue

                    elif (line[j-1] not in comparison_keywords or line[j-1] not in arithmetic_keywords) and (line[j+1] not in comparison_keywords or line[j+1] not in arithmetic_keywords):

                        if (checkInt(line[j - 1]) or checkFloat(line[j - 1]) or checkVar(line[j - 1])) and (
                                checkInt(line[j + 1]) or checkFloat(line[j + 1]) or checkVar(line[j + 1])):

                            comparison_counter -= 1
                            new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                            line[j-2] = new_grouping
                            line.pop(j-1)
                            line.pop(j-1)
                            line.pop(j-1)
                            break
                        else:
                            comparison_counter -= 1
                            break

                elif isinstance(line[j-1], list) and isinstance(line[j+1], str):
                    if line[j+1] in comparison_keywords or line[j+1] in arithmetic_keywords:
                        continue
                    else:
                        comparison_counter -= 1
                        new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                        line[j-2] = new_grouping
                        line.pop(j-1)
                        line.pop(j-1)
                        line.pop(j-1)
                        break

                elif isinstance(line[j-1], str) and isinstance(line[j+1], list):
                    if line[j-1] in comparison_keywords or line[j-1] in arithmetic_keywords:
                        continue
                    else:
                        comparison_counter -= 1
                        new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                        line[j-2] = new_grouping
                        line.pop(j-1)
                        line.pop(j-1)
                        line.pop(j-1)
                        break                                    

                elif isinstance(line[j-1], list) and isinstance(line[j+1], list):
                    comparison_counter -= 1
                    new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                    line[j-2] = new_grouping
                    line.pop(j-1)
                    line.pop(j-1)
                    line.pop(j-1)
                    break

def Boolean(line):
    boolean_counter = 0
    not_counter = 0
    for j in range(0, len(line)):
        if line[j] in unary_keywords:
            not_counter += 1
    while not_counter > 0:
        for j in range(0, len(line)):
            if line[j] in unary_keywords:
                not_counter -= 1
                new_grouping = [line[j],line[j+1]]
                line[j] = new_grouping
                line.pop(j+1)
                break
    for j in range(0, len(line)):
        if line[j] in boolean_keywords:
            boolean_counter += 1
    while boolean_counter > 0:
        for j in range(0, len(line)):
            if line[j] == "AN":
                if isinstance(line[j-1], str) and isinstance(line[j+1], str):
                    if line[j-1] in boolean_keywords and line[j+1] in boolean_keywords:
                        continue
                    elif line[j-1] not in boolean_keywords and line[j+1] in boolean_keywords:
                        continue
                    elif line[j-1] in boolean_keywords and line[j+1] not in boolean_keywords:
                        continue
                    elif line[j-1] not in boolean_keywords and line[j+1] not in boolean_keywords:
                        if line[j-2] in boolean_keywords:
                            if (checkBoolean(line[j-1]) or checkVar(line[j-1])) and (checkBoolean(line[j+1]) or checkVar(line[j+1])):
                                boolean_counter -= 1
                                new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                                line[j-2] = new_grouping
                                line.pop(j-1)
                                line.pop(j-1)
                                line.pop(j-1)
                                break
                elif isinstance(line[j-1], list) and isinstance(line[j+1], str):
                    if line[j+1] in boolean_keywords or line[j-2] not in boolean_keywords:
                        continue
                    else:
                        boolean_counter -= 1
                        new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                        line[j-2] = new_grouping
                        line.pop(j-1)
                        line.pop(j-1)
                        line.pop(j-1)
                        break
                elif isinstance(line[j-1], str) and isinstance(line[j+1], list):
                    if line[j-1] in boolean_keywords or line[j-2] not in boolean_keywords:
                        continue
                    else:
                        boolean_counter -= 1
                        new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                        line[j-2] = new_grouping
                        line.pop(j-1)
                        line.pop(j-1)
                        line.pop(j-1)
                        break                                    
                elif isinstance(line[j-1], list) and isinstance(line[j+1], list):
                    if line[j-2] not in boolean_keywords:
                        continue
                    else:
                        boolean_counter -= 1
                        new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                        line[j-2] = new_grouping
                        line.pop(j-1)
                        line.pop(j-1)
                        line.pop(j-1)
                        break
        
def checkCodeDelimiter(symbol_table):
    code_delimiters_pairs = [['HAI', 'KTHXBYE'], ['O RLY?', 'OIC', 'WTF?'], ['WTF?', 'OIC', 'O RLY?']]
    for pair in code_delimiters_pairs:
        startPresent = False
        startIndex = None
        for line in symbol_table:
            if line != []:
                if line[0] == pair[0] and not startPresent:     #may nakitang start
                    startPresent = True
                    startIndex = symbol_table.index(line) +1
                elif line[0] == pair[1] and startPresent:       #niclose yung start
                    startPresent = False
                elif code_delimiters_pairs.index(pair) == 0 and line[0] == pair[0] and startPresent:       #may start na ulet kahit di pa naend yung taas (FOR HAI ONLI)
                    #ERROR: Started a new block without closing the prior block
                    print("ERROR: Syntax error, expected a closing keyword for the "+ pair[0] +" block at line "+ str(startIndex))
                    return "ERROR: Syntax error, expected a closing keyword for the "+ pair[0] +" block at line "+ str(startIndex)
                elif line[0] == pair[1] and startPresent:   #may end pero walang start      
                    #ERROR: No start function for block but a block is supposedly closed 
                    print("ERROR: Syntax error, unexpected character in line "+str(symbol_table.index(line)+1))
                    return "ERROR: Syntax error, unexpected character in line "+str(symbol_table.index(line)+1)

        if code_delimiters_pairs.index(pair) == 0 and startPresent:        #may start pero never naclose HAI onli
            #ERROR: Block was never closed
            print("ERROR: Syntax error, expected a closing keyword for the "+ pair[0] +" block in line "+ str(startIndex))
            return "ERROR: Syntax error, expected a closing keyword for the "+ pair[0] +" block in line "+ str(startIndex)
        if code_delimiters_pairs.index(pair) == 0 and not startPresent and startIndex == None:
            #ERROR: Syntax error, both beginning and ending delimiters are missing for HAI onli
            print("ERROR: Syntax error, start and end code delimiters missing")
            return "ERROR: Syntax error, start and end code delimiters missing"
        
    return True

def checkSoloKeywords(symbol_table):
    solo_in_line_keywords_list = ['HAI', 'KTHXBYE', 'O RLY?', 'YA RLY', 'NO WAI', 'MEBBE', 'WTF?', 'OMGWTF', 'GTFO', 'OIC']
    for line in symbol_table:
        if line != [] and line[0] in solo_in_line_keywords_list and len(line) != 1:
            #ERROR: Unexpected word after a keyword
            print("ERROR: Syntax error, unexpected character after keyword "+ str(line[0]) +" in line "+ str(symbol_table.index(line)+1))
            return "ERROR: Syntax error, unexpected character after keyword "+ str(line[0]) +" in line "+ str(symbol_table.index(line)+1)
        if line != [] and line[0] == 'OMG':
            if len(line) < 2:
                #ERROR: Missing operand for OMG
                print("ERROR: Syntax error, missing operand after OMG keyword in line "+str(symbol_table.index(line)+1))
                return "ERROR: Syntax error, missing operand after OMG keyword in line "+str(symbol_table.index(line)+1)
            elif len(line) > 2:
                #ERROR:Excess character after OMG
                print("ERROR: Syntax error, excess character after OMG keyword in line "+str(symbol_table.index(line)+1))
                return "ERROR: Syntax error, excess character after OMG keyword in line "+str(symbol_table.index(line)+1)
            elif len(line) == 2:
                if not (checkFloat(str(line[1])) or checkInt(str(line[1])) or checkBoolean(str(line[1])) or re.match(r"^\".*\"$", line[1])):
                    #ERROR: invalid type of operand, must be literal
                    print("ERROR: Syntax error, operand after OMG keyword in line "+str(symbol_table.index(line)+1)+" must be a literal")
                    return "ERROR: Syntax error, operand after OMG keyword in line "+str(symbol_table.index(line)+1)+" must be a literal"
    return True
    
def checkOperationsLine(line_table_without_groupings):
    binary_operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF', 'BOTH SAEM', 'DIFFRINT', 'BOTH OF', 'EITHER OF', 'WON OF']
    infinite_operators = ['ALL OF', 'ANY OF']

    for line in line_table_without_groupings:
        # if I HAS A <var> ITZ <expression>
        if len(line) > 4 and line[0] == 'I HAS A' and line[2] == 'ITZ':
            temp = copy.deepcopy(line)
            for i in range(3):
                temp.pop(0)

            #lahat ng NOT dapat may kasunod na literal or var
            for j in range(len(temp)):
                if j > 0 and (temp[j-1] == 'NOT' and not checkBoolean(temp[j])):
                    #ERROR: invalid operand
                    print("ERROR: Syntax error, invalid operand after the keyword NOT in line " +str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, invalid operand after the keyword NOT in line " +str(line_table_without_groupings.index(line)+1)
                elif j > 0 and temp[len(temp)-1] == 'NOT':
                    #ERROR: Missing operand
                    print("ERROR: Syntax error, missing operand after the keyword NOT in line "+ str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand after the keyword NOT in line "+ str(line_table_without_groupings.index(line)+1)

            #removes all NOT
            for element in temp:
                if element == 'NOT':
                    temp.pop(temp.index(element))

            for i in range(len(temp)):
                #bawal magkasunod na AN
                if i > 0 and (temp[i] == 'AN' and temp[i-1] == 'AN'):
                    #ERROR: Missing operand or misplace separator
                    print("ERROR: Syntax error, missing operand or misplaced separator in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand or misplaced separator in line "+str(line_table_without_groupings.index(line)+1)
                #bawal magkatabi operand
                if i > 0 and ((temp[i] != 'AN' and temp[i] != 'MKAY' and temp[i] != 'NOT' and temp[i] not in binary_operators and temp[i] not in infinite_operators) and (temp[i-1] != 'AN' and temp[i-1] != 'MKAY' and temp[i-1] != 'NOT' and temp[i-1] not in binary_operators and temp[i-1] not in infinite_operators)):
                    #ERROR: Syntax error, missing separator
                    print("ERROR: Syntax error, missing operand separator in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand separator in line "+str(line_table_without_groupings.index(line)+1)
                #bawal nasa gitna ng 2 operator yung operand
                if i != 0 and i != len(temp)-1:
                    if (temp[i-1] in binary_operators and temp[i-1] in infinite_operators) and (temp[i] not in binary_operators and temp[i] not in infinite_operators and temp[i] != 'AN' and temp[i] != 'MKAY' and temp[i] != 'NOT') and (temp[i+1] in binary_operators or temp[i+1] in infinite_operators):
                        #ERROR: Syntax error, missing separator
                        print("ERROR: Syntax error, missing separator in line "+str(line_table_without_groupings.index(line)+1))
                        return "ERROR: Syntax error, missing separator in line "+str(line_table_without_groupings.index(line)+1)
                #bawal <operator> AN
                if i > 0 and temp[i] == 'AN' and (temp[i-1] in binary_operators or temp[i-1] in infinite_operators):
                    #ERROR: Syntax error, missing operand
                    print("ERROR: Syntax error, missing operand in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand in line "+str(line_table_without_groupings.index(line)+1)

            if temp[0] in binary_operators:
                #number of ops must be equal to number of ANs
                ops_count = 0
                an_count = 0
                for elem in temp:
                    if elem in binary_operators:
                        ops_count += 1
                    if elem == 'AN':
                        an_count += 1
                    if elem in infinite_operators:
                        #ERROR: Infinite cannot be nested inside other ops
                        print("ERROR: Syntax error, infinite operators cannot be nested in line "+str(line_table_without_groupings.index(line)+1))
                        return "ERROR: Syntax error, infinite operators cannot be nested in line "+str(line_table_without_groupings.index(line)+1)

                if ops_count != an_count:
                    #ERROR: Syntax error, operator count does not match with separator count
                    print("ERROR: Syntax error, operator count does not match separator count in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, operator count does not match separator count in line "+str(line_table_without_groupings.index(line)+1)
                    
                #dapat laging AN <operand> yung dulo
                if temp[-2] != 'AN' or temp[-1] == 'AN' or temp[-1] in binary_operators:
                    #ERROR: Syntax error, invalid format of operation
                    print("ERROR: Syntax error, invalid format of operation in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, invalid format of operation in line "+str(line_table_without_groupings.index(line)+1)

            if temp[0] in infinite_operators:
                temp2 = copy.deepcopy(temp)

                binary_ops_count = 0
                an_count = 0
                operands_count = 0
    
                #remove mkay first and infi
                if temp2[-1] == 'MKAY':
                    temp2.pop(-1)
                if temp2[0] in infinite_operators:
                    temp2.pop(0)
                
                #remove all not
                not_index_list = []
                for i in range(len(temp)):
                    if temp2[i] == 'NOT':
                        not_index_list.append(i)
                not_index_list.reverse()
                for notIndex in not_index_list:
                    temp2.pop(notIndex)
                
                #convert nested binary operations into a single operand
                for i in range(len(temp2)):
                    if temp2[i] in infinite_operators:
                        #ERROR: Infinite keywords must not be nested in infinite ops
                        print("ERROR: Syntax error, infinite operations must not be nested inside infinite operations, line "+str(line_table_without_groupings.index(temp)+1))
                        return "ERROR: Syntax error, infinite operations must not be nested inside infinite operations, line "+str(line_table_without_groupings.index(temp)+1)
                    if temp2[i] in binary_operators:
                        binary_ops_count += 1
                #remove binary ops
                for elem in temp2:
                    if elem in binary_operators:
                        temp2.pop(temp2.index(elem))
                #remove 2 ANs and 2 operands
                for i in range(binary_ops_count):
                    for element in temp2:
                        if element == 'AN':
                            temp2.pop(temp2.index(element))
                            break
                    for element2 in temp2:
                        if element2 not in binary_operators and element2 not in infinite_keywords and element2 != 'AN':
                            temp2.pop(temp2.index(element2))
                            break
                
                # count the number of ANs and operands
                for item in temp2:
                    if item == 'AN':
                        an_count += 1
                    else:
                        operands_count += 1
                
                # FOR INFI TO BE VALID: NUMBER OF OPERANDS = NUMBER OF ANs + 1
                if operands_count != an_count + 1:
                    #ERROR: invalid format of infinite operation
                    print("ERROR: Syntax error, invalid format of infinite operation in line "+ str(line_table_without_groupings.index(temp)+1))
                    return "ERROR: Syntax error, invalid format of infinite operation in line "+ str(line_table_without_groupings.index(temp)+1)

        # if <expression>
        if line != [] and (line[0] in binary_operators or line[0] in infinite_operators):
            temp = copy.deepcopy(line)

            #lahat ng NOT dapat may kasunod na literal or var
            for j in range(len(line)):
                if j > 0 and (line[j-1] == 'NOT' and not checkBoolean(line[j])):
                    #ERROR: invalid operand
                    print("ERROR: Syntax error, invalid operand after the keyword NOT in line " +str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, invalid operand after the keyword NOT in line " +str(line_table_without_groupings.index(line)+1)
                elif j > 0 and line[len(line)-1] == 'NOT':
                    #ERROR: Missing operand
                    print("ERROR: Syntax error, missing operand after the keyword NOT in line "+ str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand after the keyword NOT in line "+ str(line_table_without_groupings.index(line)+1)

            #removes all NOT
            for element in line:
                if element == 'NOT':
                    line.pop(line.index(element))

            for i in range(len(line)):
                #bawal magkasunod na AN
                if i > 0 and (line[i] == 'AN' and line[i-1] == 'AN'):
                    #ERROR: Missing operand or misplace separator
                    print("ERROR: Syntax error, missing operand or misplaced separator in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand or misplaced separator in line "+str(line_table_without_groupings.index(line)+1)
                #bawal magkatabi operand
                if i > 0 and ((line[i] != 'AN' and line[i] != 'MKAY' and line[i] != 'NOT' and line[i] not in binary_operators and line[i] not in infinite_operators) and (line[i-1] != 'AN' and line[i-1] != 'MKAY' and line[i-1] != 'NOT' and line[i-1] not in binary_operators and line[i-1] not in infinite_operators)):
                    #ERROR: Syntax error, missing separator
                    print("ERROR: Syntax error, missing operand separator in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand separator in line "+str(line_table_without_groupings.index(line)+1)
                #bawal nasa gitna ng 2 operator yung operand
                if i != 0 and i != len(line)-1:
                    if (line[i-1] in binary_operators or line[i-1] in infinite_operators) and (line[i] not in binary_operators and line[i] not in infinite_operators and line[i] != 'AN'  and line[i] != 'MKAY' and line[i-1] != 'NOT') and (line[i+1] in binary_operators or line[i+1] in infinite_operators):
                        #ERROR: Syntax error, missing separator
                        print("ERROR: Syntax error, missing separator in line "+str(line_table_without_groupings.index(line)+1))
                        return "ERROR: Syntax error, missing separator in line "+str(line_table_without_groupings.index(line)+1)
                #bawal <operator> AN
                if i > 0 and line[i] == 'AN' and (line[i-1] in binary_operators or line[i-1] in infinite_operators):
                    #ERROR: Syntax error, missing operand
                    print("ERROR: Syntax error, missing operand in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand in line "+str(line_table_without_groupings.index(line)+1)

            if line[0] in binary_operators:
                #number of ops must be equal to number of ANs
                ops_count = 0
                an_count = 0
                for elem in line:
                    if elem in binary_operators:
                        ops_count += 1
                    if elem == 'AN':
                        an_count += 1
                    if elem in infinite_operators:
                        #ERROR: Infinite cannot be nested inside other ops
                        print("ERROR: Syntax error, infinite operators cannot be nested in line "+str(line_table_without_groupings.index(line)+1))
                        return "ERROR: Syntax error, infinite operators cannot be nested in line "+str(line_table_without_groupings.index(line)+1)
                    
                if ops_count != an_count:
                    #ERROR: Syntax error, operator count does not match with separator count
                    print("ERROR: Syntax error, operator count does not match separator count in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, operator count does not match separator count in line "+str(line_table_without_groupings.index(line)+1)
                    
                #dapat laging AN <operand> yung dulo
                if line[-2] != 'AN' or line[-1] == 'AN' or line[-1] in binary_operators:
                    #ERROR: Syntax error, invalid format of operation
                    print("ERROR: Syntax error, invalid format of operation in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, invalid format of operation in line "+str(line_table_without_groupings.index(line)+1)
                
            if line[0] in infinite_operators:
                temp = copy.deepcopy(line)

                binary_ops_count = 0
                an_count = 0
                operands_count = 0
    
                #remove mkay first and infi
                if temp[-1] == 'MKAY':
                    temp.pop(-1)
                if temp[0] in infinite_operators:
                    temp.pop(0)
                
                #remove all not
                not_index_list = []
                for i in range(len(temp)):
                    if temp[i] == 'NOT':
                        not_index_list.append(i)
                not_index_list.reverse()
                for notIndex in not_index_list:
                    temp.pop(notIndex)
                
                #convert nested binary operations into a single operand
                for i in range(len(temp)):
                    if temp[i] in infinite_operators:
                        #ERROR: Infinite keywords must not be nested in infinite ops
                        print("ERROR: Semantic error, infinite operations must not be nested inside infinite operations, line "+str(line_table_without_groupings.index(line)+1))
                        return "ERROR: Semantic error, infinite operations must not be nested inside infinite operations, line "+str(line_table_without_groupings.index(line)+1)
                    if temp[i] in binary_operators:
                        binary_ops_count += 1
                #remove binary ops
                for elem in temp:
                    if elem in binary_operators:
                        temp.pop(temp.index(elem))
                #remove 2 ANs and 2 operands
                for i in range(binary_ops_count):
                    for element in temp:
                        if element == 'AN':
                            temp.pop(temp.index(element))
                            break
                    for element2 in temp:
                        if element2 not in binary_operators and element2 not in infinite_keywords and element2 != 'AN':
                            temp.pop(temp.index(element2))
                            break
                
                # count the number of ANs and operands
                for item in temp:
                    if item == 'AN':
                        an_count += 1
                    else:
                        operands_count += 1
                
                # FOR INFI TO BE VALID: NUMBER OF OPERANDS = NUMBER OF ANs + 1
                if operands_count != an_count + 1:
                    #ERROR: invalid format of infinite operation
                    print("ERROR: Syntax error, invalid format of infinite operation in line "+ str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, invalid format of infinite operation in line "+ str(line_table_without_groupings.index(line)+1)

            line = temp 

        #if <var> R <expression>
        if len(line) > 3 and line[1] == 'R':
            temp = copy.deepcopy(line)
            for i in range(2):
                temp.pop(0)

            #lahat ng NOT dapat may kasunod na literal or var
            for j in range(len(temp)):
                if j > 0 and (temp[j-1] == 'NOT' and not checkBoolean(temp[j])):
                    #ERROR: invalid operand
                    print("ERROR: Syntax error, invalid operand after the keyword NOT in line " +str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, invalid operand after the keyword NOT in line " +str(line_table_without_groupings.index(line)+1)
                elif j > 0 and temp[len(temp)-1] == 'NOT':
                    #ERROR: Missing operand
                    print("ERROR: Syntax error, missing operand after the keyword NOT in line "+ str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand after the keyword NOT in line "+ str(line_table_without_groupings.index(line)+1)

            #removes all NOT
            for element in temp:
                if element == 'NOT':
                    temp.pop(temp.index(element))

            for i in range(len(temp)):
                #bawal magkasunod na AN
                if i > 0 and (temp[i] == 'AN' and temp[i-1] == 'AN'):
                    #ERROR: Missing operand or misplace separator
                    print("ERROR: Syntax error, missing operand or misplaced separator in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand or misplaced separator in line "+str(line_table_without_groupings.index(line)+1)
                #bawal magkatabi operand
                if i > 0 and ((temp[i] != 'AN' and temp[i] != 'MKAY' and temp[i] != 'NOT' and temp[i] not in binary_operators and temp[i] not in infinite_operators) and (temp[i-1] != 'AN' and temp[i-1] != 'MKAY' and temp[i-1] != 'NOT' and temp[i-1] not in binary_operators and temp[i-1] not in infinite_operators)):
                    #ERROR: Syntax error, missing separator
                    print("ERROR: Syntax error, missing operand separator in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand separator in line "+str(line_table_without_groupings.index(line)+1)
                #bawal nasa gitna ng 2 operator yung operand
                if i != 0 and i != len(temp)-1:
                    if (temp[i-1] in binary_operators or temp[i-1] in infinite_operators) and (temp[i] not in binary_operators and temp[i] not in infinite_operators and temp[i] != 'AN' and temp[i] != 'MKAY' and temp[i] != 'NOT') and (temp[i+1] in binary_operators or temp[i+1] in infinite_operators):
                        #ERROR: Syntax error, missing separator
                        print("ERROR: Syntax error, missing separator in line "+str(line_table_without_groupings.index(line)+1))
                        return "ERROR: Syntax error, missing separator in line "+str(line_table_without_groupings.index(line)+1)
                #bawal <operator> AN
                if i > 0 and temp[i] == 'AN' and (temp[i-1] in binary_operators or temp[i-1] in infinite_operators):
                    #ERROR: Syntax error, missing operand
                    print("ERROR: Syntax error, missing operand in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, missing operand in line "+str(line_table_without_groupings.index(line)+1)

            if temp[0] in binary_operators:
                #number of ops must be equal to number of ANs
                ops_count = 0
                an_count = 0
                for elem in temp:
                    if elem in binary_operators:
                        ops_count += 1
                    if elem == 'AN':
                        an_count += 1
                    if elem in infinite_operators:
                        #ERROR: Infinite cannot be nested inside other ops
                        print("ERROR: Syntax error, infinite operators cannot be nested in line "+str(line_table_without_groupings.index(line)+1))
                        return "ERROR: Syntax error, infinite operators cannot be nested in line "+str(line_table_without_groupings.index(line)+1)

                if ops_count != an_count:
                    #ERROR: Syntax error, operator count does not match with separator count
                    print("ERROR: Syntax error, operator count does not match separator count in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, operator count does not match separator count in line "+str(line_table_without_groupings.index(line)+1)
                    
                #dapat laging AN <operand> yung dulo
                if temp[-2] != 'AN' or temp[-1] == 'AN' or temp[-1] in binary_operators:
                    #ERROR: Syntax error, invalid format of operation
                    print("ERROR: Syntax error, invalid format of operation in line "+str(line_table_without_groupings.index(line)+1))
                    return "ERROR: Syntax error, invalid format of operation in line "+str(line_table_without_groupings.index(line)+1)

            if temp[0] in infinite_operators:
                temp2 = copy.deepcopy(temp)

                binary_ops_count = 0
                an_count = 0
                operands_count = 0
    
                #remove mkay first and infi
                if temp2[-1] == 'MKAY':
                    temp2.pop(-1)
                if temp2[0] in infinite_operators:
                    temp2.pop(0)
                
                #remove all not
                not_index_list = []
                for i in range(len(temp)):
                    if temp2[i] == 'NOT':
                        not_index_list.append(i)
                not_index_list.reverse()
                for notIndex in not_index_list:
                    temp2.pop(notIndex)
                
                #convert nested binary operations into a single operand
                for i in range(len(temp2)):
                    if temp2[i] in infinite_operators:
                        #ERROR: Infinite keywords must not be nested in infinite ops
                        print("ERROR: Semantic error, infinite operations must not be nested inside infinite operations, line "+str(line_table_without_groupings.index(temp)+1))
                        return "ERROR: Semantic error, infinite operations must not be nested inside infinite operations, line "+str(line_table_without_groupings.index(temp)+1)
                    if temp2[i] in binary_operators:
                        binary_ops_count += 1
                #remove binary ops
                for elem in temp2:
                    if elem in binary_operators:
                        temp2.pop(temp2.index(elem))
                #remove 2 ANs and 2 operands
                for i in range(binary_ops_count):
                    for element in temp2:
                        if element == 'AN':
                            temp2.pop(temp2.index(element))
                            break
                    for element2 in temp2:
                        if element2 not in binary_operators and element2 not in infinite_keywords and element2 != 'AN':
                            temp2.pop(temp2.index(element2))
                            break
                
                # count the number of ANs and operands
                for item in temp2:
                    if item == 'AN':
                        an_count += 1
                    else:
                        operands_count += 1
                
                # FOR INFI TO BE VALID: NUMBER OF OPERANDS = NUMBER OF ANs + 1
                if operands_count != an_count + 1:
                    #ERROR: invalid format of infinite operation
                    print("ERROR: Syntax error, invalid format of infinite operation in line "+ str(line_table_without_groupings.index(temp)+1))
                    return "ERROR: Syntax error, invalid format of infinite operation in line "+ str(line_table_without_groupings.index(temp)+1)

    return True

def checkOrderOfConditionalsIfElse(line_table_without_groupings):
    # IF-ELSE: Dapat tag iisa ng instance ng O RLY?, YA RLY, NO WAI, and OIC in right order
    orly_flag = False
    yarly_flag = False
    nowai_flag = False
    oic_flag = False
    
    orly_index = None
    yarly_index = None
    nowai_index = None
    oic_index = None

    orly_count = 0
    yarly_count = 0
    nowai_count = 0
    oic_count = 0

    #extra check
    wtf_count = 0
    omg_count = 0
    omgwtf_count = 0

    for i in range(len(line_table_without_groupings)):
        if line_table_without_groupings[i] == ['O RLY?']:
            orly_flag = True
            orly_index = i + 1
            orly_count += 1
            
            nextLine = i + 1
            while line_table_without_groupings[nextLine] == []:
                nextLine += 1

            if line_table_without_groupings[nextLine] != ['YA RLY']:
                #ERROR: O RLY? must be followed immediately by YA RLY
                print("ERROR: Syntax error, expected a YA RLY keyword right after O RLY? in line "+str(orly_index))
                return "ERROR: Syntax error, expected a YA RLY keyword right after O RLY? in line "+str(orly_index)
        if line_table_without_groupings[i] == ['YA RLY']:      
            yarly_flag = True
            yarly_index = i + 1
            yarly_count += 1
        if line_table_without_groupings[i] == ['NO WAI']:      
            nowai_flag = True
            nowai_index = i + 1
            nowai_count += 1
        if line_table_without_groupings[i] == ['OIC']:
            oic_flag = True
            oic_index = i + 1
            oic_count += 1

        if line_table_without_groupings[i] != []:
            if line_table_without_groupings[i] == ['WTF?']:
                wtf_count += 1
            if line_table_without_groupings[i][0] == 'OMG':     
                omg_count += 1
            if line_table_without_groupings[i] == ['OMGWTF']:     
                omgwtf_count += 1

        if orly_count == oic_count + 2:
            #ERROR: An O RLY? block was not closed
            print("ERROR: Syntax error, O RLY? block started in line "+str(orly_index)+" but previous O RLY? block was not closed")
            return "ERROR: Syntax error, O RLY? block started in line "+str(orly_index)+" but previous O RLY? block was not closed"
        if yarly_count > 1:
            #ERROR: Syntax error, expected 1 YA RLY for O RLY? block but found 2
            print("ERROR: Syntax error, expected 1 YA RLY keyword for O RLY? block in from line "+str(orly_index)+" but found 2")
            return "ERROR: Syntax error, expected 1 YA RLY keyword for O RLY? block in from line "+str(orly_index)+" but found 2"
        if nowai_count > 1:
            #ERROR: Syntax error, expected 1 NO WAI for O RLY? block but found 2
            print("ERROR: Syntax error, expected 1 NO WAI keyword for O RLY? block in from line "+str(orly_index)+" but found 2")
            return "ERROR: Syntax error, expected 1 NO WAI keyword for O RLY? block in from line "+str(orly_index)+" but found 2"
        if orly_flag and not yarly_flag and not nowai_flag and oic_flag:
            #ERROR: The O RLY? block ended but no YA RLY and NO WAI
            print("ERROR: Syntax error, expected a YA RLY keyword and a NO WAI keyword before line "+str(oic_index))
            return "ERROR: Syntax error, expected a YA RLY keyword and a NO WAI keyword before line "+str(oic_index)
        if yarly_flag and not orly_flag:        #may ya rly pero alang orly nani
            #ERROR: Expected a start delimiter for ya rly
            print("ERROR: Syntax error, expected an O RLY? start delimiter before YA RLY block in line "+str(yarly_index))
            return "ERROR: Syntax error, expected an O RLY? start delimiter before YA RLY block in line "+str(yarly_index) 
        if nowai_flag and not orly_flag and not yarly_flag:       #may no wai na pero ala pa orly
            #ERROR: Expected an O RLY? keyword before NO WAI
            print("ERROR: Syntax error, missing O RLY? start delimiter before NO WAI or misplaced keyword in line "+str(nowai_index))
            return "ERROR: Syntax error, missing O RLY? start delimiter before NO WAI or misplaced keyword in line "+str(nowai_index)
        if nowai_flag and not yarly_flag:       #may no wai na pero ala pa yarly
            #ERROR: Expected a YA RLY keyword before NO WAI
            print("ERROR: Syntax error, expected a YA RLY keyword before NO WAI in line "+str(nowai_index))
            return "ERROR: Syntax error, expected a YA RLY keyword before NO WAI in line "+str(nowai_index)
        if i == len(line_table_without_groupings)-1 and not oic_flag and orly_flag and yarly_flag and nowai_flag:
            #ERROR: O RLY? block complete but not closed
            print("ERROR: Syntax error, expected a closing keyword for O RLY? block from line "+str(orly_index))
            return "ERROR: Syntax error, expected a closing keyword for O RLY? block from line "+str(orly_index)
        if oic_flag and orly_flag and yarly_flag and not nowai_flag:
            #ERROR: Closed oic without entering a NO WAI keyword
            print("ERROR: Syntax error, expected NO WAI keyword before line "+ str(oic_index))
            return "ERROR: Syntax error, expected NO WAI keyword before line "+ str(oic_index)
        if i == len(line_table_without_groupings)-1 and not oic_flag and orly_flag and yarly_flag and not nowai_flag:
            #ERROR: O RLY? not closed and no NO WAI keyword
            print("ERROR: Syntax error, expected NO WAI keyword to close YA RLY keyword in line "+ str(yarly_index))
            return "ERROR: Syntax error, expected NO WAI keyword to close YA RLY keyword in line "+ str(yarly_index)
        if oic_flag and not orly_flag and not yarly_flag and not nowai_flag and wtf_count == 0 and omg_count == 0 and omgwtf_count == 0:
            #ERROR: Closed oic without entering an O RLY? block
            print("ERROR: Syntax error, unexpected character in line "+ str(oic_index))
            return "ERROR: Syntax error, unexpected character in line "+ str(oic_index)
    
        if oic_flag and orly_flag and yarly_flag and nowai_flag:
            orly_flag = False
            yarly_flag = False
            nowai_flag = False
            oic_flag = False
            orly_index = None
            yarly_index = None
            nowai_index = None
            oic_index = None
            yarly_count = 0
            nowai_count = 0
    return True

def checkOrderOfConditionalsSwitchCase(line_table_without_groupings):    
    # SWITCH-CASE: Pinagkaiba sa If-else, pwede marami si OMG, sa dulo lagi si OMGWTF, may kasama si OMG sa line
    wtf_flag = False
    omg_flag = False
    omgwtf_flag = False
    oic_flag = False
    
    wtf_index = None
    omg_index = None
    omgwtf_index = None
    oic_index = None

    wtf_count = 0
    omg_count = 0
    omgwtf_count = 0
    oic_count = 0

    #extra check
    orly_count = 0
    yarly_count = 0
    nowai_count = 0

    for i in range(len(line_table_without_groupings)):
        if line_table_without_groupings[i] != []:
            if line_table_without_groupings[i] == ['WTF?']:
                wtf_flag = True
                wtf_index = i + 1
                wtf_count += 1
                
                nextLine = i + 1
                while line_table_without_groupings[nextLine] == []:
                    nextLine += 1

                if line_table_without_groupings[nextLine][0] != 'OMG':
                    #ERROR: WTF? keyword must be followed immediately by an OMG keyword
                    print("ERROR: Syntax error, expected an OMG keyword right after the WTF? keyword in line "+str(wtf_index))
                    return "ERROR: Syntax error, expected an OMG keyword right after the WTF? keyword in line "+str(wtf_index)
            if line_table_without_groupings[i][0] == 'OMG':     
                omg_flag = True
                omg_index = i + 1
                omg_count += 1
            if line_table_without_groupings[i] == ['OMGWTF']:     
                omgwtf_flag = True
                omgwtf_index = i + 1
                omgwtf_count += 1
            if line_table_without_groupings[i] == ['OIC']:
                oic_flag = True
                oic_index = i + 1
                oic_count += 1

        #extra check
        if line_table_without_groupings[i] == ['O RLY?']:
            orly_count += 1
        if line_table_without_groupings[i] == ['YA RLY']:
            yarly_count += 1
        if line_table_without_groupings[i] == ['NO WAI']:
            nowai_count += 1


        if wtf_count == oic_count + 2:
            #ERROR: A WTF? block was not closed
            print("ERROR: Syntax error, WTF? block started in line "+str(wtf_index)+" but previous WTF? block was not closed")
            return "ERROR: Syntax error, WTF? block started in line "+str(wtf_index)+" but previous WTF? block was not closed"
        if omgwtf_count > 1:
            #ERROR: Syntax error, expected 1 OMGWTF for WTF? block but found 2
            print("ERROR: Syntax error, expected 1 OMGWTF keyword for WTF? block in from line "+str(wtf_index)+" but found 2")
            return "ERROR: Syntax error, expected 1 OMGWTF keyword for WTF? block in from line "+str(wtf_index)+" but found 2"
        if wtf_flag and not omg_flag and not omgwtf_flag and oic_flag:
            #ERROR: The WTF? block ended but no OMG and OMGWTF
            print("ERROR: Syntax error, expected an OMG keyword and an OMGWTF keyword before line "+str(oic_index))
            return "ERROR: Syntax error, expected an OMG keyword and an OMGWTF keyword before line "+str(oic_index)
        if omg_flag and not wtf_flag:        #may omg pero alang wtf nani
            #ERROR: Expected a start delimiter for ya rly
            print("ERROR: Syntax error, expected a WTF? start delimiter before OMG block in line "+str(omg_index))
            return "ERROR: Syntax error, expected a WTF? start delimiter before OMG block in line "+str(omg_index)
        if omgwtf_flag and not wtf_flag and not omg_flag:       #may omgwtf na pero ala pa omg nuyun
            #ERROR: Expected a WTF? keyword before OMGWTF
            print("ERROR: Syntax error, missing WTF? start delimiter before OMGWTF or misplaced keyword in line "+str(omgwtf_index))
            return "ERROR: Syntax error, missing WTf? start delimiter before OMGWTF or misplaced keyword in line "+str(omgwtf_index)
        if omgwtf_flag and not omg_flag:       #may omgwtf na pero ala pa omg
            #ERROR: Expected an OMG keyword before OMGWTF
            print("ERROR: Syntax error, expected an OMG keyword before OMGWTF in line "+str(omgwtf_index))
            return "ERROR: Syntax error, expected an OMG keyword before OMGWTF in line "+str(omgwtf_index)
        if i == len(line_table_without_groupings)-1 and not oic_flag and wtf_flag and omg_flag and omgwtf_flag:
            #ERROR: WTF? block complete but not closed
            print("ERROR: Syntax error, expected a closing keyword for WTF? block from line "+str(wtf_index))
            return "ERROR: Syntax error, expected a closing keyword for WTF? block from line "+str(wtf_index)
        if oic_flag and wtf_flag and omg_flag and not omgwtf_flag:
            #ERROR: Closed oic without entering an OMGWTF keyword
            print("ERROR: Syntax error, expected OMGWTF keyword before line "+ str(oic_index))
            return "ERROR: Syntax error, expected OMGWTF keyword before line "+ str(oic_index)
        if i == len(line_table_without_groupings)-1 and not oic_flag and wtf_flag and omg_flag and not omgwtf_flag:
            #ERROR: WTF? not closed and no OMGWTF keyword
            print("ERROR: Syntax error, expected OMGWTF keyword to close OMG keyword in line "+ str(omg_index))
            return "ERROR: Syntax error, expected OMGWTF keyword to close OMG keyword in line "+ str(omg_index)
        if oic_flag and not wtf_flag and not omg_flag and not omgwtf_flag and orly_count == 0 and yarly_count == 0 and nowai_count == 0:
            #ERROR: Closed oic without entering an WTF? block
            print("ERROR: Syntax error, unexpected character in line "+ str(oic_index))
            return "ERROR: Syntax error, unexpected character in line "+ str(oic_index)
    
        if oic_flag and wtf_flag and omg_flag and omgwtf_flag:
            wtf_flag = False
            omg_flag = False
            omgwtf_flag = False
            oic_flag = False
            wtf_index = None
            omg_index = None
            omgwtf_index = None
            oic_index = None
            omg_count = 0
            omgwtf_count = 0

    return True
        

code7 = '''
BTW for switch
HAI
  IT R 18
  WTF?
    OMG 6
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
  BOTH SAEM 18 AN SUM OF 12 AN b
  O RLY?
    YA RLY
      VISIBLE IT
      VISIBLE "it is the same"
      b R 17
      SUM OF b AN DIFF OF a AN 5
      VISIBLE IT
    NO WAI
      VISIBLE IT
      VISIBLE "it is not!"
      b R 18
      DIFFRINT b AN SUM OF 12 AN b
      VISIBLE IT
  OIC
  O RLY?
    YA RLY
      VISIBLE IT
      VISIBLE "it is the same"
      b R 17
      SUM OF b AN DIFF OF a AN 5
      VISIBLE IT
    NO WAI
      VISIBLE IT
      VISIBLE "it is not!"
      b R 18
      DIFFRINT b AN SUM OF 12 AN b
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
    I HAS A var1 ITZ SUM OF 1 AN 2
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
  VISIBLE var5
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
  ALL OF WIN AN WIN AN WIN AN FAIL AN WIN MKAY
  VISIBLE IT
  ANY OF WIN AN WIN AN WIN AN FAIL AN WIN MKAY
  VISIBLE IT
  BTW compound expressions
  BOTH OF NOT WIN AN NOT WIN
  VISIBLE IT
  EITHER OF NOT WIN AN WIN
  VISIBLE IT
  WON OF BOTH OF WIN AN WIN AN EITHER OF WIN AN FAIL
  VISIBLE IT
  ANY OF WIN AN BOTH OF NOT FAIL AN NOT FAIL AN NOT WIN AN WON OF WIN AN NOT WIN MKAY
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
  DIFFRINT BOTH SAEM 1 AN 2 AN DIFFRINT 1 AN 2
  VISIBLE IT
  BTW with variables
  I HAS A var1 ITZ WIN
  I HAS A var2 ITZ FAIL
  DIFFRINT var1 AN var2
  VISIBLE IT
  BOTH SAEM var1 AN var2
  VISIBLE IT
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

symbol_table, lexemes_table = lexical_analyzer3.LexicalAnalyzer(code6)

SyntaxAnalyzer(symbol_table, lexemes_table)


