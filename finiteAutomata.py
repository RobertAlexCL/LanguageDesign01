"""
The main purpose of this class is to have the structure of a Finite Automaton,
with the respective conversion algorithms,
it can take the form of a Deterministic or Non-Deterministic Finite Automaton.

Author: Roberto Castillo

"""

import graphviz


class FiniteAutomaton():
    def __init__(self, states ,alphabet, transitions, start, accepting):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start = start
        self.accepting = accepting

    # display the automaton's details
    def show(self):
        print("States:")
        print(self.states)
        print("Alphabet:")
        print(self.alphabet)
        print("Transitions:")
        print(self.transitions)
        print("Start State:")
        print(self.start)
        print("Accepting States:")
        print(self.accepting)

    # render the automaton using graphviz
    def render(self, path):
        graph = graphviz.Digraph('Render of Finite Automaton', format= "png")
        for state in self.states:
            if state == self.start:
                graph.node(str(state), color = "red")
            if state in self.accepting:
                graph.node(str(state), shape = 'doublecircle')
            else:
                graph.node(str(state))
        for node in self.transitions.keys():
            for symbol in self.transitions[node].keys():
                next_state = self.transitions[node][symbol]
                for item in next_state:
                    graph.edge(str(node), str(item), label=symbol)
        graph.render(path)
