"""Computes FIRST and FOLLOW sets for a context-free grammar represented as dict.
Grammar representation:
G = { 'S': [['A','b'], ['c'], []], ... }
Empty production is represented as empty list [] (epsilon).
"""
from collections import defaultdict

def compute_first(G):
    FIRST = {A:set() for A in G}
    changed = True
    while changed:
        changed = False
        for A, prods in G.items():
            for prod in prods:
                if not prod: # epsilon
                    if 'epsilon' not in FIRST[A]:
                        FIRST[A].add('epsilon'); changed = True
                    continue
                for X in prod:
                    if X not in G: # terminal
                        if X not in FIRST[A]:
                            FIRST[A].add(X); changed = True
                        break
                    else:
                        # X is nonterminal
                        before = len(FIRST[A])
                        FIRST[A].update(x for x in FIRST[X] if x!='epsilon')
                        if 'epsilon' in FIRST[X]:
                            # continue to next symbol
                            pass
                        else:
                            break
                        if len(FIRST[A])!=before: changed=True
                else:
                    # all symbols had epsilon
                    if 'epsilon' not in FIRST[A]:
                        FIRST[A].add('epsilon'); changed=True
    return FIRST

def compute_follow(G, start):
    FIRST = compute_first(G)
    FOLLOW = {A:set() for A in G}
    FOLLOW[start].add('$')
    changed = True
    while changed:
        changed = False
        for A, prods in G.items():
            for prod in prods:
                trailer = set(FOLLOW[A])
                for X in reversed(prod):
                    if X in G:
                        before = len(FOLLOW[X])
                        FOLLOW[X].update(trailer)
                        if 'epsilon' in FIRST[X]:
                            trailer = trailer.union(x for x in FIRST[X] if x!='epsilon')
                        else:
                            trailer = set(x for x in FIRST[X] if x!='epsilon')
                        if len(FOLLOW[X])!=before:
                            changed = True
                    else:
                        trailer = set([X])
    return FIRST, FOLLOW

if __name__ == '__main__':
    from transform_ll1 import transformed_grammar
    G = transformed_grammar()
    FIRST, FOLLOW = compute_follow(G, 'E')
    print('FIRST:')
    for k,v in FIRST.items(): print(k, v)
    print('\nFOLLOW:')
    for k,v in FOLLOW.items(): print(k, v)
