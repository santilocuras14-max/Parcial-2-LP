"""Recursive-descent parser for the transformed arithmetic grammar.
Also demonstrates a small 'matching' helper that peeks tokens and matches expected terminals.
"""
from tokenizer import tokenize, Token

class ParserRD:
    def __init__(self, tokens):
        # tokens: list of Token
        self.tokens = tokens + [Token('$','$')]
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def match(self, expected_type=None, expected_val=None):
        tok = self.peek()
        if expected_type and tok.type != expected_type:
            raise SyntaxError(f'Expected token type {expected_type} but got {tok} at pos {self.pos}')
        if expected_val and tok.value != expected_val:
            raise SyntaxError(f'Expected token value {expected_val} but got {tok.value} at pos {self.pos}')
        self.pos += 1
        return tok

    # Grammar (transformed):
    # E -> T E'
    # E' -> + T E' | epsilon
    # T -> F T'
    # T' -> * F T' | epsilon
    # F -> ( E ) | id

    def parse_E(self):
        self.parse_T()
        self.parse_E_prime()

    def parse_E_prime(self):
        tok = self.peek()
        if tok.value == '+':
            self.match(expected_val='+')
            self.parse_T()
            self.parse_E_prime()
        else:
            # epsilon
            return

    def parse_T(self):
        self.parse_F()
        self.parse_T_prime()

    def parse_T_prime(self):
        tok = self.peek()
        if tok.value == '*':
            self.match(expected_val='*')
            self.parse_F()
            self.parse_T_prime()
        else:
            return

    def parse_F(self):
        tok = self.peek()
        if tok.value == '(':
            self.match(expected_val='(')
            self.parse_E()
            self.match(expected_val=')')
        elif tok.type == 'id':
            self.match(expected_type='id')
        else:
            raise SyntaxError(f'Unexpected token in F: {tok}')

def test_inputs():
    from tokenizer import tokenize
    tests = ['id + id * id', '( id + id ) * id', 'id + * id']
    for s in tests:
        toks = list(tokenize(s))
        p = ParserRD(toks)
        print('\nInput:', s)
        try:
            p.parse_E()
            if p.peek().type == '$':
                print('Accepted')
            else:
                print('Not fully consumed, pos', p.pos)
        except Exception as e:
            print('Error:', e)

if __name__ == '__main__':
    test_inputs()
