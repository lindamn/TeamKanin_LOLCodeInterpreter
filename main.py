# import Tkinter
# top = Tkinter.Tk()

# top.mainloop()
import re
code = '''HAI

KTHXBAI'''
check_string = ""
#lexeme analyzer ????
for i in range(0, len(code)):
    # print("Current string:", check_string)
    if code[i] != "\n":
        check_string = check_string + code[i]
    if re.match("^HAI$", check_string):
        check_string = ""
        print("Code Delimiter")
    elif re.match("^KTHXBAI$", check_string):
        check_string = ""
        print("Code Delimiter")
    elif re.match("^BTW$", check_string):
        check_string = ""
    elif re.match("^OBTW$", check_string):
        check_string = ""
    elif re.match("^TLDR$", check_string):
        check_string = ""
    elif re.match("^I HAS A$", check_string):
        check_string = ""
    elif re.match("^ITZ$", check_string):
        check_string = ""
    elif re.match("^R$", check_string):
        check_string = ""
    elif re.match("^SUM OF$", check_string):
        check_string = ""
    elif re.match("^DIFF OF$", check_string):
        check_string = ""
    elif re.match("^PRODUKT OF$", check_string):
        check_string = ""
    elif re.match("^QUOSHUNT OF$", check_string):
        check_string = ""
    elif re.match("^MOD OF$", check_string):
        check_string = ""
    elif re.match("^BIGGR OF$", check_string):
        check_string = ""
    elif re.match("^SMALLR OF$", check_string):
        check_string = ""
    elif re.match("^BOTH OF$", check_string):
        check_string = ""
    elif re.match("^EITHER OF$", check_string):
        check_string = ""
    elif re.match("^WON OF$", check_string):
        check_string = ""
    elif re.match("^NOT$", check_string):
        check_string = ""
    elif re.match("^ANY OF$", check_string):
        check_string = ""
    elif re.match("^ALL OF$", check_string):
        check_string = ""
    elif re.match("^BOTH SAEM$", check_string):
        check_string = ""
    elif re.match("^DIFFRINT$", check_string):
        check_string = ""
    elif re.match("^SMOOSH$", check_string):
        check_string = ""
    elif re.match("^MAEK$", check_string):
        check_string = ""
    elif re.match("^A$", check_string):
        check_string = ""
    elif re.match("^IS NOW A$", check_string):
        check_string = ""
    elif re.match("^VISIBLE$", check_string):
        check_string = ""
    elif re.match("^GIMMEH$", check_string):
        check_string = ""
    elif re.match("^O RLY?$", check_string):
        check_string = ""
    elif re.match("^YA RLY$", check_string):
        check_string = ""
    elif re.match("^MEEBE$", check_string):
        check_string = ""
    elif re.match("^NO WAI$", check_string):
        check_string = ""
    elif re.match("^OIC$", check_string):
        check_string = ""
    elif re.match("^WTF?$", check_string):
        check_string = ""
    elif re.match("^OMG$", check_string):
        check_string = ""
    elif re.match("^OMG WTF$", check_string):
        check_string = ""
    elif re.match("^IM IN YR$", check_string):
        check_string = ""
    elif re.match("^UPPIN$", check_string):
        check_string = ""
    elif re.match("^NERFIN$", check_string):
        check_string = ""
    elif re.match("^YR$", check_string):
        check_string = ""
    elif re.match("^TIL$", check_string):
        check_string = ""
    elif re.match("^WILE$", check_string):
        check_string = ""
    elif re.match("^IM OUTTA YR$", check_string):
        check_string = ""