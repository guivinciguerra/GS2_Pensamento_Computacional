# Citizen Assist AI — orientação ao cidadão

## Equipe

- Integrante 1: Guilherme Vinciguerra Carvalho, RM: 571951
- Integrante 2: Marcos Peterson RM: 571951
- 
## Público, problema e objetivo

**Público escolhido:** jovens em início de vida adulta e do mercado de trabalho que precisam usar serviços públicos digitais.

**Problema:** informações espalhadas e procedimentos pouco claros sobre documentos, conta gov.br e emprego.

**Objetivo:** orientar a partir de informações de fontes oficiais verificadas, indicar documentos, canais e fonte, sem receber CPF, telefone nem e-mail.

**ODS relacionados:** ODS 4 (Educação de Qualidade, letramento digital), ODS 8 (Trabalho Decente e Crescimento Econômico) e ODS 16 (Paz, Justiça e Instituições Eficazes, acesso à informação).

## Como executar

Precisa apenas de **Python 3.9+** (sem bibliotecas externas). Dentro da pasta do projeto:

```bash
python main.py
```

O menu permite fazer perguntas livres, navegar pelas categorias, ver indicadores e exportar CSV. A opção `0` volta ou encerra. Na saída, o programa pede uma avaliação anônima de facilidade de 1 a 5.

Rodar testes de software:

```bash
python -m unittest discover -s tests -v
```

## Estrutura

```text
citizen-assist-ai/
├── README.md
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
├── roteiro_video.md
├── testes_usuarios_modelo.md
├── entrega_fiap_modelo.txt
├── tests/test_sistema.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    ├── avaliacoes.json
    └── atendimentos.csv  (criado pelo programa)
```

O `historico.json` inicia vazio propositalmente. `avaliacoes.json` armazena somente notas anônimas. Não há indicadores de testes reais fabricados.

## As 3 classes e a composição

- `Orientacao` guarda os 9 campos exigidos e usa `exibir()`.
- `BaseConhecimento` contém uma lista de objetos `Orientacao` e implementa `carregar()`, `categorias()`, `por_categoria()`, `pontuar()` e `buscar()`.
- `Assistente` contém uma instância de `BaseConhecimento` e implementa `perguntar()`, `navegar()`, `registrar()`, `indicadores()` e `exportar_csv()`.

**Composição:** `Assistente → BaseConhecimento → lista de Orientacao`. Os objetos acessam seus próprios atributos pelo `self`.

## Regra de normalização, pontuação e confiança

`normalizar()` transforma tudo em minúsculas, remove acentos e pontuação e trata espaços. Para cada orientação:

- **+3** para cada palavra-chave completa que aparece na pergunta normalizada;
- **+1** por palavra **distinta** da pergunta com 4 ou mais caracteres encontrada no título;
- **6 pontos ou mais:** confiança ALTA;
- **3 a 5 pontos:** confiança MÉDIA;
- **menos de 3 pontos:** nenhuma resposta confiável encontrada.

`buscar()` devolve uma **lista de tuplas `(pontos, orientacao)`**, ordenada por pontos decrescentes e ID crescente no desempate. Mostra a melhor resposta e até duas alternativas com pelo menos 3 pontos. Não existe IA generativa: somente correspondência com o JSON.

## Privacidade, transparência e limitações

- O assistente **não solicita dados pessoais**. Se a pergunta tiver `@` ou **8 ou mais dígitos** somados, ela é recusada **antes da busca e do histórico**. Isso segue o critério mínimo do enunciado.
- Respostas incluem fonte, data de consulta e aviso de que o assistente não é oficial.
- Arquivo JSON ausente/corrompido não fecha o aplicativo; a base fica vazia e o menu permanece acessível.
- Limitação: a regra de 8 dígitos ou `@` **não detecta todos os dados pessoais possíveis**. O programa não identifica nomes e endereços escritos por extenso; portanto, evite inserir dados pessoais no campo de perguntas. Para um uso público real, o histórico textual exigiria proteção adicional ou anonimização robusta.
- Pontuação textual pode confundir assuntos próximos; a confiança é **do casamento de palavras**, não de veracidade do conteúdo.
- Serviços, requisitos e páginas públicas podem mudar; é preciso rever a base periodicamente.
- Não integra APIs, outras disciplinas ou modelos externos; isso é opcional no desafio.

## Histórico, métricas e exportação

Cada atendimento válido é registrado em `data/historico.json` com data, origem, pergunta (ou título no fluxo por categoria), ID da orientação, `encontrou`, `ajudou`, `tentativas` e `tempo_segundos`. Na busca, tentativas contam perguntas válidas na mesma interação; dados bloqueados e respostas vazias não contam. O tempo começa ao entrar no fluxo de perguntas e termina quando o usuário conclui a interação; por categoria, mede o tempo da leitura e avaliação da orientação. O indicador usa o tempo médio de atendimentos encerrados, inclusive os sem resultado (nome exibido na tela).

O CSV é exportado por `csv.DictWriter` para `data/atendimentos.csv`. Métricas: taxa de resposta encontrada, taxa de orientações que ajudaram, tempo médio, tentativas por atendimento, nota média de facilidade (1–5) e lista de perguntas sem solução. Resultados vazios são exibidos como **sem dados**, nunca como resultados de teste inventados.

## Fontes oficiais consultadas em 16/11/2026

Cada orientação traz URL e `verificado_em` no JSON. Fontes principais: [criação de conta gov.br](https://www.gov.br/pt-br/servicos/criar-sua-conta-gov.br), [recuperação de senha](https://www.gov.br/governodigital/pt-br/acessibilidade-e-usuario/atendimento-gov.br/duvidas-na-conta-gov.br/recuperar-senha-da-conta-gov.br/recuperar-senha-da-conta-gov.br/), [níveis da conta](https://www.gov.br/governodigital/pt-br/identidade/conta-gov-br/niveis-da-conta-govbr), [segurança da conta](https://www.gov.br/governodigital/pt-br/identidade/conta-gov-br/seguranca-da-conta), [Carteira de Trabalho Digital](https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho), [SINE](https://www.gov.br/pt-br/servicos/buscar-emprego-no-sistema-nacional-de-emprego-sine), [seguro-desemprego](https://www.gov.br/pt-br/servicos/solicitar-o-seguro-desemprego), [inscrição no CPF](https://www.gov.br/pt-br/servicos/inscrever-no-cpf), [Meu CPF](https://www.gov.br/receitafederal/pt-br/assuntos/meu-cpf/cpf), [Título Net](https://www.tse.jus.br/servicos-eleitorais/titulo-eleitoral/autoatendimento-eleitoral) e [e-Título](https://www.tse.jus.br/servicos-eleitorais/servicos/aplicativo-e-titulo/aplicativo-e-titulo).

