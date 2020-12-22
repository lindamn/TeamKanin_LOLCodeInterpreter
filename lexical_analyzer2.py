import re

def LexicalAnalyzer(code):

    keywords = ["HAI", "KTHXBAI", "BTW", "OBTW", "TLDR", "I", "HAS", "A" "ITZ", "R", "SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD", "BIGGR", "SMALLR", "BOTH", "EITHER", "WON", "OF", "NOT", "ANY", "ALL", "BOTH", "SAEM", "DIFFRINT", "SMOOSH", "MAEK", "A", "IS", "NOW", "VISIBLE", "GIMMEH", "O", "RLY?", "YA", "RLY", "MEBBE", "NO", "WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM", "IN", "YR", "UPPIN", "NERFIN", "YR", "TIL", "WILE", "OUTTA"]

    lines = code.split("\n")
    print(lines)

    for a in range(0, len(lines)):
        print("current line:", lines[a])
        split_list = lines[a].split(" ")
        for words in split_list:
            for valid_words in keywords:
                if valid_words == words:
                    print(words)
        if re.search("HAI", lines[a]):
            print("hai")
            lines[a] = lines[a].partition("HAI")
        elif re.search("KTHXBAI", lines[a]):
            lines[a] = lines[a].partition("KTHXBAI")
            print("kthxbai")
        elif re.search("OBTW", lines[a]):
            lines[a] = lines[a].partition("OBTW")
            print("obtw")
        elif re.search("BTW ", lines[a]):
            lines[a] = lines[a].partition("BTW ")
            print("btw")
        elif re.search("TLDR", lines[a]):
            lines[a] = lines[a].partition("TLDR")
            print("tldr")
        elif re.search("I HAS A ", lines[a]):
            lines[a] = lines[a].partition("I HAS A ")
            print("i has a")
        elif re.search("ITZ ", lines[a]):
            lines[a] = lines[a].partition("ITZ ")
            print("itz")
        elif re.search("SUM OF ", lines[a]):
            lines[a] = lines[a].partition("SUM OF ")
            print("sum of")
        elif re.search("DIFF OF ", lines[a]):
            lines[a] = lines[a].partition("DIFF OF ")
            print("diff of")
        elif re.search("PRODUKT OF ", lines[a]):
            lines[a] = lines[a].partition("PRODUKT OF ")
            print("produkt of")
        elif re.search("QUOSHUNT OF ", lines[a]):
            lines[a] = lines[a].partition("QUOSHUNT OF ")
            print("quoshunt of")
        elif re.search("MOD OF ", lines[a]):
            lines[a] = lines[a].partition("MOD OF ")
            print("mod of")
        elif re.search("BIGGR OF ", lines[a]):
            lines[a] = lines[a].partition("BIGGR OF ")
            print("biggr of")
        elif re.search("SMALLR OF ", lines[a]):
            lines[a] = lines[a].partition("SMALLR OF ")
            print("smallr of")
        elif re.search("BOTH OF ", lines[a]):
            lines[a] = lines[a].partition("BOTH OF ")
            print("both of")
        elif re.search("EITHER OF ", lines[a]):
            lines[a] = lines[a].partition("EITHER OF ")
            print("either of")
        elif re.search("WON OF ", lines[a]):
            lines[a] = lines[a].partition("WON OF ")
            print("won of")
        elif re.search("NOT ", lines[a]):
            lines[a] = lines[a].partition("NOT ")
            print("not")
        elif re.search("ANY OF ", lines[a]):
            lines[a] = lines[a].partition("ANY OF ")
            print("any of")
        elif re.search("ALL OF ", lines[a]):
            lines[a] = lines[a].partition("ALL OF ")
            print("all of")
        elif re.search("BOTH SAEM ", lines[a]):
            lines[a] = lines[a].partition("BOTH SAEM ")
            print("both saem")
        elif re.search("DIFFRINT ", lines[a]):
            lines[a] = lines[a].partition("DIFFRINT ")
            print("diffrint")
        elif re.search("SMOOSH ", lines[a]):
            lines[a] = lines[a].partition("SMOOSH ")
            print("smoosh")
        elif re.search("MAEK ", lines[a]):
            lines[a] = lines[a].partition("MAEK")
            print("maek")
        elif re.search("IS NOW A ", lines[a]):
            lines[a] = lines[a].partition("IS NOW A ")
            print("is now a")
        elif re.search("VISIBLE ", lines[a]):
            lines[a] = lines[a].partition("VISIBLE ")
            print("visible")
        elif re.search("GIMMEH ", lines[a]):
            lines[a] = lines[a].partition("GIMMEH ")
            print("gimmeh")
        elif re.search("O RLY? ", lines[a]):
            lines[a] = lines[a].partition("O RLY? ")
            print("o rly?")
        elif re.search("YA RLY ", lines[a]):
            lines[a] = lines[a].partition("YA RLY ")
            print("ya rly")
        elif re.search("MEEBE ", lines[a]):
            lines[a] = lines[a].partition("MEEBE ")
            print("meebe")
        elif re.search("NO WAI ", lines[a]):
            lines[a] = lines[a].partition("NO WAI ")
            print("no wai")
        elif re.search("OIC ", lines[a]):
            lines[a] = lines[a].partition("OIC ")
            print("oic")
        elif re.search("WTF? ", lines[a]):
            lines[a] = lines[a].partition("WTF? ")
            print("wtf")
        elif re.search("OMG ", lines[a]):
            lines[a] = lines[a].partition("OMG ")
            print("omg")
        elif re.search("OMG WTF ", lines[a]):
            lines[a] = lines[a].partition("OMG WTF ")
            print("omg wtf")
        elif re.search("IM IN YR ", lines[a]):
            lines[a] = lines[a].partition("IM IN YR ")
            print("im in yr")
        elif re.search("UPPIN", lines[a]):
            lines[a] = lines[a].partition("UPPIN")
            print("uppin")
        elif re.search("NERFIN ", lines[a]):
            lines[a] = lines[a].partition("NERFIN ")
            print("nerfin")
        elif re.search("WILE ", lines[a]):
            lines[a] = lines[a].partition("WILE ")
            print("wile")
        elif re.search("IM OUTTA YR ", lines[a]):
            lines[a] = lines[a].partition("IM OUTTA YR ")
            print("im outta yr")
        elif re.search("-{0,1}[0-9]{1,}", lines[a]):
            print("numbr literal")
        elif re.search("-{0,1}[0-9]{1,}.{0,1}[0-9]{1,}", lines[a]):
            print("numbar literal")
        elif re.search("(WIN|FAIL)", lines[a]):
            print("troof literal")
        elif re.search("(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)", lines[a]):
            print("type literal")
        elif re.search("R ", lines[a]):
            lines[a] = lines[a].partition("R")
            print("r")
        elif re.search("YR ", lines[a]):
            lines[a] = lines[a].partition("YR")
            print("yr")
        elif re.search("TIL ", lines[a]):
            lines[a] = lines[a].partition("TIL") 
            print("til")
        elif re.search("A ", lines[a]):
            lines[a] = lines[a].partition("A") 
            print("a")
        
    print(lines)

    new_lines = []

    for i in range(0, len(lines)):
        if lines[i] != "":
            line_group = []
            if isinstance(lines[i], tuple):
                is_blank = True
                for j in range(0, len(lines[i])): #loops every element of the tuple
                    for k in range(0, len(lines[i][j])): #checks if the string is purely whitespace
                        if lines[i][j][k] != " ":
                            is_blank = False
                            break
                    if not is_blank:
                        line_group.append(lines[i][j])
            if isinstance(lines[i], str):
                is_blank = True
                for j in range(0, len(lines[i])): #loops every character of the str
                    if lines[i][j] != " ":
                        is_blank = False
                        break
                if not is_blank:
                    line_group.append(lines[i])
            new_lines.append(line_group)
    
    print("-----------------")
    print(new_lines)


code = '''BTW for arithmetic operations
HAI
    OBTW
        if your interpreter does not implement IT,
        move the expressions to the VISIBLE statement
    TLDR
'''

code2 = '''
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

LexicalAnalyzer(code2)