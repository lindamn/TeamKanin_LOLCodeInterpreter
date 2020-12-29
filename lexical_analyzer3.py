import re

class SymbolTableElement():
  def __init__(self, lexeme):
    self.lexeme = lexeme
    self.type = None

def LexicalAnalyzer(code):

    keywords = ["HAI", "KTHXBYE", "BTW", "OBTW", "TLDR", "I", "HAS", "A" "ITZ", "R", "SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD", "BIGGR", "SMALLR", "BOTH", "EITHER", "WON", "OF", "NOT", "ANY", "ALL", "BOTH", "SAEM", "DIFFRINT", "SMOOSH", "MAEK", "A", "IS", "NOW", "VISIBLE", "GIMMEH", "O", "RLY?", "YA", "RLY", "MEBBE", "NO", "WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM", "IN", "YR", "UPPIN", "NERFIN", "YR", "TIL", "WILE", "OUTTA"]
    operators = ["SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD", "BIGGR", "SMALLR", "EITHER", "WON", "ANY", "ALL"]
    etc = ["I", "BOTH", "IS", "O", "YA", "IM", "NO"]

    lines = code.split("\n")

    symbol_table = []

    # splits the lines by spaces
    for i in range(0, len(lines)):
        if re.search("VISIBLE",lines[i]) and re.search("\s{2,}V", lines[i]) or re.search(r"[A-z]{1}([A-z0-9_])*\sR\s", lines[i]):      #eto lang yung nabago mami
            quote_flag = False
            strings = re.findall(r"[\"]([^\"]*?)[\"]", lines[i])

            strings_count = len(strings)
            temp = lines[i].split(" ")
            #cleans the temp list, removes empty strings
            new_temp = []
            for j in range(0, len(temp)):
                if temp[j] != "":
                    new_temp.append(temp[j])
            
            #appends the variables and literals to the list of lexemes
            new_split_list = []
            if re.search("VISIBLE", lines[i]) and re.search("\s{2,}V", lines[i]):
                new_split_list.append("VISIBLE")
            for j in range(0, len(new_temp)):
                # counts the number of double quotes in a string, if it is 2 then it automatically adds the string to the list of lexemes
                # if it is one, it keeps track until the other double quotes show up (and appends the str once it sees the double quotes)
                quote_count = new_temp[j].count("\"")
                if new_temp[j] == "VISIBLE":
                    continue
                if "\"" in new_temp[j]:
                    if quote_count == 1:
                        if quote_flag == False:
                            quote_flag = True
                        else:
                            quote_flag = False
                            new_str = "\""+strings[len(strings)-strings_count]+"\""
                            strings_count -= 1
                            new_split_list.append(new_str)
                    else:
                        new_str = "\""+strings[len(strings)-strings_count]+"\""
                        strings_count -= 1
                        new_split_list.append(new_str)
                else:
                    if quote_flag == False:
                        new_split_list.append(new_temp[j])
            symbol_table.append(new_split_list)
            continue

        # for other cases aside VISIBLE
        split_list = lines[i].split(" ")

        # for words in split_list:
        #     for valid_words in keywords:
        #         if valid_words == words:
        #             continue

        new_split_list = []
        for j in range(0, len(split_list)):
            if split_list[j] != "":
                new_split_list.append(split_list[j])
        # if new_split_list != []:
        symbol_table.append(new_split_list)
        
    # pagsasama samahin yung mga keywords separated w spaces
    for i in range(0, len(symbol_table)):
        operator_flag = 0
        etc_flag = 0
        for j in range(0, len(symbol_table[i])):
            if symbol_table[i][j] in operators:
                operator_flag += 1
            if symbol_table[i][j] in etc:
                etc_flag += 1
        while operator_flag > 0:
            for j in range(0, len(symbol_table[i])):
                if symbol_table[i][j] in operators:
                    if symbol_table[i][j+1] == "OF":
                        symbol_table[i][j] = symbol_table[i][j] + " OF"
                        symbol_table[i].pop(j+1)
                        operator_flag -= 1
                        break
                    else:
                        operator_flag -= 1
                        break      
        
        while etc_flag > 0:
            for j in range(0, len(symbol_table[i])):
                if symbol_table[i][j] in etc:
                    # checks if j goes out of bounds
                    j_plus_1_flag = True
                    j_plus_2_flag = True
                    if j+1 >= len(symbol_table[i]):
                        j_plus_1_flag = False
                        j_plus_2_flag = False
                    if j+2 >= len(symbol_table[i]):
                        j_plus_2_flag = False
                    if j_plus_1_flag:
                        if symbol_table[i][j] == "BOTH" and symbol_table[i][j+1] == "SAEM":
                            symbol_table[i][j] = "BOTH SAEM"
                            symbol_table[i].pop(j+1)
                            etc_flag -= 1
                            break
                        if symbol_table[i][j] == "O" and symbol_table[i][j+1] == "RLY?":
                            symbol_table[i][j] = "O RLY?"
                            symbol_table[i].pop(j+1)
                            etc_flag -= 1
                            break
                        if symbol_table[i][j] == "YA" and symbol_table[i][j+1] == "RLY":
                            symbol_table[i][j] = "YA RLY"
                            symbol_table[i].pop(j+1)
                            etc_flag -= 1
                            break
                        if symbol_table[i][j] == "NO" and symbol_table[i][j+1] == "WAI":
                            symbol_table[i][j] = "NO WAI"
                            symbol_table[i].pop(j+1)
                            etc_flag -= 1
                            break
                        if symbol_table[i][j] == "BOTH" and symbol_table[i][j+1] == "OF":
                            symbol_table[i][j] = "BOTH OF"
                            symbol_table[i].pop(j+1)
                            etc_flag -= 1
                            break
                    if j_plus_2_flag:
                        if symbol_table[i][j] == "I" and symbol_table[i][j+1] == "HAS" and symbol_table[i][j+2] == "A":
                            symbol_table[i][j] = "I HAS A"
                            symbol_table[i].pop(j+1)
                            symbol_table[i].pop(j+1)
                            etc_flag -= 1
                            break
                        if symbol_table[i][j] == "IS" and symbol_table[i][j+1] == "NOW" and symbol_table[i][j+2] == "A":
                            symbol_table[i][j] = "IS NOW A"
                            symbol_table[i].pop(j+1)
                            symbol_table[i].pop(j+1)
                            etc_flag -= 1
                            break
                        if symbol_table[i][j] == "IM" and symbol_table[i][j+1] == "IN" and symbol_table[i][j+2] == "YR":
                            symbol_table[i][j] = "IM IN YR"
                            symbol_table[i].pop(j+1)
                            symbol_table[i].pop(j+1)
                            etc_flag -= 1
                            break
                        if symbol_table[i][j] == "IM" and symbol_table[i][j+1] == "OUTTA" and symbol_table[i][j+2] == "YR":
                            symbol_table[i].pop(j+1)
                            symbol_table[i].pop(j+1)
                            etc_flag -= 1
                            break                            

    #replaces the BTW single line comments with [] in the symbol_table (list of lines)
    for line in symbol_table:
      if line != [] and line[0] == 'BTW':
        symbol_table[symbol_table.index(line)] = []

      #for the BTW comments in the same line with other valid lines
      btwIndex = False
      for i in range(len(line)):
        if line[i] == 'BTW':
          btwIndex = i
          break
      if btwIndex:
        while len(line) != btwIndex:
          line.pop(-1)

    #adds all lexemes in the symbol table
    lexemes_table = []

    for line in symbol_table:
      if line == ['OBTW']:
        index = symbol_table.index(line)
        symbol_table.pop(index)
        counter = 2
        while symbol_table[index] != ['TLDR']:
          symbol_table.pop(index)
          counter += 1
        symbol_table.pop(index)
        while counter > 0:
          symbol_table.insert(index, [])
          counter -= 1
      if line == ['KTHXBYE']:
        symbol_table.pop(symbol_table.index(line)+1)

    for line in range(len(symbol_table)):
      for i in range(len(symbol_table[line])):
        lexemes_table.append(SymbolTableElement(symbol_table[line][i]))

    #adds the type of lexemes (for tokens) part 1 (operator types in part2 in syntax analyzer)
    for element in lexemes_table:
      if re.match(r"^\".*\"$", element.lexeme):
        element.type = "YARN Literal"
      elif re.match(r"^-?[0-9]*$",element.lexeme):
        element.type = "NUMBR Literal"
      elif re.match(r"^-?[0-9]+\.[0-9]+$", element.lexeme):
        element.type = "NUMBAR Literal"
      elif re.match(r"^(WIN|FAIL)$", element.lexeme):
        element.type = "TROOF Literal"
      elif element.lexeme in ["HAI", "KTHXBYE"]:
        element.type = "Code Delimiter"
      elif element.lexeme == "VISIBLE":
        element.type = "Output Keyword"
      elif element.lexeme == "GIMMEH":
        element.type = "Input Keyword"
      elif element.lexeme == "I HAS A":
        element.type = "Variable Declaration"
      elif element.lexeme == "ITZ":
        element.type = "Variable Initialization"
      elif element.lexeme == "IT":
        element.type = "Implicit Variable"
      elif element.lexeme == "R":
        element.type = "Assignment Operator"
      elif element.lexeme == "O RLY?":
        element.type = "If-Else Block Delimiter"    
      elif element.lexeme == "YA RLY":
        element.type = "If-Clause Keyword"
      elif element.lexeme == "NO WAI":
        element.type = "Else-Clause Keyword"
      elif element.lexeme == "WTF?":
        element.type = "Switch-Case Block Delimiter"   
      elif element.lexeme == "OMG":
        element.type = "Case Keyword"
      elif element.lexeme == "OMGWTF":
        element.type = "Switch-Case Default Keyword"
      elif element.lexeme == "GTFO":
        element.type = "Break Keyword"
      elif element.lexeme == "OIC":
        element.type = "Conditional Block Delimiter"
      elif re.match(r"^[A-z]{1}([A-z0-9_])*", element.lexeme) :
        element.type = "Variable Identifier"

    #UNCOMMENT TO CHECK THE FINAL lexemes_table AND THE symbol_table (code per line)
    '''for i in range(len(lexemes_table)):
      print([lexemes_table[i].lexeme, lexemes_table[i].type])

    print()

    for line in symbol_table:
      print(line)'''

    return symbol_table, lexemes_table

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
LexicalAnalyzer(code)