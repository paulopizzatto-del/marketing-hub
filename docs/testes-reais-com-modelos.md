# Resultados reais: registro e limites

O script `evaluate_model_outputs.py` verifica registros dos casos legados em `tests/fixtures/20-brands-model-prompts.jsonl`. **Não atribui nota de qualidade nem detecta idioma por palavra-chave.** O novo piloto comparativo tem protocolo separado em [evaluation/pilot-144/PLAN.md](../evaluation/pilot-144/PLAN.md).

Cada linha JSONL dos casos legados deve ter `case_id`, `output` e `human_approved`. Registre provedor e versão com `--provider` e `--model-version`. Use `--report caminho.json` para salvar um relatório sem os textos completos.

Três saídas do verificador: `safety_errors` (dados ausentes, credenciais e violações explícitas), `review_flags` (alegações que exigem revisão) e `format_warnings` (sugestões editáveis por tarefa, não limites oficiais das redes). Um LinkedIn longo ou uma legenda em inglês sem palavras da fixture não falha por esse motivo.

Percentuais são sinais para checar contexto, não prova de falsidade. Para resolver um sinal, registrar em `reviewed_flags` seu `id` exato, `decision: accepted`, `reason` e `evidence`. Isso registra a decisão humana; o código não confirma que a fonte é verdadeira. Declarações incompletas, casos ausentes ou credenciais permanecem bloqueados.

Voz, clareza, idioma, originalidade e adequação precisam de avaliadores independentes. Registre entradas, amostras, parâmetros, saídas reais, modelo, versão e data. Não preencha resultados com fixtures nem anuncie superioridade a partir de testes de código.
