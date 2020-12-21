# https://github.com/christianrfg/lexical-analyzer

import re

def LexicalAnalyzer(code):
    check_string = ""
    btw_flag = False
    obtw_flag = False

    for i in range(0, len(code)):
        print(str(i)+" current string:"+ check_string)
        # print("current btw_flag and obtw_flag:", btw_flag, obtw_flag)
        # if code[i] != "\n" or code[i] != "\t":
        #     check_string = check_string + code[i]
        # elif code[i] == "\n":
        #     print("new line")
        #     check_string = ""
        # elif code[i] == "\t":
        #     print("tab")
        #     check_string = ""
        if code[i] == "\n":
            print("new line")
            check_string = ""
        elif code[i] == "   ":
            print("new tab")
            check_string = ""
        else:
            check_string = check_string + code[i]

        if btw_flag == False and obtw_flag == False:
            if check_string == "HAI":
                print("hai")
                check_string = ""
            elif re.match("KTHXBAI", check_string):
                print("kthxbai")
                check_string = ""
            elif re.match("BTW", check_string):
                btw_flag = True
                print("btw")
                check_string = ""
            elif re.match("OBTW", check_string):
                obtw_flag = True
                print("obtw")
                check_string = ""
            elif re.match("I HAS A", check_string):
                print("i has a")
                check_string = ""
            elif re.match("ITZ", check_string):
                print("itz")
                check_string = ""
            elif re.match("R", check_string):
                print("r")
                check_string = ""
            elif re.match("SUM OF", check_string):
                print("sum of")
                check_string = ""
            elif re.match("DIFF OF", check_string):
                print("diff of")
                check_string = ""
            elif re.match("PRODUKT OF", check_string):
                print("produkt of")
                check_string = ""
            elif re.match("QUOSHUNT OF", check_string):
                print("quoshunt of")
                check_string = ""
            elif re.match("MOD OF", check_string):
                print("mod of")
                check_string = ""
            elif re.match("BIGGR OF", check_string):
                print("biggr of")
                check_string = ""
            elif re.match("SMALLR OF", check_string):
                print("smallr of")
                check_string = ""
            elif re.match("BOTH OF", check_string):
                print("both of")
                check_string = ""
            elif re.match("EITHER OF", check_string):
                print("either of")
                check_string = ""
            elif re.match("WON OF", check_string):
                print("won of")
                check_string = ""
            elif re.match("NOT", check_string):
                print("not")
                check_string = ""
            elif re.match("ANY OF", check_string):
                print("any of")
                check_string = ""
            elif re.match("ALL OF", check_string):
                print("all of")
                check_string = ""
            elif re.match("BOTH SAEM", check_string):
                print("both saem")
                check_string = ""
            elif re.match("DIFFRINT", check_string):
                print("diffrint")
                check_string = ""
            elif re.match("SMOOSH", check_string):
                print("smoosh")
                check_string = ""
            elif re.match("MAEK", check_string):
                print("maek")
                check_string = ""
            elif re.match("A", check_string):
                print("a")
                check_string = ""
            elif re.match("IS NOW A", check_string):
                print("is now a")
                check_string = ""
            elif re.match("VISIBLE", check_string):
                print("visible")
                check_string = ""
            elif re.match("GIMMEH", check_string):
                print("gimmeh")
                check_string = ""
            elif re.match("O RLY?", check_string):
                print("o rly?")
                check_string = ""
            elif re.match("YA RLY", check_string):
                print("ya rly")
                check_string = ""
            elif re.match("MEEBE", check_string):
                print("meebe")
                check_string = ""
            elif re.match("NO WAI", check_string):
                print("no wai")
                check_string = ""
            elif re.match("OIC", check_string):
                print("oic")
                check_string = ""
            elif re.match("WTF?", check_string):
                print("wtf")
                check_string = ""
            elif re.match("OMG", check_string):
                print("omg")
                check_string = ""
            elif re.match("OMG WTF", check_string):
                print("omg wtf")
                check_string = ""
            elif re.match("IM IN YR", check_string):
                print("im in yr")
                check_string = ""
            elif re.match("UPPIN", check_string):
                print("uppin")
                check_string = ""
            elif re.match("NERFIN", check_string):
                print("nerfin")
                check_string = ""
            elif re.match("YR", check_string):
                print("yr")
                check_string = ""
            elif re.match("TIL", check_string):
                print("til")
                check_string = ""
            elif re.match("WILE", check_string):
                print("wile")
                check_string = ""
            elif re.match("IM OUTTA YR", check_string):
                print("im outta yr")
                check_string = ""
            # elif re.match("[a-Z]{1}([a-Z0-9])*", check_string):
            # elif re.match("\w+$", check_string):
            #  
            #     print("variable/fxn/loop identifier")
            elif re.match("-{0,1}[0-9]{1,}", check_string):
                print("numbr literal")
                check_string = ""
            elif re.match("-{0,1}[0-9]{1,}.{0,1}[0-9]{1,}", check_string):
                print("numbar literal")
                check_string = ""
            elif re.match("(WIN|FAIL)", check_string):
                print("troof literal")
                check_string = ""
            elif re.match("(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)", check_string):
                check_string = ""
                print("type literal")
            # else:
            #     print("not read") 
        else:
            if btw_flag == True:
                if code[i] == "\n":
                    print("end comment! (btw)")
                    btw_flag = False
                    check_string = ""
            if obtw_flag == True:
                if code[i] == "T":
                    if code[i+1] == "L" and code[i+2] == "D" and code[i+3] == "R":
                        print("end comment! (obtw)")
                        obtw_flag = False
                        check_string = ""
                    

code = '''BTW for arithmetic operations
HAI
    OBTW
        if your interpreter does not implement IT,
        move the expressions to the VISIBLE statement
    TLDR
'''
'''
  BTW basic expressions
  SUM OF 1 AN 2
  VISIBLE IT
  DIFF OF 1 AN 2
  VISIBLE IT
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

LexicalAnalyzer(code)