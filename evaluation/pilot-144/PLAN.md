# Piloto editorial: protocolo preparado, ainda não executado

## Objetivo

Este piloto estima se o Marketing Hub melhora fidelidade à voz em relação a uma instrução competente com o **mesmo briefing e as mesmas amostras**. Ele não foi executado e não contém resultados reais.

O desenho inicial permanece em **8 marcas × 3 tarefas × 3 condições × 2 repetições = 144 saídas**, em um modelo e em pt-BR. O número de pares não deve ser confundido com unidades independentes: para a comparação principal há 48 pares B×A, agrupados em apenas oito marcas.

- **A:** assistente competente + briefing + três amostras.
- **B:** Marketing Hub + o mesmo briefing + as mesmas três amostras.
- **C:** Marketing Hub + briefing, sem amostras.

A comparação primária é B × A. B × C investiga o efeito das amostras dentro do Hub. Uma ablação alternativa A=base, B=base+cartão, C=base+cartão+Hub pode ser registrada em outro protocolo; não misturar resultados de desenhos diferentes.

## Pré-registro antes da geração

Registrar: provedor; modelo/versão; data; parâmetros; prompts e hashes; seed; marcas e amostras; orçamento de caracteres/palavras por tarefa; política de emoji, hashtag e quebras; tratamento de empates; análise primária e de sensibilidade.

Cada marca precisa de cinco textos reais aprovados por uma pessoa: três entram como amostra e dois ficam reservados. As amostras devem ser características e, de preferência, variar tema/formato. Os textos reservados nunca entram na geração.

## Controle de comprimento, posição e empates

Definir uma faixa de comprimento por tarefa **antes** de gerar. Se uma saída escapar da tolerância por erro de execução, regenerar usando a mesma regra para todas as condições e registrar a regeneração. Não favorecer a condição que escreve mais.

Aleatorizar A/B por par e contrabalancear posição por avaliador, marca e tarefa. Permitir três respostas: **A**, **B** ou **sem diferença**; manter também **ambos ruins** como motivo editorial, sem convertê-lo silenciosamente em vitória.

Análise primária de preferência: excluir empates do denominador e reportar a taxa de empate. Sensibilidade: empate vale meia vitória. Nunca descartar empates sem mostrar quantos ocorreram.

## Avaliadores

Preferir pessoas que conheçam a marca ou editores capazes de reconhecer seus textos. Usar pelo menos dois avaliadores independentes dos autores dos prompts e calibrá-los com pares fora da amostra. Reportar resultados por avaliador e concordância percentual; kappa/AC1 podem ser calculados em análise posterior quando houver dados suficientes.

Um juiz LLM, se usado, é apenas análise secundária: modelo de família diferente do gerador, pares nas duas ordens e conflitos tratados como empate. Ele não desempata humanos e não entra no critério primário.

## Critério e inferência

**Não usar “estimativa B ≥ 60%” como requisito adicional.** Esse limiar pontual pode reprovar aproximadamente metade dos estudos mesmo quando o efeito verdadeiro estiver exatamente em 60%.

Tratar esta rodada como **piloto de estimação**. O efeito principal é a preferência B×A, com incerteza agrupada por marca. Com apenas oito marcas, intervalos assintóticos e bootstrap por pares de clusters podem ser mal calibrados.

Pré-registrar:

1. **Análise principal:** estimativa agrupada por marca e método adequado a poucos clusters (por exemplo, modelo logístico misto com inferência robusta/wild-cluster quando a ferramenta estatística escolhida for validada).
2. **Robustez simples e reproduzível:** teste de sinais exato sobre a direção do efeito por marca. O script `scripts/analyze_pilot.py` fornece esta análise descritiva/exata sem dependências externas.
3. **Sensibilidade:** diferença de comprimento entre condições e tratamento de empates como meia vitória.

O piloto não “certifica” o produto. Ele estima efeito, heterogeneidade entre marcas, empates e concordância para dimensionar um estudo confirmatório. Se houver recursos, aumentar primeiro para **12–16 marcas**, antes de multiplicar repetições por marca.

## Dados e privacidade

Não colocar saídas reais, textos de clientes, dados pessoais ou avaliações humanas identificáveis no repositório público. `evaluation/pilot-144/results/` contém apenas instruções públicas; dados reais devem ficar em armazenamento privado ou registro embargado. Publicar depois apenas o conjunto autorizado e anonimizado, com proveniência clara.

## Resultados e gráficos

Só gerar gráficos depois de respostas reais e revisão humana. Mostrar: preferência com incerteza, pontos por marca, taxa de empate, alegações sinalizadas, comprimento/tokens e custo/latência quando disponíveis. Eixo, unidade, amostra, versão do modelo e data devem aparecer. Resultado favorável, nulo ou desfavorável deve ser publicado pelo mesmo critério.
