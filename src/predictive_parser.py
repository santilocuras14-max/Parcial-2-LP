"""Parser predictivo (LL(1)) para la gramática aritmética transformada.
Se implementa una tabla de parseo manualmente construida para la
gramática transformada en transform_ll1.py
"""
from tokenizer import Token, tokenize
from transform_ll1 import transformed_grammar as getG

def build_table():
    # Manual table for the transformed grammar (terminals: id, '(', ')', '+', '*', '$')
    # Non-terminals: E, E_PRIME, T, T_PRIME, F
    table = {}
    # For demonstration, we fill entries based on FIRST/FOLLOW analysis.
    table['E'] = {
        'id': ['T','E_PRIME'],
        '(' : ['T','E_PRIME']
    }
    table['E_PRIME'] = {
        '+': ['+','T','E_PRIME'],
        ')': [],
        '$': []
    }
    table['T'] = {
        'id': ['F','T_PRIME'],
        '(' : ['F','T_PRIME']
    }
    table['T_PRIME'] = {
        '*': ['*','F','T_PRIME'],
        '+': [],
        ')': [],
        '$': []
    }
    table['F'] = {
        'id': ['id'],
        '(' : ['(','E',')']
    }
    return table

def predict_parse(tokens):
    table = build_table()
    stack = ['$', 'E']  # stack bottom on left
    tokens = [t for t in tokens if t.type!='SKIP']
    input_stream = [tok.type if tok.type in ('id','(',' )','+','*') else tok.type for tok in tokens]
    # Better to map token types to terminals used in table:
    mapped = []
    for tok in tokens:
        if tok.type=='id': mapped.append('id')
        elif tok.value in ('+', '*', '(', ')'): mapped.append(tok.value)
        elif tok.type=='literal': mapped.append('id')  # treat literal as id for arithmetic tests
        else:
            mapped.append(tok.value)
    mapped.append('$')
    ip = 0

    while stack:
        top = stack.pop()
        cur = mapped[ip]
        if top == '$' and cur == '$':
            print('Input accepted.')
            return True
        if top in ('id','+','*','(',')'):
            if top == cur:
                ip += 1
                continue
            else:
                print(f'Mismatch terminal: stack top {top} vs input {cur}'); return False
        else:
            # nonterminal
            entry = table.get(top, {}).get(cur, None)
            if entry is None:
                print(f'No table entry for nonterminal {top} and token {cur}'); return False
            if entry==[]:
                # epsilon: do nothing
                continue
            else:
                # push reversed
                for sym in reversed(entry):
                    stack.append(sym)
    return False

if __name__ == '__main__':
    # Quick test inputs
    tests = [
        "id + id * id",
        "( id + id ) * id",
        "id + * id"
    ]
    from tokenizer import tokenize
    for s in tests:
        toks = list(tokenize(s))
        print('Input:', s)
        ok = predict_parse(toks)
        print('OK?', ok)
        print('---')
