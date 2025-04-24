# Guilherme Daudt – Matheus Gabriel Pereira Nogueira
# main.py – laço principal iterativo (sem recursão)

import sys
from lexer import scan
from parser import Parser   # Parser iterativo com pilha LL(1)

def is_valid(expr: str) -> bool:
    """Wrapper que liga o scanner ao parser iterativo."""
    try:
        tokens = scan(expr)
        return Parser(tokens).validate()
    except ValueError:       # erro léxico ou sintático
        return False

def main() -> None:
    if len(sys.argv) != 2:
        sys.stderr.write('Uso: python main.py arquivo.txt\n')
        sys.exit(1)

    # —— lê arquivo
    try:
        with open(sys.argv[1], encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        sys.stderr.write(f'Erro ao ler arquivo: {exc}\n')
        sys.exit(1)

    if not lines:
        return

    # —— interpreta primeira linha
    try:
        n = int(lines[0].strip())
    except ValueError:
        sys.stderr.write('Primeira linha deve conter um inteiro.\n')
        sys.exit(1)

    exprs = lines[1:n + 1]

    # —— valida cada expressão
    for expr in exprs:
        print('valida' if is_valid(expr) else 'invalida')

    # —— se o arquivo prometeu mais do que entregou
    for _ in range(n - len(exprs)):
        print('invalida')

if __name__ == '__main__':
    main()
