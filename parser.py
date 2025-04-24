# Guilherme Daudt
# parser.py – Parser LL(1) + função valida()

from typing import List
from lexer import TokenType, Token, scan

class Parser:
    """Parser recursivo-descendente LL(1) para a gramática de fórmulas."""

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos    = 0

    # ---------- helpers -------------------------------------------------------
    def _look(self) -> TokenType:
        return self.tokens[self.pos][1]

    def _eat(self, expected: TokenType) -> None:
        if self._look() == expected:
            self.pos += 1
        else:
            raise ValueError('syntax')

    # ---------- regras --------------------------------------------------------
    def _formula(self) -> None:
        t = self._look()

        if t is TokenType.CONST:
            self._eat(TokenType.CONST)

        elif t is TokenType.PROP:
            self._eat(TokenType.PROP)

        elif t is TokenType.LPAREN:
            self._eat(TokenType.LPAREN)
            op = self._look()

            if op is TokenType.UNARY_OP:              # ( UNARY_OP FORMULA )
                self._eat(TokenType.UNARY_OP)
                self._formula()
                self._eat(TokenType.RPAREN)

            elif op is TokenType.BINARY_OP:           # ( BINARY_OP FORMULA FORMULA )
                self._eat(TokenType.BINARY_OP)
                self._formula()
                self._formula()
                self._eat(TokenType.RPAREN)

            else:
                raise ValueError('syntax')
        else:
            raise ValueError('syntax')

    def parse(self) -> None:
        self._formula()
        if self._look() is not TokenType.EOF:         # tokens sobrando
            raise ValueError('syntax')

# ---------- API externa: função valida ----------------------------------------
def valida(expr: str) -> bool:
    """Devolve True se a expressão *expr* é léxica + sintaticamente correta."""
    try:
        tokens = scan(expr)
        Parser(tokens).parse()
        return True
    except ValueError:
        return False
