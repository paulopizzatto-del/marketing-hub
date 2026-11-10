# Marketing Hub | Auditoria de 20 marcas fictícias

**Tipo de teste:** validação offline de perfil e revisão de amostras editoriais autoradas. **Não é uma avaliação da execução em outros modelos de IA.**

## Resultado objetivo

- Perfis distintos: **20**.
- Passagens por marca: **3** (Instagram, LinkedIn e comentário).
- Amostras editoriais aprovadas pelos critérios automatizados: **60/60**.
- Critérios: relação com o assunto, ausência de termos proibidos, nenhuma outra marca identificada, sem promessas absolutas ou métricas inventadas, estrutura e tamanho dos textos, verificações básicas de idioma.
- Os testes de unidade e validação JSON são executados pelo workflow de CI, separadamente.

## Matrizes por marca (todas simuladas, nenhuma empresa real)

| Marca fictícia | Tema | Instagram | LinkedIn | Comentário |
|---|---|:---:|:---:|:---:|
| Briarfina de Papel | floricultura | OK | OK | OK |
| Grão de Órbita | cafeteria | OK | OK | OK |
| Nó de Argila | cerâmica artesanal | OK | OK | OK |
| Aula de Brumas | aulas de idiomas | OK | OK | OK |
| Roda de Mirtilo | oficina de bicicletas | OK | OK | OK |
| Nimbo e Linha | ajustes de roupas | OK | OK | OK |
| Trem de Biscoito | padaria | OK | OK | OK |
| Cores de Fósforo | design gráfico | OK | OK | OK |
| Compasso das Folhas | paisagismo | OK | OK | OK |
| Estrela de Tinta | editora independente | OK | OK | OK |
| Mimo do Asteroide | pet shop | OK | OK | OK |
| Vento de Teclas | software de organização | OK | OK | OK |
| Casa da Alga | ONG ambiental | OK | OK | OK |
| Pontes Claras | consultoria operacional | OK | OK | OK |
| Sorriso de Jade | consultório odontológico | OK | OK | OK |
| Cofre de Chá | educação financeira | OK | OK | OK |
| Tecido em Marte | brechó | OK | OK | OK |
| Pomar em Pixel | jogos narrativos | OK | OK | OK |
| Sol de Parafuso | ferramentas para reparo | OK | OK | OK |
| Norte de Caderno | mentoria de estudo | OK | OK | OK |

## Histórico da execução

- Rodada inicial: 58/60 exemplos atenderam aos critérios; dois comentários eram genéricos para o nicho.
- Correção: foram reescritos os dois comentários para mencionar, respectivamente, pão e tarefas de equipe; não afrouxamos a regra de relevância.
- Nova rodada: 60/60 amostras autoradas passaram na bateria offline.
- Testes negativos detectam termos proibidos, contaminação entre marcas, promessa não verificada, credencial sintética e nível inválido de formalidade.

## Limites e decisão de lançamento

**Não declarar compatibilidade ou qualidade editorial de 100% em diferentes IAs com base nesta auditoria.** As 60 amostras foram escritas como fixtures de avaliação; o repositório é uma skill/prompt e não contém motor de inferência próprio. Não houve chamadas reais ao Claude, Gemini, Copilot ou ChatGPT por instalação da skill. Uma validação funcional exigiria executar os 60 briefings em versões identificadas dos modelos, guardar saídas e fazer revisão editorial independente.

**Situação:** o projeto é distribuído como prévia pública (beta), com escopo e limitações transparentes. Os testes offline validam estrutura e amostras autoradas; **não** comprovam desempenho na execução em GPT, Claude, Gemini ou Copilot. Não declarar nenhum modelo como validado até completar o protocolo de 60 respostas reais com revisão humana.

## Reproduzir

```bash
python -m unittest discover -s tests -v
python scripts/check_repo.py
python scripts/report_20_brands.py
```
