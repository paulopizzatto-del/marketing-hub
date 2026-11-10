# Piloto editorial: protocolo preparado, ainda não executado

## Base do desenho

Este protocolo preserva o desenho de 144 saídas proposto no parecer independente do Claude de 10/11/2026: **8 marcas × 3 tarefas × 3 condições × 2 repetições**, em um modelo e em pt-BR. O script cria uma agenda, não chama um modelo e não preenche resultados.

- **A:** assistente competente + briefing + três amostras.
- **B:** Marketing Hub + o mesmo briefing + as mesmas amostras.
- **C:** Marketing Hub + o mesmo briefing, sem as amostras.

A comparação primária é B × A. B × C investiga o efeito de fornecer as amostras dentro do Hub. **Esse desenho não isola o efeito do cartão de voz.** Como alternativa sugerida na discussão posterior, poderia ser registrado um protocolo A=base, B=base+cartão, C=base+cartão+Hub; mudar o desenho exige decisão e pré-registro antes da geração, sem misturar resultados entre protocolos.

## Pré-requisitos humanos

Cada marca precisa de cinco textos de referência escritos/revisados por uma pessoa: três como entrada e dois reservados para a avaliação. Preencher o template e obter aprovação antes de executar. As fixtures curtas do repositório não substituem essas amostras.

## Execução

Registrar provedor, modelo/versão, data, parâmetros, instruções exatas e hash da skill. Manter fatos e tarefas equivalentes; mudar apenas os componentes definidos para cada condição. Abrir contexto novo por saída, sortear ordem com seed registrada e usar duas repetições. Registrar tokens, custo informado pelo provedor e latência quando mensuráveis; nenhum deles é inferido.

`python scripts/prepare_pilot.py --out dist/pilot-plan.json` prepara a agenda marcada `not_run`. `--check-inputs arquivo.json` verifica a presença das amostras antes da execução; não comprova revisão humana.

## Avaliação

Dois avaliadores independentes dos autores dos prompts recebem as duas referências reservadas e pares de candidatos com condições ocultas e ordem sorteada. Métrica primária: qual candidato parece mais com a marca. Secundárias: clareza (1–5), alegações inventadas (sim/não e contagem) e publicação com poucos ajustes (sim/não). Tempo de edição é uma sugestão adicional, a registrar antes do ensaio.

O parecer propõe preferência por B de pelo menos 60%, com limite inferior de IC95% acima de 50%. Calcular intervalos por reamostragem agrupada por marca, descrever as limitações de apenas oito grupos e a concordância dos revisores. São 48 pares por comparação, agrupados em oito marcas, não 144 observações independentes. Resultado inconclusivo não prova equivalência.

## Resultados e gráficos

Nenhuma saída real foi incluída nesta correção. Os arquivos de resultado permanecem vazios. Gráficos só devem ser gerados depois de dados reais revisados: preferência com intervalo, variação por marca, alegações e custo/latência. Informar unidades, amostra, condições, versão e data; nunca apresentar fixture como resultado. Publicar conclusão favorável, negativa ou inconclusiva com a mesma regra.
