# Testar o Marketing Hub em modelos reais

O repositório contém 20 marcas inteiramente fictícias e 60 amostras editoriais escritas para auditoria offline. **Essas amostras não são saídas obtidas do ChatGPT, Claude ou Gemini por execução da skill.**

## Ensaio real reproduzível

1. Instale a skill em cada cliente compatível, ou forneça o prompt universal como instruções e o JSON de perfil completo como contexto. Identifique nome e versão do modelo.
2. Leia os 60 pedidos em `tests/fixtures/20-brands-model-prompts.jsonl`. Execute cada caso em contexto isolado para evitar que a saída de outra marca influencie o resultado.
3. Grave um JSONL para cada modelo, com um objeto por `case_id`: `{"case_id": "briarfina-de-papel/instagram", "output": "resposta real do modelo", "human_approved": true}`. Não marque `human_approved: true` antes de revisão humana de voz, factualidade e intenção.
4. Execute `python scripts/evaluate_model_outputs.py --results results-gpt.jsonl --provider ChatGPT --model-version <versão>`, e repita para Claude, Gemini e demais provedores realmente utilizados.
5. Revise manualmente alegações, língua, naturalidade, clareza, privacidade e uniformidade de tom. O verificador só consegue identificar problemas observáveis por regras; qualidade e intenção dependem da leitura humana.

Um arquivo com qualquer uma das 60 saídas ausente ou sem revisão **falhará** por padrão; o teste não inventará um resultado.

## Gate de estabilidade (saída do beta)

- Todos os 20 perfis têm schema válido e os 60 casos offline passam nos verificadores objetivos.
- Todas as versões de modelos anunciadas como 'testadas' devem ter 60 respostas reais e avaliadas, sem casos em aberto.
- Devem estar claros o provedor, versão, data, condições de execução e limitações. **Não extrapolar 100% nesta amostra para 100% de qualidade futura.**
- Checar licença de software, atribuição do material de terceiros e autorização de divulgação das artes originais da marca.
- Para criar o repositório remoto, a ferramenta conectada precisa suportar a criação de repositórios, ou o proprietário deve criá-lo manualmente antes de permitir commits por API.

Enquanto esse gate não for cumprido, disponibilize o projeto apenas como **prévia pública (beta)**. Não anuncie certificação multimodelo, memória persistente nem confiabilidade de 100%. Relate o provedor, a versão e a data de qualquer teste real executado.
