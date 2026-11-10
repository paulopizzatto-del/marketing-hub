# Analytics, diagnóstico e experimentos editoriais

Integra `analytics-dashboard` e controle de qualidade de `post-scorer`. **Não há métricas confiáveis sem dados reais da conta e período.** A skill não recebe acesso automático a Instagram, LinkedIn, Meta, Google Analytics, Buffer ou ferramentas de publicação.

## Coleta e auditoria

1. Identificar marca, contas, canal, período, fuso, fonte e granularidade (post/dia/campanha).
2. Verificar nome e definição das colunas. Separar seguidores, alcance (pessoas únicas), impressões (exibições), visualizações, cliques, reações, comentários, compartilhamentos, salvamentos, leads e vendas.
3. Validar unidades e formato numérico, incluindo vírgula decimal e separador de milhares. Distinguir número ausente de zero.
4. Remover duplicidades somente com chave comprovada (ID/URL de publicação e contexto), não pelo título.
5. Segmentar por formato, tema, objetivo e canal apenas quando os dados permitirem.
6. Comparar janelas equivalentes, indicando mudança de volume, sazonalidade e posts extraordinários.

## Indicadores

**Taxa de engajamento por impressões (exemplo):**

`ER_i = (reacoes + comentarios + compartilhamentos + salvamentos) / impressoes * 100`

Declarar explicitamente que interações foram incluídas e qual é o denominador. Algumas redes/exportações definem engajamento de maneira distinta; não misturar. Para agregado, usar **soma de interações / soma de impressões**, e não média simples das taxas por post, a menos que esse seja o indicador desejado.

**Variação relativa:** `(atual - anterior) / anterior * 100` quando o denominador não é zero. Distinguir de variação em pontos percentuais. Impressão não é pessoa única; curtida não é compra. Crescimento de seguidores não prova causalidade de post.

**Métricas de objetivo:** alcance para notoriedade, retenção e interações relevantes para conteúdo, leads qualificados para aquisição, tráfego para encaminhamento, conversão para vendas; documentar métodos e limitações.

## Diagnóstico

- Comparar desempenhos **por objetivo**, sem premiar automaticamente viralidade.
- Analisar conteúdo e contexto dos melhores e piores posts disponíveis; não confundir amostra selecionada com universo.
- Listar hipóteses, fontes, tamanho da amostra e variáveis de confusão. Ex.: formato vertical pode coincidir com campanha paga, e não causar sozinho o aumento de alcance.
- Não inventar melhor horário, frequência ideal ou projeção de crescimento. Só sugerir testes de horários como hipótese, com métricas e período de observação.

## Experimentos

Descrever para cada teste:

`hipótese | variável que muda | comparação/controlado | métrica primária | duração | interpretação e limitações`

Testes pequenos não garantem significância estatística. Evitar alegar melhoria causal sem desenho apropriado. Escolher mudanças controladas quando possível: abertura, nível de tecnicidade, foto real vs card, formato de CTA ou tema.

## Apresentação dos dados

Painel útil pode incluir alcance/impressões, taxa de interação com denominador, evolução temporal, temas e formatos, tabela de posts e limitações dos dados. Construir somente com ferramenta de arquivo/gráfico disponível; explicar quando houver apenas análise textual. Não prometer "dashboard interativo" sem gerar arquivo funcional.

## Saída sugerida

- Resumo do período com fontes e janela.
- Indicadores calculados com definição.
- Padrões e riscos (sem causalidade inventada).
- 3 prioridades de conteúdo e 2–4 testes rastreáveis.
- Lacunas para melhorar a medição.

## Exemplo calculado (dados fictícios)

Dois posts têm 100 interações / 2.000 impressões e 160 / 8.000. As taxas individuais são 5% e 2%. O agregado ponderado é (100 + 160) / (2.000 + 8.000) = **2,6%**, e não a média simples de 3,5%. Declarar quais interações entraram na conta. Este cálculo ensina o denominador; não demonstra resultado do Hub.
