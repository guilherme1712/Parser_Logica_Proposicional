# Guilherme Daudt - Matheus Gabriel Pereira Nogueira
# parser.py – Ponto de entrada que lê o arquivo e imprime valida/invalida

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0
        self.stack = []
        self.table = self._create_parse_table()

    def _create_parse_table(self):
        """
        cria a tabela de análise sintática para o parser LL(1)
        """
        table = {
            # inicial
            ('S', 'CONSTANTE'): ['CONSTANTE'],
            ('S', 'PROPOSICAO'): ['PROPOSICAO'],
            ('S', 'ABREPAREN'): ['X'],  # depende do proximo token

            # intermediario?
            ('X', 'OPERADORUNARIO'): ['U'],
            ('X', 'OPERADORBINARIO'): ['B'],

            # unario e binarie
            ('U', 'ABREPAREN'): ['ABREPAREN', 'OPERADORUNARIO', 'S', 'FECHAPAREN'],
            ('B', 'ABREPAREN'): ['ABREPAREN', 'OPERADORBINARIO', 'S', 'S', 'FECHAPAREN']
        }
        return table

    def _current_token(self):
        """retorna o token atual"""
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None

    def _next_token(self):
        """avanca para o proximo token e retorna"""
        if self.current_index + 1 < len(self.tokens):
            return self.tokens[self.current_index + 1]
        return None

    def _next(self):
        """avanca o indice do token atual"""
        self.current_index += 1

    def validate(self):
        """
        valida a expressao usando um parser LL(1) com pilha
        retorna True se a expressao for valida, False caso contrario
        """
        # inicia pilha com uma expressao
        self.stack = ['$', 'S']  # $ = fim da pilha

        while self.stack[-1] != '$':
            top = self.stack[-1]  # topo
            token = self._current_token()

            if token is None:
                return False  # fim dos tokens

            if top == 'X':
                # decidir entre U e B
                self.stack.pop()
                next_token = self._next_token()
                if next_token and next_token.type == 'OPERADORUNARIO':
                    production = self.table.get(('X', 'OPERADORUNARIO'), [])
                    for symbol in reversed(production):
                        self.stack.append(symbol)
                elif next_token and next_token.type == 'OPERADORBINARIO':
                    production = self.table.get(('X', 'OPERADORBINARIO'), [])
                    for symbol in reversed(production):
                        self.stack.append(symbol)
                else:
                    return False
                continue

            # se topo for um terminal, verifica se coincide com o token atual
            if top in ['CONSTANTE', 'PROPOSICAO', 'ABREPAREN', 'FECHAPAREN', 'OPERADORUNARIO', 'OPERADORBINARIO']:
                if top == token.type:
                    self.stack.pop()
                    self._next()
                else:
                    return False
            else:
                # topo é um nao-terminal
                production = self.table.get((top, token.type), None)

                if production is None:
                    return False

                # remove nao terminal
                self.stack.pop()

                # adiciona producao invertida na pilha
                for symbol in reversed(production):
                    self.stack.append(symbol)

        # verifica se foi tudo
        return self.current_index == len(self.tokens)
