"""Transformations to make a grammar LL(1): remove left recursion for the example grammar:
Original grammar:
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
We produce an equivalent grammar without left recursion.
"""

def transformed_grammar():
    # E -> T E'
    # E' -> + T E' | epsilon
    # T -> F T'
    # T' -> * F T' | epsilon
    G = {
        'E': [['T','E_PRIME']],
        'E_PRIME': [['+','T','E_PRIME'], []],
        'T': [['F','T_PRIME']],
        'T_PRIME': [['*','F','T_PRIME'], []],
        'F': [['(','E',')'], ['id']]
    }
    return G

if __name__ == '__main__':
    import pprint
    pprint.pprint(transformed_grammar())
