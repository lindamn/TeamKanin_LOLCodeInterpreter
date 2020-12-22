import re, lexical_analyzer3

def SyntaxAnalyzer(symbol_table):

    arithmetic_keywords = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]
    comparison_keywords = ["BOTH SAEM", "DIFFRINT"]
    boolean_keywords = ["BOTH OF", "EITHER OF", "WON OF"]
    unary_keywords = ["NOT"]
    infinite_keywords = ["ALL OF", "ANY OF"]
    io_keywords = ["VISIBLE", "GIMMEH"]
    if_keywords = ["O RLY?", "YA RLY", "NO WAI", "OIC"]
    switch_keywords = ["WTF?", "OMG", "OMGWTF", "OIC"]
    obtw_flag = False

    for i in range(0, len(symbol_table)):
        line = symbol_table[i]
        print("current line:", line)
        if len(line) != 0:
            # ignores comments
            if line[0] == "TLDR":
                obtw_flag = False
            if obtw_flag == False:
                if line[0] == "OBTW":
                    obtw_flag = True
                for j in range(0, len(line)):
                    if line[j] == "BTW":
                        print("ignore (btw)")
                        break
            else:
                print("ignore (obtw)")
                continue
            
            #deals w arithmetic
            arithmetic_counter = 0
            if line[0] in arithmetic_keywords:
                for j in range(0, len(line)):
                    if line[j] in arithmetic_keywords:
                        arithmetic_counter += 1
                while arithmetic_counter > 0:
                    for j in range(0, len(line)):
                        if line[j] == "AN":
                            if isinstance(line[j-1], str) and isinstance(line[j+1], str):
                                if line[j-1] in arithmetic_keywords and line[j+1] in arithmetic_keywords:
                                    continue
                                else:
                                    arithmetic_counter -= 1
                                    new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                                    line[j-2] = new_grouping
                                    line.pop(j-1)
                                    line.pop(j-1)
                                    line.pop(j-1)
                                    break
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
                print(line)

            #deals w comparison
            if line[0] in comparison_keywords:
                if len(line) == 4:
                    #both saem and diffrint na ito
                    print("comparison")
                elif len(line) == 7:
                    #relational operators
                    print("relational")

            #deals w boolean
            boolean_counter = 0
            not_counter = 0
            if line[0] in boolean_keywords or line[0] in unary_keywords:
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
                                else:
                                    boolean_counter -= 1
                                    new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                                    line[j-2] = new_grouping
                                    line.pop(j-1)
                                    line.pop(j-1)
                                    line.pop(j-1)
                                    break
                            elif isinstance(line[j-1], list) and isinstance(line[j+1], str):
                                if line[j+1] in boolean_keywords:
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
                                if line[j-1] in boolean_keywords:
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
                                boolean_counter -= 1
                                new_grouping = [line[j-2],line[j-1],line[j],line[j+1]]
                                line[j-2] = new_grouping
                                line.pop(j-1)
                                line.pop(j-1)
                                line.pop(j-1)
                                break
                print(line)



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

symbol_table = lexical_analyzer3.LexicalAnalyzer(code)
SyntaxAnalyzer(symbol_table)