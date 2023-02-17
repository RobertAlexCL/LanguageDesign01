"""
Driver program for the Thompson's construction algorithm

Author: Roberto Castillo

"""

from thompson import Thompson


print("laboratorio A")
wantsToContinue = True
regex = ""
while wantsToContinue and regex != "exit":
    print("Ingrese una expresion regular:")
    regex = input()
    # Try except to catch syntax errors
    if regex != "exit":
        try:
            thompson = Thompson(regex)
            postfix = thompson.infix_to_postfix(regex)
            print("Postfix: ", postfix)
            thompsonNFA = thompson.createNfafromRegex()
            thompsonNFA.show()
            thompsonNFA.render("NFA")
        except:
            print("Error de sintaxis, ingrese una nueva exresion regular")
    else:
        wantsToContinue = False
        print("Adios")
