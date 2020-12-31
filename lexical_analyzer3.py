import re

class SymbolTableElement():
  def __init__(self, lexeme):
    self.lexeme = lexeme
    self.type = None


#check if nagfofollow sa tamang format yung mga lexemes

def LexicalAnalyzer(code):

    keywords = ["HAI", "KTHXBYE", "BTW", "OBTW", "TLDR", "I", "HAS", "A" "ITZ", "R", "SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD", "BIGGR", "SMALLR", "BOTH", "EITHER", "WON", "OF", "NOT", "ANY", "ALL", "BOTH", "SAEM", "DIFFRINT", "SMOOSH", "MAEK", "A", "IS", "NOW", "VISIBLE", "GIMMEH", "O", "RLY?", "YA", "RLY", "MEBBE", "NO", "WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM", "IN", "YR", "UPPIN", "NERFIN", "YR", "TIL", "WILE", "OUTTA", "MKAY"]
    operators = ["SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD", "BIGGR", "SMALLR", "EITHER", "WON", "ANY", "ALL"]
    etc = ["I", "BOTH", "IS", "O", "YA", "IM", "NO"]

    lines = code.split("\n")

    symbol_table = []

    # splits the lines by spaces
    for i in range(0, len(lines)):
        if re.search(r"\s*VISIBLE",lines[i]) and re.search(r"\s*V", lines[i]) or re.search(r"[A-z]{1}([A-z0-9_])*\sR\s", lines[i]):      #eto lang yung nabago mami
            quote_flag = False
            strings = re.findall(r"[\"]([^\"]*)[\"]", lines[i])
            strings_count = len(strings)
            temp = lines[i].split(" ")
            #cleans the temp list, removes empty strings
            new_temp = []
            for j in range(0, len(temp)):
                if temp[j] != "":
                    new_temp.append(temp[j])
            
            #appends the variables and literals to the list of lexemes
            new_split_list = []
            if re.search(r"\s*VISIBLE", lines[i]) and re.search(r"\s*V", lines[i]):
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

        new_split_list = []
        for j in range(0, len(split_list)):
            if split_list[j] != "":
                new_split_list.append(split_list[j])
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

    #removes the OBTW and BTW and replaces it with empty lists
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
      if len(line) != 0:
        if line[0] == "BTW":
          line = []
      

    all_keywords = ["HAI", "KTHXBYE", "I HAS A", "ITZ", "VISIBLE", "GIMMEH", "IT", "SMOOSH", "ALL OF", "ANY OF", "MKAY","NOT", "AN", "SUM OF", "DIFF OF", "PRODUKT OF",
    "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF", "BOTH SAEM", "DIFFRINT", "FAIL", "WIN", "R", "O RLY?", "YA RLY", "NO WAI",
    "OIC", "MEBBE", "WTF?", "OMG", "OMGWTF"]

    lexError = False
    # checks if all lexemes are valid
    for i in range(len(symbol_table)):
      #checks if current line is not empty
      if symbol_table[i] != []:
        for j in range(len(symbol_table[i])):
          #checks if token is keyword, or string, or int, or float, or var
          if not (symbol_table[i][j] in all_keywords or re.match(r"[\"]([^\"]*?)[\"]$",symbol_table[i][j]) or re.match(r"-{0,1}[0-9]{1,}$",symbol_table[i][j]) or re.match(r"-{0,1}[0-9]{1,}\.[0-9]{1,}$", symbol_table[i][j]) or re.match(r"[a-zA-Z]{1}([a-zA-Z0-9_])*$", symbol_table[i][j])):
            # print("ERROR: Invalid token at line "+ str(symbol_table.index(symbol_table[i])) +": "+str(symbol_table[i][j]))
            lexError = "ERROR: Invalid token at line "+ str(symbol_table.index(symbol_table[i])) +": "+str(symbol_table[i][j])
            
    if lexError:
      return lexError

    #adds all lexemes in the symbol table
    lexemes_table = []

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
      elif element.lexeme == "SUM OF":
        element.type = "ADD Operator"
      elif element.lexeme == "DIFF OF":
        element.type = "SUBTRACT Operator"
      elif element.lexeme == "PRODUKT OF":
        element.type = "MULTIPLY Operator"
      elif element.lexeme == "QUOSHUNT OF":
        element.type = "DIVIDE Operator"
      elif element.lexeme == "MOD OF":
        element.type = "MODULO Operator"
      elif element.lexeme == "BIGGR OF":
        element.type = "MAX Operator"
      elif element.lexeme == "SMALLR OF":
        element.type = "MIN Operator"
      elif element.lexeme == "EITHER OF":
        element.type = "OR Operator"
      elif element.lexeme == "BOTH OF":
        element.type = "AND Operator"
      elif element.lexeme == "WON OF":
        element.type = "XOR Operator"
      elif element.lexeme == "ALL OF":
        element.type = "Infinite Arity Boolean Operation Delimiter"
      elif element.lexeme == "ANY OF":
        element.type = "Infinite Arity Boolean Operation Delimiter"
      elif element.lexeme == "BOTH SAEM":
        element.type = "EQUALS Operator"
      elif element.lexeme == "DIFFRINT":
        element.type = "NOT EQUAL Operator"
      elif element.lexeme == "NOT":
        element.type = "NOT Operator"
      elif element.lexeme == "MKAY":
        element.type = "Infinite Arity Boolean Operation Delimiter"
      elif re.match(r"^[A-z]{1}([A-z0-9_])*", element.lexeme) :
        element.type = "Variable Identifier"

    #UNCOMMENT TO CHECK THE FINAL lexemes_table AND THE symbol_table (code per line)
    '''for i in range(len(lexemes_table)):
      print([lexemes_table[i].lexeme, lexemes_table[i].type])

    print()
    
    for line in symbol_table:
      print(line)
    '''
    return symbol_table, lexemes_table