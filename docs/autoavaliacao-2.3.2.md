# Autoavaliação técnica 2.3.2

**Data:** 11/11/2026. Esta é uma revisão técnica, não benchmark editorial nem parecer jurídico.

## Veredito

A 2.3.2 está **apta para revisão externa e futura publicação técnica**, sem alegação de superioridade editorial. O incremento corrige problemas do protocolo de piloto, generaliza o avaliador e reduz duplicidade de instalação. O valor incremental do Hub continua dependente do piloto com saídas reais e avaliação humana cega.

## Verificações executadas

- `python scripts/check_repo.py`: aprovado.
- `python -m unittest discover -s tests -v`: **56 testes aprovados**.
- `python skills/marketinghub/scripts/validate_brand_profile.py --require-full examples/brand-profile-ficticio.json`: aprovado.
- `python -m compileall -q scripts skills/marketinghub/scripts tests`: aprovado.
- `python scripts/build_release.py`: concluído; duas execuções consecutivas mantêm arquivos determinísticos pelos testes existentes.
- `scripts/analyze_pilot.py`: exercitado com amostra sintética; mantém empates e calcula teste de sinais por marca.

## Melhorias relevantes

1. O piloto deixou de exigir simultaneamente uma estimativa pontual de 60% e IC acima de 50%. Agora é tratado como estudo de estimação com poucos clusters, empates e comprimento pré-registrados.
2. O avaliador não carrega mais as 20 marcas de fixture de forma implícita. `--cases` é obrigatório e pode apontar para regras reais autorizadas.
3. Segredos, placeholders, recusas e dados pessoais aparentes bloqueiam a passagem mecânica; alegações comerciais geram revisão humana. Isso não certifica verdade nem conformidade jurídica.
4. Termos por marca podem ser aprovados, proibidos, cuidadosos ou pendentes. `voice.avoid_terms` legado continua funcionando.
5. Codex, Gemini, Copilot e Cursor convergem para `.agents/skills`; Claude Code usa `.claude/skills`.
6. O cartão de voz passou a registrar sinais observáveis, mas as amostras brutas continuam sendo usadas quando disponíveis. Há uma única autocrítica curta antes da entrega.
7. Arquivos reais do piloto são excluídos do pacote público por padrão.

## Pendências

- executar o piloto real;
- definir e validar a ferramenta estatística para inferência com poucos clusters antes da coleta;
- testar descoberta/ativação ponta a ponta nos clientes anunciados;
- revisar listas regulatórias setoriais com especialistas antes de transformá-las em regras específicas;
- validar inglês e outros idiomas com revisores adequados antes de ampliar promessas.
