# Marketing Hub 50 — laboratório de investigação real

**Status: pronto para cadastro e execução, sem dados humanos/modelos coletados.** Produto candidato: Marketing Hub v2.4.0. Código de pesquisa tem limitações; não há superioridade demonstrada nem "50 marcas já testadas".

## 50 marcas: o desenho, não o resultado

- **Pré-piloto:** 10 marcas × (10 tarefas × 3 condições × 2 repetições + 4 estresses × 3 condições) = **720 prompts**.
- **Estudo planejado:** 50 marcas × (10 × 3 × 2 + 4 × 3) = **3.600 prompts**.
- **Comparações centrais:** 50 × 10 tarefas × 2 repetições × 3 contrastes = **3.000 pares cegos**. Dois votos por par = **6.000 votos** (incluindo 2.000 votos no contraste primário B–C). Os quatro estresses têm avaliação factual separada; não se misturam ao desfecho primário.
- **Cenários**: 10 tarefas de escrita (Instagram, LinkedIn, newsletter, landing, CTA, e-mail, anúncio, suporte, crise e UX microcopy); 4 estresses (brief ambíguo, fatos conflitantes, troca de canal, alegação arriscada).
- **Três condições:** A = modelo competente + briefing, fatos, 3 exemplos; B = A + cartão de voz previamente revisado; C = B + métodos Marketing Hub 2.4.0.
- **Principal:** C vs B, preferência editorial cega para publicabilidade e voz. B vs A secundário. Factualidade, estratégia, UX, custo e tempo em estudos separados.

## Requisitos por marca

Dez setores com cinco marcas cada (vide `brands.50.template.json`), variedade de porte/B2B/B2C/idioma/risco com metas de quotas. Cada organização fornece ao menos **3 textos aprovados para geração + 3 referências reservadas**, um briefing com fatos verificáveis, 14 briefings-tarefa, um cartão de voz criado exclusivamente com textos visíveis, autorização de uso e confirmação do responsável. Preferir 8–12 materiais reais e separação prévia para reduzir vazamento. Apenas marcas reais com autorização entram em resultados de fidelidade. Cenários sintéticos servem **somente para teste de software**.

**Não subir** formulários preenchidos, amostras, respostas, gravações ou julgamentos ao GitHub. Manter `private/` fora da distribuição, revisar LGPD e ética de pesquisa. Para pesquisas com participantes, obter avaliação institucional pertinente.

## Início rápido

Na raiz do repositório:

```bash
python evaluation/lab50/lab.py template --brand-count 50 --out private/brands.50.json
# Preencha com marcas autorizadas; vazios e dados sem aprovação são bloqueados.
python evaluation/lab50/lab.py prepare --brand-count 50 \
  --brands private/brands.50.json --skill-root skills/marketinghub \
  --out private/experimento-50 --seed 4321
python evaluation/lab50/lab.py status --experiment private/experimento-50
```

O comando `prepare` **não chama modelo**. Execute cada prompt numa conversa nova, com provedor/modelo/versão/temperatura consistentes, mantendo os mesmos fatos, orçamento de saída, ordem randomizada e custo/tokens registrados. A condição C naturalmente usa mais tokens de entrada; isso deve entrar na análise de custo e robustez.

### Coleta de respostas

```bash
python evaluation/lab50/lab.py capture --experiment private/experimento-50 \
 --case brand-001--instagram--r1--A \
 --text-file private/resposta-real.txt --provider PROVEDOR --model VERSAO_EXATA \
 --date 2026-11-11T18:00:00Z --temperature 0.2
```

`capture-batch` também existe para importação atômica a partir de um ledger, com hash e data. Consulte `lab.py --help`. Respostas externas e origem do provedor são **declaratórias**; um hash não comprova que um modelo escreveu o texto.

### Avaliação humana cega e em escala

**Somente depois de 3.600 respostas completas**:

```bash
python evaluation/lab50/lab.py blind --experiment private/experimento-50 --out private/revisao-cega
python evaluation/lab50/lab_shard.py create --blind private/revisao-cega \
  --out private/revisores --workers 20
```

Distribua `private/revisores/reviewer-XX/` **apenas** à pessoa correspondente, sem `SHARD_ASSIGNMENT_PRIVATE.json`, chaves nem dados confidenciais de outras marcas. Cada um abre `review.html`, avalia e devolve `judgments.csv` na própria pasta. A distribuição garante avaliadores distintos para os dois votos do mesmo par. Recrute e remunere pessoas reais; não substitua por autojulgamento da IA.

```bash
python evaluation/lab50/lab_shard.py merge --blind private/revisao-cega --shards private/revisores
python evaluation/lab50/lab.py analyze --blind private/revisao-cega --out private/resultado-editorial.json
python evaluation/lab50/lab_ui.py results --analysis private/resultado-editorial.json --out private/relatorio.html
```

**Atenção:** o resultado de `analyze` é descritivo (sinais por marca, taxas por tarefa, concordância); não implementa modelo hierárquico completo, cálculo de poder nem certificação de superioridade. O resultado confirmatório requer estatístico, pré-registro e análise apropriada aos clusters; não usar 6.000 votos como 6.000 marcas independentes.

### Auditoria factual e diagnóstico de confusão

```bash
python evaluation/lab50/lab_quality.py --experiment private/experimento-50 --out private/diagnostico.json
python evaluation/lab50/lab_factual.py prepare --experiment private/experimento-50 --out private/fatos
python evaluation/lab50/lab_factual.py ui --review private/fatos
```

A auditoria factual prepara itens cegos; para o estudo confirmatório recrute pelo menos dois revisores factuais por item selecionado, estratifique seleção e vincule cada claim à fonte. O script incluído para auditoria factual é um apoio de um revisor, **não implementa sozinho a amostragem de 20% com 2 pessoas** prevista no protocolo.

### Estudo humano causal (separado)

Planejar 5 regimes: H0 IA, H1 revisão leve, H2 revisão profunda, H3 humano lidera com IA, H4 humano sem IA. O software fornece alocação aleatória por estratos declarados e registro de sessões; não pode garantir cegamento, aderência, ausência de interferência ou inferência causal por si só.

```bash
python evaluation/lab50/human_study.py assign --roster private/participants.json --out private/human-study --seed 4206
# Colete quatro tarefas reais por participante e avaliação cega independente,
# em private/human-study/sessions.private.csv.
python evaluation/lab50/human_study.py analyze --plan private/human-study \
 --sessions private/human-study/sessions.private.csv --out private/human-result.json
```

Atributos de participante não devem conter nomes, emails ou segredos; participação exige consentimento. O relatório descritivo preserva o braço **atribuído** (ITT), mesmo em não conformidade. Tempo de edição é mediador, não covariável pré-tratamento de uma análise causal principal.

## Ética, UX e rigor metodológico

Ler `PROTOCOL.md`, `PREREGISTRATION.md` e `RUBRICS.md` antes de coletar dados. Testes de usabilidade devem envolver participantes, teclado, leitor de tela, tarefas reais e uma medição global (por exemplo SUS após sessão); conformidade WCAG 2.2 AA só pode ser declarada após inspeção e testes.

Fontes orientadoras: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [OSF](https://help.osf.io/article/330-welcome-to-registrations), [CONAR](https://www.conar.org.br/codigos), [Guia ANPD para pesquisas](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-tratamento-de-dados-pessoais-para-fins-academicos-e-para-a-realizacao-de-estudos-e-pesquisas).
