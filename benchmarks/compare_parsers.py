"""Compare performance between predictive parser and CYK for several input sizes.
This is a simple micro-benchmark using time.perf_counter.">"""
from time import perf_counter
from src.predictive_parser import predict_parse
from src.tokenizer import tokenize
import importlib, sys, os

# Adjust path to import local src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predictive_parser import predict_parse as predict_parse_local
from src.cyk import cyk_parse
from src.tokenizer import tokenize

def tokens_to_term_list(token_objs):
    mapped = []
    for tok in token_objs:
        if tok.type=='id': mapped.append('id')
        elif tok.value in ('+','*','(',')'): mapped.append(tok.value)
        else: mapped.append(tok.value)
    return mapped

def bench_once(parser_fn, input_str, use_token_objs=False):
    if use_token_objs:
        toks = list(tokenize(input_str))
    else:
        toks = input_str
    t0 = perf_counter()
    res = parser_fn(toks)
    t1 = perf_counter()
    return t1-t0, res

def main():
    seq = 'id + id * id + id * id + id * id'
    inputs = [ ' '.join(['id']*n) for n in [5,10,20,40] ]
    print('Micro-benchmark: predictive (approx) vs CYK')
    for s in inputs:
        tok_objs = list(tokenize(s))
        term_list = tokens_to_term_list(tok_objs)
        # predictive: call predict_parse using token objects (it expects token objs)
        import src.predictive_parser as pp
        t_pp, res_pp = bench_once(pp.predict_parse, tok_objs, use_token_objs=True)
        # cyk: call cyk_parse with term_list
        import src.cyk as cykmod
        t_cyk, res_cyk = bench_once(cykmod.cyk_parse, term_list, use_token_objs=False)
        print(f'Input length {len(term_list):3d}: predictive {t_pp:.6f}s, cyk {t_cyk:.6f}s, predictive_ok={res_pp}, cyk_ok={res_cyk}')

if __name__ == '__main__':
    main()
