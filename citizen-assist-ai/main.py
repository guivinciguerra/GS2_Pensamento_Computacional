"""Executar com: python main.py"""
from pathlib import Path
from assistente import Assistente
from base_conhecimento import BaseConhecimento


def main():
    raiz = Path(__file__).resolve().parent
    base = BaseConhecimento(raiz / 'data' / 'base_conhecimento.json')
    base.carregar()
    assistente = Assistente('Citizen Assist AI', base, raiz / 'data')
    print(f'\nBem-vindo ao {assistente.nome}!')
    print('Orientações educativas, com fontes oficiais. Não informe dados pessoais.')
    print('Este assistente NÃO é um canal oficial.')
    try:
        while True:
            print('\nMENU PRINCIPAL')
            print('1. Perguntar em texto livre')
            print('2. Navegar por categorias')
            print('3. Ver indicadores')
            print('4. Exportar atendimentos para CSV')
            print('0. Sair')
            opcao = input('Escolha: ').strip()
            if opcao == '1':
                assistente.perguntar()
            elif opcao == '2':
                assistente.navegar()
            elif opcao == '3':
                assistente.indicadores()
            elif opcao == '4':
                assistente.exportar_csv()
            elif opcao == '0':
                assistente.avaliar_facilidade()
                assistente.exportar_csv()
                print('Obrigado por usar o Citizen Assist AI!')
                break
            else:
                print('Opção inválida. Digite um número do menu.')
    except (EOFError, KeyboardInterrupt):
        print('\nEncerrando de forma segura.')
        assistente.exportar_csv()


if __name__ == '__main__':
    main()
