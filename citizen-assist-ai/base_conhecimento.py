"""Carregamento, navegação e busca textual por regras."""
import json
import re
import unicodedata
from pathlib import Path
from orientacao import Orientacao


def normalizar(texto):
    """Remove acentos e pontuação, converte para minúsculas e isola palavras."""
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(ch for ch in texto if unicodedata.category(ch) != 'Mn')
    texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
    return ' ' + ' '.join(texto.split()) + ' '


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []

    def carregar(self):
        """Não encerra o programa se o arquivo estiver ausente ou inválido."""
        try:
            with self.caminho.open(encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError('O JSON precisa conter uma lista')
            novas = [Orientacao(item) for item in dados]
            ids = [item.id for item in novas]
            if len(ids) != len(set(ids)):
                raise ValueError('Há IDs repetidos')
            self.orientacoes = novas
            return True
        except (OSError, ValueError, TypeError, KeyError) as erro:
            self.orientacoes = []
            print(f'Aviso: não foi possível carregar a base: {erro}')
            return False

    def categorias(self):
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        pergunta_norm = normalizar(pergunta)
        titulo_norm = normalizar(orientacao.titulo)
        pontos = 0
        for chave in orientacao.palavras_chave:
            chave_norm = normalizar(chave).strip()
            if chave_norm and f' {chave_norm} ' in pergunta_norm:
                pontos += 3
        # Palavras distintas evitam pontos extras pela repetição da mesma palavra.
        for palavra in set(pergunta_norm.split()):
            if len(palavra) >= 4 and f' {palavra} ' in titulo_norm:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        """Lista de tuplas (pontuação, Orientacao) em ordem decrescente."""
        resultados = [(self.pontuar(pergunta, o), o) for o in self.orientacoes]
        return sorted(resultados, key=lambda par: (-par[0], par[1].id))
