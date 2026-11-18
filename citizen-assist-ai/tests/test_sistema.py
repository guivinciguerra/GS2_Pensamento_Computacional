"""Testes automatizados SEM substituir os testes obrigatórios com pessoas reais."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from base_conhecimento import BaseConhecimento, normalizar
from assistente import Assistente, contem_dados_pessoais

RAIZ = Path(__file__).resolve().parents[1]

class Testes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = BaseConhecimento(RAIZ / 'data' / 'base_conhecimento.json')
        self.assertTrue(self.base.carregar())
        self.assistente = Assistente('Teste', self.base, self.temp.name)

    def test_base_e_campos(self):
        self.assertGreaterEqual(len(self.base.orientacoes), 10)
        self.assertGreaterEqual(len(self.base.categorias()), 3)
        self.assertTrue(all(len(o.palavras_chave) >= 3 for o in self.base.orientacoes))

    def test_normalizacao(self):
        self.assertEqual(normalizar('TÍTULO?!'), ' titulo ')

    def test_pontuacao_e_tuplas(self):
        resultados = self.base.buscar('Como faço a carteira de trabalho digital?')
        self.assertIsInstance(resultados[0], tuple)
        self.assertGreaterEqual(resultados[0][0], 6)
        self.assertEqual(resultados[0][1].id, 5)
        self.assertEqual(resultados, sorted(resultados,key=lambda x: (-x[0],x[1].id)))

    def test_sem_resultado(self):
        self.assertLess(self.base.buscar('meteorito zumbido')[0][0], 3)

    def test_protecao_privacidade(self):
        self.assertTrue(contem_dados_pessoais('123.456.78'))
        self.assertTrue(contem_dados_pessoais('pessoa@provedor.com'))
        self.assertFalse(contem_dados_pessoais('como tirar cpf?'))
        self.assertFalse(self.assistente.registrar('pergunta','12345678',1,True,True,1,1))
        self.assertFalse(self.assistente.historico)

    def test_registro_csv(self):
        self.assertTrue(self.assistente.registrar('pergunta','Como obter a CTPS?',5,True,True,1,2.5))
        self.assertTrue(self.assistente.exportar_csv())
        self.assertEqual(len(json.loads((Path(self.temp.name)/'historico.json').read_text())),1)
        self.assertIn('Como obter a CTPS?', (Path(self.temp.name)/'atendimentos.csv').read_text(encoding='utf-8-sig'))

    def test_json_faltando_ou_corrompido(self):
        b = BaseConhecimento(Path(self.temp.name) / 'faltando.json')
        with patch('builtins.print'):
            self.assertFalse(b.carregar())
        errado = Path(self.temp.name)/'quebrado.json'
        errado.write_text('{',encoding='utf8')
        b = BaseConhecimento(errado)
        with patch('builtins.print'):
            self.assertFalse(b.carregar())

    def test_menu_invalido_e_navegacao(self):
        with patch('builtins.input',side_effect=['abc','99','1','abc','1','x','s','0','0']):
            with patch('builtins.print'):
                self.assistente.navegar()
        self.assertEqual(len(self.assistente.historico),1)

    def test_pergunta_privada_nao_registrada(self):
        with patch('builtins.input',side_effect=['meu numero 123456789','0']):
            with patch('builtins.print'):
                self.assistente.perguntar()
        self.assertEqual(self.assistente.historico, [])

if __name__ == '__main__':
    unittest.main()
