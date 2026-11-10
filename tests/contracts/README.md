# Testes de contrato, não benchmark de escrita

Os 20 perfis e 60 textos em `tests/fixtures/20-brands-3-rounds.json` foram autorados como fixtures. Conferem leitura de perfis, identidade dos casos e sinais mecânicos. Não representam respostas geradas por modelos, amostras de voz aprovadas por avaliadores independentes ou evidência de superioridade do Hub.

Os textos curtos de LinkedIn dessa fixture não definem um padrão de qualidade ou extensão da rede. Critérios de formato são avisos por tarefa; idioma e relevância não são medidos por palavras obrigatórias.

O avaliador de registros reais usa `scripts/editorial_checks.py`, independente dos testes. Erros de dados/segurança bloqueiam; sinais de alegação pedem revisão individual; formato apenas avisa. Revisão de voz, verdade e idioma continua humana. Um campo `human_approved: true` registra uma declaração, não prova que houve avaliação independente.

Execute `python -m unittest discover -s tests -v` e `python scripts/report_20_brands.py`. Para comparar condições reais, use o [piloto separado](../../evaluation/pilot-144/PLAN.md).
