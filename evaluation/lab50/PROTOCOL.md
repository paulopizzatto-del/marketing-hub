# Protocolo de pesquisa MH-50 v1 — rascunho para pré-registro

## Escopo e hipótese

Comparar a qualidade editorial do Marketing Hub v2.4.0 (C) **contra o cartão de voz isolado** (B), mantendo modelo, briefing, fatos, exemplos e geração tão comparáveis quanto possível. A diferença B-A mede cartão, não métodos. A comparação C-A é total, não efeito marginal.

**Hipótese primária exploratória:** preferência cega por C na publicabilidade fiel à marca versus B. Antes do estudo confirmatório, congelar modelo, tarefas, amostra, critério primário e diferença mínima relevante acordada com stakeholders (um exemplo para debate é 55%, **não** limiar universal). Um piloto de 10 marcas precede estimativa de ICC/empates e simulação de poder.

## Amostragem estratificada por cotas

50 marcas reais autorizadas, dez famílias/setores com cinco marcas; variar B2C/B2B, porte, maturidade, risco, regiões e idioma. Proposta de cotas: 40 pt-BR, 5 en, 5 es (idiomas não portugueses **exploratórios**, revisão nativa). Cotas não equivalem a amostra probabilística representativa.

Anotar para cada marca `brand_id`, setor, porte, segmento, risco, região, idioma, estado do posicionamento, responsável pela aprovação e escopo da autorização. A mesma marca pode gerar múltiplas tarefas: **unidade de generalização = marca**, não texto/voto.

## Material

No mínimo 3 exemplos para o gerador e 3 holdouts ocultos; cartão de voz preparado apenas com exemplos visíveis, documentação de estratégia, fatos e fonte. Hash antes da geração. Manter marcas reais privadas, pseudonimizar `M001–M050`, não incluir PII desnecessária.

## Variáveis e vieses

- Randomizar ordem dos prompts, sessões novas por caso, manter versão do modelo e parâmetros, registrar `input_tokens/output_tokens/custo/latência` reais quando fornecidos.
- Rótulos de condição ocultos; lado esquerdo/direito contrabalançado por revisor.
- Mesmo teto de tamanho editorial por tarefa; não punir texto apenas por comprimento. A condição C terá instruções adicionais e mais tokens de entrada: medir esse diferencial e planejar análise de sensibilidade.
- Rastrear cópia longa de amostras, contradição com fatos, idioma, confusão com marcas externas e separação do holdout.
- Registrar falhas e respostas vazias; não selecionar apenas as melhores. Toda exclusão precisa de razão anterior ao resultado.

## Avaliação

Core: 3.000 comparações em 6.000 votos humanos (A-C, B-C, A-B); 20 revisores como exemplo operacional, cada par recebe dois revisores distintos. Resultado principal é preferência por publicabilidade **fiel à marca**, com opções esquerda, direita, empate, ambos inadequados. Avaliar dimensões estratégicas e factuais separadamente; revisores veem amostras reservadas mas o gerador nunca as recebe. A revisão por marca exige competência e conflito de interesse documentado.

Estresse: 600 saídas adicionais, triadas por risco/factualidade fora do desfecho primário. Revisão factual do planejamento: 600 textos amostrados estratificadamente × 2 revisores = 1.200 auditorias; o CLI atual só prepara revisão individual, portanto **amostragem e segundo julgamento ainda precisam de coordenação externa**.

## Inferência

Modelos mistos por marca/tarefa/revisor e intervalos de confiança, quando os dados existirem. Calibrar com pré-piloto; não declarar poder de 80% sem simulação. Analisar empates, ambos ruins, marca, setor, risco e idioma; comparações secundárias com controle de multiplicidade. Respostas observacionais não são evidência de aumento de conversão. Regimes humanos H0–H4 requerem randomização e análise ITT, separadamente da diferença A/B/C.

## Governança

LGPD/ANPD, direitos de conteúdo, autorização para uso e confidencialidade; comitê de ética quando aplicável. Arquivos privados em `private/` fora do Git. Somente sínteses autorizadas e outputs pseudonimizados podem ser publicados depois de revisão. Sem criar uma medição chamada "porcentagem humana". O estudo compara regimes de envolvimento, não uma essência quantificável da escrita humana.
