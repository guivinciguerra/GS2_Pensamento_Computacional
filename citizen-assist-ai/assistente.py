"""Interação no terminal, proteção de dados e indicadores."""
import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path


CAMPOS_CSV = ['data', 'origem', 'pergunta', 'id_orientacao', 'encontrou',
              'ajudou', 'tentativas', 'tempo_segundos']


def contem_dados_pessoais(texto):
    """Critério obrigatório do enunciado: @ ou oito algarismos no total."""
    return '@' in texto or len(re.findall(r'\d', texto)) >= 8


class Assistente:
    def __init__(self, nome, base, pasta_dados='data'):
        self.nome = nome
        self.base = base
        self.pasta = Path(pasta_dados)
        self.pasta.mkdir(parents=True, exist_ok=True)
        self.arquivo_historico = self.pasta / 'historico.json'
        self.arquivo_avaliacoes = self.pasta / 'avaliacoes.json'
        self.historico = self._ler_lista(self.arquivo_historico)
        self.avaliacoes = self._ler_lista(self.arquivo_avaliacoes)

    @staticmethod
    def _ler_lista(caminho):
        try:
            with caminho.open(encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, list):
                return dados
            print(f'Aviso: {caminho} não contém lista; começando sem registros.')
        except FileNotFoundError:
            pass
        except (OSError, ValueError, TypeError) as erro:
            print(f'Aviso: não foi possível ler {caminho}: {erro}')
        return []

    @staticmethod
    def _salvar_lista(caminho, dados):
        try:
            temporario = caminho.with_suffix('.tmp')
            with temporario.open('w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
            temporario.replace(caminho)
            return True
        except OSError as erro:
            print(f'Erro ao salvar {caminho}: {erro}')
            return False

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou,
                  tentativas, tempo_segundos):
        if contem_dados_pessoais(pergunta):
            return False
        registro = {
            'data': datetime.now().astimezone().isoformat(timespec='seconds'),
            'origem': origem,
            'pergunta': pergunta,
            'id_orientacao': id_orientacao,
            'encontrou': bool(encontrou),
            'ajudou': bool(ajudou),
            'tentativas': tentativas,
            'tempo_segundos': round(tempo_segundos, 1)
        }
        self.historico.append(registro)
        return self._salvar_lista(self.arquivo_historico, self.historico)

    @staticmethod
    def _perguntar_sn(mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ('s', 'n'):
                return resposta == 's'
            print('Entrada inválida. Digite s ou n.')

    def perguntar(self):
        print('\nDigite sua dúvida em texto livre. Digite 0 para voltar.')
        inicio = time.time()
        tentativas = 0
        while True:
            pergunta = input('Sua dúvida: ').strip()
            if pergunta == '0':
                return
            if not pergunta:
                print('Escreva uma dúvida ou digite 0 para voltar.')
                continue
            if contem_dados_pessoais(pergunta):
                print('Atenção: não digite CPF, telefone ou e-mail. Reescreva sem dados pessoais.')
                continue
            tentativas += 1
            resultados = self.base.buscar(pergunta)
            melhor_pontuacao = resultados[0][0] if resultados else 0
            if melhor_pontuacao < 3:
                print('Não encontrei orientação confiável. Tente outras palavras ou navegue pelas categorias.')
                if self._perguntar_sn('Deseja tentar outra pergunta? (s/n): '):
                    continue
                self.registrar('pergunta', pergunta, None, False, False,
                              tentativas, time.time() - inicio)
                return
            pontos, orientacao = resultados[0]
            confianca = 'ALTA' if pontos >= 6 else 'MÉDIA'
            print(f'\nConfiança da resposta: {confianca} ({pontos} pontos)')
            orientacao.exibir()
            alternativas = [(p, o) for p, o in resultados[1:] if p >= 3][:2]
            if alternativas:
                print('\nOutras orientações possivelmente úteis:')
                for p, o in alternativas:
                    print(f'  - {o.titulo} ({p} pontos)')
            ajudou = self._perguntar_sn('\nEssa orientação respondeu sua dúvida? (s/n): ')
            self.registrar('pergunta', pergunta, orientacao.id, True, ajudou,
                          tentativas, time.time() - inicio)
            return

    def navegar(self):
        while True:
            categorias = self.base.categorias()
            if not categorias:
                print('Nenhuma categoria disponível. Confira a base de conhecimento.')
                return
            print('\nCATEGORIAS')
            for n, categoria in enumerate(categorias, 1):
                print(f'{n}. {categoria}')
            print('0. Voltar')
            escolha = input('Escolha uma categoria: ').strip()
            if escolha == '0':
                return
            if not escolha.isdigit() or int(escolha) not in range(1, len(categorias) + 1):
                print('Opção inválida. Tente novamente.')
                continue
            categoria = categorias[int(escolha) - 1]
            orientacoes = self.base.por_categoria(categoria)
            while True:
                print(f'\n{categoria.upper()}')
                for n, orientacao in enumerate(orientacoes, 1):
                    print(f'{n}. {orientacao.titulo}')
                print('0. Voltar')
                escolha_item = input('Escolha uma orientação: ').strip()
                if escolha_item == '0':
                    break
                if not escolha_item.isdigit() or int(escolha_item) not in range(1, len(orientacoes) + 1):
                    print('Opção inválida. Tente novamente.')
                    continue
                inicio = time.time()
                orientacao = orientacoes[int(escolha_item) - 1]
                orientacao.exibir()
                ajudou = self._perguntar_sn('\nEssa orientação respondeu sua dúvida? (s/n): ')
                # Não há texto livre na navegação; apenas o título público da orientação.
                self.registrar('categoria', orientacao.titulo, orientacao.id,
                              True, ajudou, 1, time.time() - inicio)

    def indicadores(self):
        total = len(self.historico)
        encontrados = sum(bool(r.get('encontrou')) for r in self.historico)
        ajudaram = sum(bool(r.get('ajudou')) for r in self.historico)
        tempos = [float(r.get('tempo_segundos', 0)) for r in self.historico]
        tentativas = [int(r.get('tentativas', 0)) for r in self.historico]
        notas = [n for n in self.avaliacoes if isinstance(n, int) and 1 <= n <= 5]
        sem_solucao = [r.get('pergunta', '') for r in self.historico if not r.get('encontrou')]
        print('\nINDICADORES')
        print(f'Atendimentos: {total}')
        print(f'Resposta encontrada: {100 * encontrados / total:.1f}%' if total else 'Resposta encontrada: sem dados')
        print(f'Taxa de acerto (ajudou): {100 * ajudaram / total:.1f}%' if total else 'Taxa de acerto: sem dados')
        print(f'Tempo médio para encontrar/encerrar: {sum(tempos) / total:.1f} s' if total else 'Tempo médio: sem dados')
        print(f'Tentativas por atendimento: {sum(tentativas) / total:.1f}' if total else 'Tentativas por atendimento: sem dados')
        print(f'Facilidade de uso: {sum(notas) / len(notas):.1f}/5' if notas else 'Facilidade de uso: sem avaliações')
        print('Dúvidas sem solução:')
        for pergunta in sem_solucao:
            print(f'  - {pergunta}')
        if not sem_solucao:
            print('  Nenhuma registrada.')
        return {'total': total, 'encontrados': encontrados, 'ajudaram': ajudaram,
                'sem_solucao': sem_solucao}

    def exportar_csv(self):
        caminho = self.pasta / 'atendimentos.csv'
        try:
            with caminho.open('w', newline='', encoding='utf-8-sig') as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV, extrasaction='ignore')
                escritor.writeheader()
                escritor.writerows(self.historico)
            print(f'CSV exportado: {caminho}')
            return True
        except (OSError, ValueError) as erro:
            print(f'Erro ao exportar CSV: {erro}')
            return False

    def avaliar_facilidade(self):
        while True:
            valor = input('Facilidade de uso (nota 1 a 5; 0 para não avaliar): ').strip()
            if valor == '0':
                return
            if valor in ('1', '2', '3', '4', '5'):
                self.avaliacoes.append(int(valor))
                self._salvar_lista(self.arquivo_avaliacoes, self.avaliacoes)
                print('Avaliação registrada sem identificar a pessoa.')
                return
            print('Nota inválida. Digite um número de 1 a 5 ou 0.')
