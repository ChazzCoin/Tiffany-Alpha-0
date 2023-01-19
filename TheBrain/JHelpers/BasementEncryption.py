from F.TYPE.Dict import fict

dic = { "a" : 26, "b" : 25, "c" : 24, "d" : 23,
        "e" : 22, "f" : 21, "g" : 20, "h" : 19,
        "i" : 18, "j" : 17, "k" : 16, "l" : 15,
        "m" : 14, "n" : 13, "o" : 12, "p" : 11,
        "q" : 10, "r" : 9, "s" : 8, "t" : 7,
        "u" : 6, "v" : 5, "w" : 4, "x" : 3,
        "y" : 2, "z" : 1}

keys = fict(dic)

"14-26-15-15-12-9-2 9-12-14-22-12"
clear = "MalloryRomeo"
hidden = "14-26-15-15-12-9-2 9-12-14-22-12"

def decrypt():
        # decrypt
        temp = ""
        t = ""
        count = len(hidden) - 1
        i = 0
        for char in hidden:
            if i >= count:
                temp = temp + str(char)
                temp = str(temp).replace("-", "").replace(" ", "")
                m = keys.find_key_by_value(temp)
                t += m
            if str(char) == "-":
                if temp != "":
                    temp = str(temp).replace("-", "").replace(" ", "")
                    m = keys.find_key_by_value(temp)
                    t += m
                    temp = ""
            elif str(char) == " ":
               if temp != "":
                    temp = str(temp).replace("-", "").replace(" ", "")
                    m = keys.find_key_by_value(temp)
                    t += m + " "
                    temp = ""
            temp = temp + str(char)
            i += 1
        print(t)

def encrypt():
        # Encrypt
        t = ""
        for char in clear:
                digit = dic[str(char).lower()]
                t += "-" + str(digit)
        print(t)

