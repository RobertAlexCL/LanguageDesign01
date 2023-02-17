"""
Here are the most important generic functions and variables of the project, 
more will be added as the project progresses.

Author: Roberto Castillo

"""

epsilon = "ε"


# Combine two transition functions into a single function
def combine_transitions(transitions1, transitions2):
    combined_transitions = {}
    for key in transitions1:
        combined_transitions[key] = transitions1[key]
    for key in transitions2:
        combined_transitions[key] = transitions2[key]
    return combined_transitions
