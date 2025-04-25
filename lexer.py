# Guilherme Daudt – Matheus Gabriel Pereira Nogueira
# lexer.py – scanner DFA iterativo (sem recursão)

from dataclasses import dataclass
from typing import List

# -------- 1. Estrutura de token que o parser espera --------------------------
@dataclass
class Token:
    lexeme: str   # texto original
    type: str     # classe: CONSTANTE, PROPOSICAO, ABREPAREN, ...

# -------- 2. Literais de operador --------------------------------------------
_BINARY = {
    r'\wedge',
    r'\vee',
    r'\rightarrow',
    r'\leftrightarrow',
}

# -------- 3. DFA iterativo ----------------------------------------------------
def scan(src: str) -> List[Token]:
    """
    Percorre a string *src* caractere a caractere e devolve
    uma lista de Token(lexeme, type). Lança ValueError em
    qualquer caractere inesperado.
    """
    tokens: List[Token] = []
    i, n = 0, len(src)

    while i < n:
        ch = src[i]

        # —— ignora espaços / quebras de linha
        if ch.isspace():
            i += 1
            continue

        # —— parênteses
        if ch == '(':
            tokens.append(Token('(', 'ABREPAREN'))
            i += 1
            continue
        if ch == ')':
            tokens.append(Token(')', 'FECHAPAREN'))
            i += 1
            continue

        # —— constantes true | false (sem regex)
        if src.startswith('true', i):
            tokens.append(Token('true', 'CONSTANTE'))
            i += 4
            continue
        if src.startswith('false', i):
            tokens.append(Token('false', 'CONSTANTE'))
            i += 5
            continue

        # —— proposições: [0-9][0-9a-z]* (sem regex)
        if ch.isdigit():
            start = i
            i += 1
            # aceita dígitos ou letras minúsculas
            while i < n and (src[i].isdigit() or ('a' <= src[i] <= 'z')):
                i += 1
            lex = src[start:i]
            tokens.append(Token(lex, 'PROPOSICAO'))
            continue

        # —— operadores iniciados por '\'
        if ch == '\\':
            # unário?
            if src.startswith(r'\neg', i):
                tokens.append(Token(r'\neg', 'OPERADORUNARIO'))
                i += 4
                continue
            # binário? (tenta cada literal)
            for lit in _BINARY:
                if src.startswith(lit, i):
                    tokens.append(Token(lit, 'OPERADORBINARIO'))
                    i += len(lit)
                    break
            else:
                raise ValueError(f'lexical error at pos {i}')
            continue

        # —— qualquer outro símbolo é erro
        raise ValueError(f'lexical error at pos {i}')

    return tokens
