import re

def LexicalAnalyzer(code):
    # check_string = ""
    btw_flag = False
    obtw_flag = False

    check_string = code.split("\n")
    print(check_string)

    for a in range(0, len(check_string)):
        print("current line:", check_string[a])
        if re.match("HAI", check_string[a]):
            print("hai")
            check_string[a] = check_string[a].partition("HAI")
            # hai_flag = True
        elif re.match("KTHXBAI", check_string[a]):
            print("kthxbai")
        elif re.match("BTW", check_string[a]):
            # btw_flag = True
            check_string[a] = check_string[a].partition("BTW")
            print("btw")
        elif re.match("OBTW", check_string[a]):
            # obtw_flag = True
            check_string[a] = check_string[a].partition("OBTW")
            print("obtw")
        elif re.match("I HAS A", check_string[a]):
            print("i has a")
        elif re.match("ITZ", check_string[a]):
            print("itz")
        elif re.match("R", check_string[a]):
            print("r")
        elif re.match("SUM OF", check_string[a]):
            print("sum of")
        elif re.match("DIFF OF", check_string[a]):
            print("diff of")
        elif re.match("PRODUKT OF", check_string[a]):
            print("produkt of")
        elif re.match("QUOSHUNT OF", check_string[a]):
            print("quoshunt of")
        elif re.match("MOD OF", check_string[a]):
            print("mod of")
        elif re.match("BIGGR OF", check_string[a]):
            print("biggr of")
        elif re.match("SMALLR OF", check_string[a]):
            print("smallr of")
        elif re.match("BOTH OF", check_string[a]):
            print("both of")
        elif re.match("EITHER OF", check_string[a]):
            print("either of")
        elif re.match("WON OF", check_string[a]):
            print("won of")
        elif re.match("NOT", check_string[a]):
            print("not")
        elif re.match("ANY OF", check_string[a]):
            print("any of")
        elif re.match("ALL OF", check_string[a]):
            print("all of")
        elif re.match("BOTH SAEM", check_string[a]):
            print("both saem")
        elif re.match("DIFFRINT", check_string[a]):
            print("diffrint")
        elif re.match("SMOOSH", check_string[a]):
            print("smoosh")
        elif re.match("MAEK", check_string[a]):
            print("maek")
        elif re.match("A", check_string[a]):
            print("a")
        elif re.match("IS NOW A", check_string[a]):
            print("is now a")
        elif re.match("VISIBLE", check_string[a]):
            print("visible")
        elif re.match("GIMMEH", check_string[a]):
            print("gimmeh")
        elif re.match("O RLY?", check_string[a]):
            print("o rly?")
        elif re.match("YA RLY", check_string[a]):
            print("ya rly")
        elif re.match("MEEBE", check_string[a]):
            print("meebe")
        elif re.match("NO WAI", check_string[a]):
            print("no wai")
        elif re.match("OIC", check_string[a]):
            print("oic")
        elif re.match("WTF?", check_string[a]):
            print("wtf")
        elif re.match("OMG", check_string[a]):
            print("omg")
        elif re.match("OMG WTF", check_string[a]):
            print("omg wtf")
        elif re.match("IM IN YR", check_string[a]):
            print("im in yr")
        elif re.match("UPPIN", check_string[a]):
            print("uppin")
        elif re.match("NERFIN", check_string[a]):
            print("nerfin")
        elif re.match("YR", check_string[a]):
            print("yr")
        elif re.match("TIL", check_string[a]):
            print("til")
        elif re.match("WILE", check_string[a]):
            print("wile")
        elif re.match("IM OUTTA YR", check_string[a]):
            print("im outta yr")
        # elif re.match("[a-Z]{1}([a-Z0-9])*", check_string[a]):
        # elif re.match("\w+$", check_string[a]):
        #  
        #     print("variable/fxn/loop identifier")
        elif re.match("-{0,1}[0-9]{1,}", check_string[a]):
            print("numbr literal")
        elif re.match("-{0,1}[0-9]{1,}.{0,1}[0-9]{1,}", check_string[a]):
            print("numbar literal")
        elif re.match("(WIN|FAIL)", check_string[a]):
            print("troof literal")
        elif re.match("(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)", check_string[a]):
            print("type literal")
        # else:
        #     print("not read") 

    print(check_string)



code = '''BTW for arithmetic operations
HAI
    OBTW
        if your interpreter does not implement IT,
        move the expressions to the VISIBLE statement
    TLDR
'''

LexicalAnalyzer(code)