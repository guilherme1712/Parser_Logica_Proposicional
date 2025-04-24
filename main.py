# Guilherme Daudt
# main.py – Ponto de entrada que lê o arquivo e imprime valida/invalida

import sys
from parser import valida

def main() -> None:
    if len(sys.argv) != 2:
        sys.stderr.write('Uso: python main.py arquivo.txt\n')
        sys.exit(1)

    try:
        with open(sys.argv[1], encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        sys.stderr.write(f'Erro ao ler arquivo: {exc}\n')
        sys.exit(1)

    if not lines:
        sys.exit(0)                                 # nada a processar

    try:
        n = int(lines[0].strip())
    except ValueError:
        sys.stderr.write('Primeira linha deve conter um inteiro.\n')
        sys.exit(1)

    exprs = lines[1:n+1]                            # pode faltar alguma
    for expr in exprs:
        print('valida' if valida(expr) else 'invalida')

    # linhas prometidas mas ausentes ⇒ inválidas
    for _ in range(n - len(exprs)):
        print('invalida')

if __name__ == '__main__':
    main()
