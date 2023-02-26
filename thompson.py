
"""

This class covers the implementation of Thompson's algorithm for an infix function, 
from its conversion to Thompson to the creation of a Non-Deterministic Finite Automaton.

Author: Roberto Castillo

"""

from finiteAutomata import FiniteAutomaton
from managers import epsilon, combine_transitions



class Thompson():
    def __init__(self, regex):
        self.regex = regex
        self.nextSymbol = 0
        self.parseRegex()

    def parseRegex(self):
        i = 0
        regex = ''
        while i < len(self.regex):
            regex += self.regex[i]
            if self.regex[i] !="(" and self.regex[i] != "|":
                if i + 1< len(self.regex) and (self.regex[i + 1].isalnum() or self.regex[i + 1] == '(') :
                    regex += "."
            i += 1
        self.regex = regex

    def infix_to_postfix(self, regex):
        # Dict to the precedence of the operators
        precedence = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1, '(': 0}

        # Stack for maintaining operators
        operator_stack = []

        # List for maintaining the postfix expression
        postfix_list = []

        # Delete all spaces from the regular expression
        regex = regex.replace(' ', '')

        # Iterate through the characters of the regular expression
        for char in regex:
            if char == '(':
                # If the character is a left parenthesis, push it to the stack
                operator_stack.append(char)
            elif char == ')':
                # If the character is a right parenthesis, pop the stack until we find the left parenthesis
                top_operator = operator_stack.pop()
                while top_operator != '(':
                    postfix_list.append(top_operator)
                    top_operator = operator_stack.pop()
            elif char in '*+?.|':
                # If the character is an operator, pop all the operators from the stack that have
                # greater precedence than the current operator and append them to the postfix list
                while operator_stack and precedence[char] <= precedence[operator_stack[-1]]:
                    postfix_list.append(operator_stack.pop())
                # Add the current operator to the stack
                operator_stack.append(char)
            else:
                # If the character is an operand, append it to the postfix list
                postfix_list.append(char)

        # Drop all the remaining operators from the stack and append them to the postfix list
        while operator_stack:
            postfix_list.append(operator_stack.pop())

        # Last, convert the list to a string
        postfix = ''.join(postfix_list)

        # Return the postfix expression
        return postfix

        
    # Functions to create nfaStack from postfix
    def getSymbol(self):
        to_return = self.nextSymbol
        self.nextSymbol += 1
        return to_return

    def symbolNFA(self,char):
        firstSymbol = self.getSymbol()
        secondSymbol = self.getSymbol()
        states = set([firstSymbol, secondSymbol])
        if char ==epsilon:
            alphabet = set()
        else:
            alphabet = set(char)
        initialState = firstSymbol
        finalStates = set([secondSymbol])
        transitions = {
            firstSymbol:{
                char:set([secondSymbol])
            },
            secondSymbol:{
            }
        }
        return FiniteAutomaton(states,alphabet, transitions,initialState, finalStates)

    def orNFA(self, nfaA, nfaB):
        initialStateSymbol = self.getSymbol()
        finalStateSymbol = self.getSymbol()
        newtransitions = combine_transitions(nfaA.transitions, nfaB.transitions)
        newtransitions[initialStateSymbol] = {epsilon: set([nfaA.start, nfaB.start])}

        for state in nfaA.accepting:
            newtransitions[state][epsilon] = set([finalStateSymbol])
        for state in nfaB.accepting:
            newtransitions[state][epsilon] = set([finalStateSymbol])
            
        newtransitions[finalStateSymbol] = {}
        newStates = nfaA.states | nfaB.states 
        newStates.add(initialStateSymbol)
        newStates.add(finalStateSymbol)
        newAlphabet = nfaA.alphabet | nfaB.alphabet         
        return FiniteAutomaton(newStates, newAlphabet, newtransitions, initialStateSymbol, set([finalStateSymbol]))
    
    def concatNFA(self, nfaA, nfaB):
        newtransitions = combine_transitions(nfaA.transitions, nfaB.transitions)
        for state in nfaA.accepting:
            newtransitions[state][epsilon] = set([nfaB.start])
        newStates = nfaA.states | nfaB.states
        newAlphabet = nfaA.alphabet | nfaB.alphabet
        return FiniteAutomaton(newStates,newAlphabet, newtransitions,nfaA.start, nfaB.accepting)
    
    def kleenNFA(self, nfaA):
        initialStateSymbol = self.getSymbol()
        finalStateSymbol = self.getSymbol()
        newtransitions = nfaA.transitions
        newtransitions[initialStateSymbol] = {}
        newtransitions[initialStateSymbol][epsilon] = set([nfaA.start, finalStateSymbol])
        newtransitions[finalStateSymbol] = {}
        for state in nfaA.accepting:
            newtransitions[state][epsilon] = set([nfaA.start, finalStateSymbol])
        nfaA.states.add(initialStateSymbol)
        nfaA.states.add(finalStateSymbol)
        return FiniteAutomaton(nfaA.states, nfaA.alphabet, newtransitions, initialStateSymbol, set([finalStateSymbol]))

    def precedence(self,op):
        if op == '|':
            return 1
        if op == '.':
            return 2
        if op == '*' or op =='+' or op =='?':
            return 3
        return 0

    #create nfa form two NFA's and and a single operator
    def applyOp(self, a,  op, b = None):
        if op == '.': return self.concatNFA(a,b) 
        if op == '|': return self.orNFA(a,b)
        if op == '*': return self.kleenNFA(a)
        if op == '+': return self.concatNFA(a,self.kleenNFA(a))
        if op == '?': return self.orNFA(a,self.symbolNFA(epsilon))
    
    def createNfafromPostfix(self):

        # stack to store the NFA's
        nfaStack = []
        
        # stack to store Operators 
        operators = []

        i = 0

        postfix = self.regex
        while i < len(postfix):
            # ignore empty spaces
            if postfix[i] == ' ':
                i += 1
                continue
            
            elif postfix[i] == '(':
                operators.append(postfix[i])
            
            elif postfix[i].isalnum():
                nfaStack.append(self.symbolNFA(postfix[i]))
            
            elif postfix[i] == ')':
                while len(operators) !=0 and operators[-1] != '(':
                    op = operators.pop()
                    if op == "*" or op =="+" or op =="?":
                        nfa1 = nfaStack.pop()
                        nfaStack.append(self.applyOp(nfa1, op))
                    else:
                        nfa2 = nfaStack.pop()
                        nfa1 = nfaStack.pop()
                        nfaStack.append(self.applyOp(nfa1, op, nfa2))
                operators.pop()
            else:
                while (len(operators) != 0 and self.precedence(operators[-1]) >= self.precedence(postfix[i])):
                    op = operators.pop()
                    if op == "*"or op =="+" or op =="?":
                        nfa1 = nfaStack.pop()
                        nfaStack.append(self.applyOp(nfa1, op))
                    else:
                        nfa2 = nfaStack.pop()
                        nfa1 = nfaStack.pop()
                        nfaStack.append(self.applyOp(nfa1, op, nfa2))
                operators.append(postfix[i])
            i +=1
        while len(operators) != 0:
            op = operators.pop()
            if op == "*"or op =="+" or op =="?":
                nfa1 = nfaStack.pop()
                nfaStack.append(self.applyOp(nfa1, op))
            else:
                nfa2 = nfaStack.pop()
                nfa1 = nfaStack.pop()
                nfaStack.append(self.applyOp(nfa1, op, nfa2))   
        return nfaStack[-1]


