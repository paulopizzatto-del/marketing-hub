# Autoavaliação técnica — Marketing Hub 2.4.0 (registro pré-publicação)

**O que existe e foi exercitado**

- Skill, guias e prompt portátil com roteamento por risco e tipo de tarefa.
- Studio local responsivo: campos obrigatórios, prompt, JSON exportável, função de limpeza e verificação de ausência de rolagem horizontal em tamanhos testados de desktop/mobile. Execução direta no Chromium com HTML injetado, por restrições de navegação local no ambiente de teste.
- Laboratório planejado de 50 marcas: 3.600 prompts sintéticos preparados em testes, holdouts ausentes dos prompts, tentativas de revisão antes da captura bloqueadas, integridade detecta adulteração, 20 pacotes de revisor em testes e reagrupamento de votos sintéticos.
- Atribuição de participantes H0–H4 balanceada para 250 IDs sintéticos em teste.
- Documentos de protocolo e pré-registro em estado **rascunho**.

**O que ainda não foi comprovado**

- Nenhuma métrica comparativa de saída real de LLM frente ao baseline A/B.
- Nenhum voto humano real, auditoria factual independente real ou medida de conversão.
- Nenhum teste de usabilidade com pessoas com deficiência ou certificação de conformidade WCAG 2.2 AA.
- Nenhuma melhoria causal de produtividade: sem coleta do estudo humano.
- Compatibilidade ponta a ponta com todos os clientes de IA ainda não comprovada.

**Riscos e decisões**

- C possui mais tokens de entrada que B: a comparação de qualidade deve contabilizar custo e incluir análise de sensibilidade.
- O Lab50 entrega agregados descritivos; análise estatística hierárquica confirmatória exige implementação auditada por pessoa qualificada e pré-registro.
- Revisão factual automática não deve substituir especialista nem normalizar claims não sustentados.
- O Studio é uma ferramenta de montagem de prompt, **não analisa amostras por algoritmo de IA nem gera textos finais**.
- Não liberar alegação 'somos superiores' antes de dados reais, estudos cegos e inferência apropriada.
- No momento desta autoavaliação, a versão 2.4.0 ainda era candidata. A [release oficial v2.4.0](https://github.com/paulopizzatto-del/marketing-hub/releases/tag/v2.4.0) foi publicada posteriormente, em 11/11/2026.
