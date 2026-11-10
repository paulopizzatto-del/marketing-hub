# Onboarding: personalizar sem atrito

## Objetivo

Construir uma base editorial confiável e reutilizável para **qualquer** negócio, pessoa criadora, entidade, campanha ou produto. Não presumir segmento, maturidade, país, canal, capacidade técnica ou tom desejado. Não importar configurações de marcas anteriores de terceiros.

## Três entradas possíveis

1. **Briefing pronto**: a pessoa fornece materiais (site, manual, exemplos, público e objetivo). Analisar primeiro; fazer uma pergunta apenas se a lacuna impedir o trabalho pedido.
2. **Descrição curta**: nome + o que oferece + público + canal. Entregar uma primeira peça útil imediatamente; refinamento de voz é opcional.
3. **Configuração completa solicitada**: levantar marca, ofertas, público, diferenciais evidenciados, voz desejada, canais, limites, materiais e objetivos. Agrupar perguntas em 2 ou 3 conversas curtas, não exigir cadastro de 25 campos antes de criar algo.

## Perguntas essenciais para configuração completa

Usar somente as ainda não respondidas pelos materiais:

- "Qual é sua marca, o que você oferece e para quem?"
- "Como quer que a marca soe? Pode mandar 2–3 posts que representam essa voz?"
- "Quais canais e objetivos são prioridade agora?"

Opcional, em etapa posterior: o que jamais deve ser dito, ofertas ativas, link/CTA autorizado, limites regulatórios, diretrizes visuais, concorrentes/referências, calendário e equipe responsável pela aprovação. Se houve amostras ou documentação, priorizar aquilo em vez de adjetivos soltos.

## Montar uma ficha de marca

Organizar os elementos em `templates/brand-profile.template.json` e seguir `references/profile-model.md`:

1. **Identidade:** nome, tipo de emissor, descrição fiel, idioma/mercado, identidade visual quando houver referência.
2. **Público e oferta:** segmento de cliente, problema, necessidade, proposta real, produto/serviço documentado.
3. **Voz e posicionamento:** 3–5 atributos, grau de formalidade/humor/tecnicidade, pronomes, expressões próprias, termos a evitar, exemplos aprovados.
4. **Objetivos e canais:** conscientização, relacionamento, leads, reputação, comunidade ou educação. Configurar CTA pertinente, não exigir sempre link.
5. **Políticas e restrições:** promessas que exigem prova, assuntos proibidos, direitos de imagem, setores regulados e fluxos de aprovação.
6. **Fontes:** URL/arquivo/texto originário; data de verificação quando consultado; evidência de cada alegação importante.

Distinguir `confirmed`, `inferred`, `unknown` em notas quando apropriado. Não preencher com boatos do nicho. Se a pessoa não quiser publicar uma ficha, trabalhar com o contexto da conversa.

## Calibração em duas etapas

1. **Retrato da voz:** identificar o que é consistente nos exemplos (vocabulário, comprimento, ritmo, humor, estrutura, CTA). Separar estilo dos fatos e da campanha específica.
2. **Teste de voz:** escrever duas microlegendas sobre o mesmo tema, com nuances distintas; apresentar para escolha apenas durante configuração de voz, não durante a produção rotineira.

Quando receber correção "mais humano/menos formal", atualizar somente o perfil ativo, não as demais marcas. Somente gravar alteração em arquivo, banco ou app quando a pessoa solicitar e a ferramenta permitir.

## Marcas múltiplas e isolamento

- Identificar `brand_id` e `display_name` antes de escrever.
- Distinguir **emissor** (quem publica), **referenciado** (de quem o post fala) e **canal**. Um repost feito por alguém sobre uma marca não é publicação da própria marca.
- Nunca usar público, logotipo, relacionamento empresarial, hashtags, histórias pessoais, resultados, contratos ou benefícios de uma marca em outra sem autorização explícita.
- Se a pessoa pedir "escreva no estilo de X", adaptar **características** de tom, mas não atribuir falsamente autoria, parceria ou oferta a X.
- Se o contexto conflitar, preferir o pedido atual. Perguntar qual marca publica apenas se isso alterar materialmente a resposta.

## Revisões e evolução

Definir uma versão de ficha e registrar no texto/exportação: alteração pedida, data e origem da decisão. Tratar amostras aprovadas como referência mais forte que exemplos gerados sem aprovação. Não declarar um perfil "aprovado" sem a pessoa ter aprovado.

## Saída recomendada de configuração

- Parágrafo de posicionamento claro.
- Cartão compacto de voz: 4 traços + como escrever + como não escrever + duas frases de exemplo.
- Objetivo e público priorizados.
- Lacunas que afetam afirmações publicáveis.
- Ficha JSON opcional quando solicitada, nunca obrigatória para gerar um post.
