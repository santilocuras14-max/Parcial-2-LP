"""CYK parser for a grammar in CNF. For simplicity we define a CNF version
of the arithmetic grammar and then test CYK on sample inputs.
CNF grammar used (example):
E -> (not directly in CNF) so we prepare a small CNF set for expressions using intermediate non-terminals.
"""
from collections import defaultdict

# Example CNF grammar for simple expressions over tokens id, +, *, (, )
# We'll encode productions as: A -> BC  or A -> terminal
CNF = {
    'E': [['T','E_PRIME']],
    'E_PRIME': [['PLUS_T','E_PRIME'], []],  # empty will not be used in CNF; we will use an equivalent CNF below
}

# For CYK we must provide pure CNF. Construct a small CNF for expressions like id + id * id
# We'll use:
# S -> EXPR
# EXPR -> TERM EXPR2
# EXPR2 -> PLUS TERM | PLUS TERM EXPR2  (not CNF) -> transform using intermediate
# For brevity we provide a small illustrative CNF for the language id (+ id | * id )* which suffices for short strings

GRAM = [
    ('S','EXPR'),
    ('EXPR','TERM EXPR2'),
    ('EXPR2','PLUS_TERM'),
    ('EXPR2','EPS'),  # we'll handle EPS specially
    ('PLUS_TERM','PLUS TERM'),
    ('TERM','FACTOR TERM2'),
    ('TERM2','MUL_FACTOR'),
    ('TERM2','EPS'),
    ('MUL_FACTOR','MUL FACTOR'),
    ('FACTOR','LPAREN_EXPR'),
    ('FACTOR','id'),
    ('LPAREN_EXPR','LP EXPR_RP'),
    ('EXPR_RP','EXPR RP')
]

# Convert GRAM to useful maps
def build_maps():
    bin_rules = defaultdict(list)
    term_rules = defaultdict(list)
    eps = set()
    for lhs, rhs in GRAM:
        if rhs == 'EPS':
            eps.add(lhs)
            continue
        parts = rhs.split()
        if len(parts) == 1:
            term_rules[parts[0]].append(lhs)
        elif len(parts) == 2:
            bin_rules[(parts[0],parts[1])].append(lhs)
    return bin_rules, term_rules, eps

def cyk_parse(tokens):
    # tokens: list of terminal strings ['id','+','id',...]
    n = len(tokens)
    bin_rules, term_rules, eps = build_maps()
    P = [ [set() for j in range(n)] for i in range(n) ]
    # initialize
    for i,t in enumerate(tokens):
        if t in term_rules:
            P[i][i].update(term_rules[t])
    # CYK
    for l in range(2, n+1):
        for i in range(0, n-l+1):
            j = i + l - 1
            for k in range(i, j):
                left = P[i][k]
                right = P[k+1][j]
                for A in list(left):
                    for B in list(right):
                        for lhs in bin_rules.get((A,B), []):
                            P[i][j].add(lhs)
    # check if S in P[0][n-1]
    if n==0:
        return False
    return 'S' in P[0][n-1]

if __name__ == '__main__':
    tests = [
        ['id','+','id','*','id'],
        ['(','id','+','id',')','*','id']
    ]
    for t in tests:
        print('Tokens:', t, '->', cyk_parse(t))
