"""Compute FIRST, FOLLOW and Prediction sets for a given grammar (dictionary form).
Also builds a simple LL(1) prediction table for nonterminals and terminals.
"""
from collections import defaultdict

def compute_first(G):
    FIRST = {A:set() for A in G}
    changed = True
    while changed:
        changed = False
        for A, prods in G.items():
            for prod in prods:
                if not prod:
                    if 'epsilon' not in FIRST[A]:
                        FIRST[A].add('epsilon'); changed = True
                    continue
                for X in prod:
                    if X not in G:
                        if X not in FIRST[A]:
                            FIRST[A].add(X); changed = True
                        break
                    else:
                        before = len(FIRST[A])
                        FIRST[A].update(x for x in FIRST[X] if x!='epsilon')
                        if 'epsilon' in FIRST[X]:
                            continue
                        else:
                            break
                        if len(FIRST[A])!=before: changed=True
                else:
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

def build_prediction_table(G, start):
    FIRST = compute_first(G)
    FIRST, FOLLOW = compute_follow(G, start)
    table = defaultdict(dict)
    for A, prods in G.items():
        for prod in prods:
            # compute FIRST(prod)
            first_prod = set()
            if not prod:
                first_prod.add('epsilon')
            else:
                for X in prod:
                    if X not in G:
                        first_prod.add(X); break
                    else:
                        first_prod.update(x for x in FIRST[X] if x!='epsilon')
                        if 'epsilon' in FIRST[X]:
                            continue
                        else:
                            break
                else:
                    first_prod.add('epsilon')
            for terminal in (first_prod - set(['epsilon'])):
                table[A][terminal] = prod
            if 'epsilon' in first_prod:
                for b in FOLLOW[A]:
                    table[A][b] = prod
    return FIRST, FOLLOW, table

if __name__ == '__main__':
    # use transformed arithmetic grammar
    G = {
        'E': [['T','E_PRIME']],
        'E_PRIME': [['+','T','E_PRIME'], []],
        'T': [['F','T_PRIME']],
        'T_PRIME': [['*','F','T_PRIME'], []],
        'F': [['(','E',')'], ['id']]
    }
    FIRST, FOLLOW, TABLE = build_prediction_table(G, 'E')
    print('FIRST:')
    for k,v in FIRST.items(): print(k, v)
    print('\nFOLLOW:')
    for k,v in FOLLOW.items(): print(k, v)
    print('\nPrediction Table:')
    for A, row in TABLE.items():
        print(A)
        for term, prod in row.items():
            print('  ', term, '->', prod)
