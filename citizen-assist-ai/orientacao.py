"""Representa uma orientação verificada da base de conhecimento."""

class Orientacao:
    CAMPOS = ('id', 'categoria', 'titulo', 'palavras_chave', 'resposta',
              'documentos', 'onde', 'fonte', 'verificado_em')

    def __init__(self, dados):
        for campo in self.CAMPOS:
            if campo not in dados:
                raise ValueError(f'Campo obrigatório ausente: {campo}')
        if not isinstance(dados['id'], int) or isinstance(dados['id'], bool):
            raise ValueError('id deve ser um número inteiro')
        if any(not isinstance(dados[c], str) or not dados[c].strip()
               for c in ('categoria', 'titulo', 'resposta', 'onde', 'fonte', 'verificado_em')):
            raise ValueError('Campos de texto não podem estar vazios')
        if not isinstance(dados['palavras_chave'], list) or len(dados['palavras_chave']) < 3 or not all(isinstance(x, str) and x.strip() for x in dados['palavras_chave']):
            raise ValueError('Cada orientação precisa de ao menos 3 palavras-chave')
        if not isinstance(dados['documentos'], list) or not all(isinstance(x, str) for x in dados['documentos']):
            raise ValueError('documentos deve ser uma lista de textos')
        if not dados['fonte'].startswith('https://'):
            raise ValueError('Fonte precisa ser URL HTTPS')
        for campo in self.CAMPOS:
            setattr(self, campo, dados[campo])

    def exibir(self):
        print(f'\n>> {self.titulo} [{self.categoria}]')
        print(self.resposta)
        print('Documentos ou requisitos necessários:')
        for item in self.documentos or ['Verifique os requisitos no portal oficial.']:
            print(f'  - {item}')
        print(f'Onde: {self.onde}')
        print(f'Fonte: {self.fonte} (verificado em {self.verificado_em})')
        print('Aviso: este assistente NÃO é um canal oficial.')
