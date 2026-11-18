# Roteiro de vídeo técnico — 5 a 8 minutos

> **A equipe deve narrar com a própria voz.** Este é um guia; cada pessoa precisa entender e explicar o código que está mostrando. O que não for demonstrado não será pontuado.

**00:00–00:25 — Equipe e problema**: mostrar nome do projeto, público (jovens) e problema (serviços e documentos). Todos se apresentam ao longo do vídeo.

**00:25–01:20 — JSON, dicionários e tuplas**: abrir `data/base_conhecimento.json`, explicar os nove campos de um registro, três categorias, 11 orientações e fontes oficiais. Mostrar em `buscar()` a lista de tuplas `(pontos, orientacao)`.

**01:20–02:30 — POO e composição**: mostrar `orientacao.py`, `base_conhecimento.py` e `assistente.py`; explicar `self`, atributos, métodos e a relação `Assistente → BaseConhecimento → Orientacao`.

**02:30–03:35 — Busca e cálculo**: abrir `normalizar()` e `pontuar()`. Executar `Como faço a carteira de trabalho digital?` e calcular os pontos efetivos na tela. Mostrar `ALTA` ou `MÉDIA` pelo limite configurado. Explicar +3 palavra-chave e +1 palavra do título.

**03:35–04:55 — Demonstração de fluxos**: mostrar uma pergunta encontrada; uma pergunta sem resposta (por exemplo, `meteorito zumbido`); entrada inválida (`abc` no menu, `x` em s/n); bloqueio de `meu cpf é 123.456.789-00` (não deve salvar); navegação por categoria com `0 para voltar`.

**04:55–05:45 — Alteração ao vivo**: antes da gravação, escolher uma pergunta segura sem correspondência, por exemplo `preciso do registro profissional online`, e confirmar que ela não obtém 3 pontos. Abrir o JSON da orientação **Carteira de Trabalho Digital**, incluir `registro profissional online` em `palavras_chave`, salvar. **Reiniciar o programa**, pois o JSON é carregado na inicialização. Repetir a pergunta e mostrar que passa a existir correspondência. Explicar o motivo do novo +3. Se a pergunta já pontuar antes, escolha outra frase comprovadamente sem resultado. Deixar a palavra-chave apenas se a equipe julgar que faz sentido e a explicar no README.

**05:45–06:35 — Indicadores e arquivos**: mostrar `historico.json`, `atendimentos.csv` e indicadores gerados após testes. Explicar média de tempo, tentativas, acerto e facilidade. Mostrar resultados **reais** de 3+ pessoas, 10+ atendimentos e uma melhoria feita, sem identificar participantes.

**06:35–07:15 — Decisão técnica e limitação**: explicar a decisão de usar busca por regras e JSON sem bibliotecas externas; mencionar a limitação de detecção de dados pessoais por regra simples e da correspondência lexical.

**07:15–07:30 — Encerramento**: relembrar caráter educacional, fontes oficiais, link do GitHub e participação de todos.

## Checklist antes de gravar

- [ ] Cada integrante consegue explicar a própria parte.
- [ ] Foram feitos testes reais com 3+ pessoas e 10+ atendimentos.
- [ ] O README tem os resultados e a melhoria feita de verdade.
- [ ] A demonstração da palavra-chave funciona antes/depois.
- [ ] Código legível, terminal legível e microfone compreensível.
- [ ] Vídeo tem entre 5 e 8 minutos e está publicado como **não listado**.
- [ ] Link do vídeo e repositório público estão acessíveis.
