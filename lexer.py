# Guilherme Daudt
# lexer.py – DFA que converte a string-fonte em tokens da gramática

from enum import Enum, auto
import re
from typing import List, Tuple

# ----------- 1. Tipos de token ------------------------------------------------
class TokenType(Enum):
    LPAREN      = auto()          # (
    RPAREN      = auto()          # )
    CONST       = auto()          # true | false
    PROP        = auto()          # [0-9][0-9a-z]*
    UNARY_OP    = auto()          # \neg
    BINARY_OP   = auto()          # \wedge \vee \rightarrow \leftrightarrow
    EOF         = auto()          # fim de entrada

Token = Tuple[str, TokenType]

# ----------- 2. Expressões regulares finais -----------------------------------
_RE_PROP  = re.compile(r'[0-9][0-9a-z]*')
_RE_CONST = re.compile(r'(true|false)')

_OPERATORS = {
    r'\neg'            : TokenType.UNARY_OP,
    r'\wedge'          : TokenType.BINARY_OP,
    r'\vee'            : TokenType.BINARY_OP,
    r'\rightarrow'     : TokenType.BINARY_OP,
    r'\leftrightarrow' : TokenType.BINARY_OP,
}

# ----------- 3. Scanner (máquina de estados finitos) --------------------------
def scan(src: str) -> List[Token]:
    """Retorna a lista de tokens reconhecida em *src* ou lança ValueError."""
    tokens: List[Token] = []
    i, n = 0, len(src)

    while i < n:
        ch = src[i]

        if ch.isspace():                       # ignora espaços
            i += 1
            continue

        if ch == '(':
            tokens.append(('(', TokenType.LPAREN)); i += 1; continue
        if ch == ')':
            tokens.append((')', TokenType.RPAREN)); i += 1; continue

        if ch in ('t', 'f'):                   # constantes
            m = _RE_CONST.match(src, i)
            if m:
                lex = m.group(0)
                tokens.append((lex, TokenType.CONST))
                i += len(lex); continue

        if ch.isdigit():                       # proposições
            m = _RE_PROP.match(src, i)
            if m:
                lex = m.group(0)
                tokens.append((lex, TokenType.PROP))
                i += len(lex); continue

        if ch == '\\':                         # operadores
            for lit, ttype in _OPERATORS.items():
                if src.startswith(lit, i):
                    tokens.append((lit, ttype))
                    i += len(lit)
                    break
            else:
                raise ValueError(f'lexical error at pos {i}')
            continue

        raise ValueError(f'lexical error at pos {i}')

    tokens.append(('', TokenType.EOF))
    return tokens
