
import re
from dataclasses import dataclass
from typing import List, Tuple

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(?:\.\d+)?'),
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
    ('STRING',   r"'[^']*'|\"[^\"]*\"") ,
    ('EQ',       r'='),
    ('COMMA',    r','),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('SEMICOL',  r';'),
    ('STAR',     r'\*'),
    ('SKIP',     r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]

master_re = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC))

@dataclass
class Token:
    type: str
    value: str

def tokenize(s: str):
    for mo in master_re.finditer(s):
        kind = mo.lastgroup
        val = mo.group()
        if kind == 'NUMBER':
            yield Token('literal', val)
        elif kind == 'STRING':
            yield Token('literal', val)
        elif kind == 'ID':
            ut = val.upper()
            if ut in ('SELECT','INSERT','INTO','UPDATE','DELETE','FROM','WHERE','SET','VALUES'):
                yield Token(ut, ut)
            else:
                yield Token('id', val)
        elif kind == 'EQ':
            yield Token('=', '=')
        elif kind == 'COMMA':
            yield Token(',', ',')
        elif kind == 'LPAREN':
            yield Token('(', '(')
        elif kind == 'RPAREN':
            yield Token(')', ')')
        elif kind == 'SEMICOL':
            yield Token(';', ';')
        elif kind == 'STAR':
            yield Token('*', '*')
        elif kind == 'SKIP':
            continue
        else:
            yield Token('MISMATCH', val)

if __name__ == '__main__':
    s = "SELECT name, age FROM users WHERE id = 10;"
    print(list(tokenize(s)))
