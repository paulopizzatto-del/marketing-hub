# Revisão 2.3.2 — validade do piloto, riscos de publicação e portabilidade

Esta correção incorpora recomendações da reavaliação externa sem transformar heurísticas em certificação. A prioridade foi reduzir risco de **evidência inválida sobre o próprio produto**.

## Implementado

- piloto tratado como estudo de estimação; removido o requisito redundante de estimativa pontual ≥60%; empates, comprimento, posição e poucos clusters passam a ter regra explícita;
- `scripts/analyze_pilot.py` adiciona resumo reproduzível, teste de sinais exato por marca e sensibilidade de empates sem fingir um modelo confirmatório;
- avaliador exige arquivo `--cases` explícito; não lê mais as 20 fixtures silenciosamente;
- padrões de segredo, dados pessoais aparentes, placeholder e recusa viram bloqueios mecânicos; percentuais, multiplicadores, preços, superlativos objetivos, “grátis”, depoimentos e disclosure patrocinado viram revisão humana;
- políticas de termos por marca: aprovado / não usar / usar com cuidado / pendente, com normalização básica;
- cartão de voz passa a registrar regras observáveis e “não soa como nós”; as três amostras continuam no contexto quando disponíveis;
- fluxo de escrita ganhou uma comparação silenciosa e uma reescrita curta contra amostras/cartão;
- instalador converge Codex/Gemini/Copilot/Cursor para `.agents/skills` e Claude Code para `.claude/skills`, reduzindo duplicatas;
- dados reais do piloto ficam fora do pacote público; o build só permite o README público em `evaluation/pilot-144/results/`;
- versão avançada para 2.3.2 para evitar dois artefatos diferentes com o mesmo número.

## Não automatizado

- Nenhum verificador declara conformidade jurídica. Regras comerciais/regulatórias são sinais para revisão qualificada.
- Wild cluster bootstrap/logística mista não foram implementados na biblioteca padrão. O protocolo os descreve como opção estatística a validar antes da coleta.
- Não há resultado do piloto, benchmark multimodelo, validação nativa de inglês/mandarim ou teste de descoberta em todos os clientes.

## Evidência externa usada na decisão

Documentação oficial atual confirma `.agents/skills` como caminho compartilhado em Codex/Gemini/Copilot e `.claude/skills` para Claude Code. O CDC exige informação/oferta correta, clara e suficientemente precisa, e o CONAR mantém código próprio para alegações publicitárias. Essas referências orientam o lint, mas não transformam o Marketing Hub em ferramenta jurídica.
