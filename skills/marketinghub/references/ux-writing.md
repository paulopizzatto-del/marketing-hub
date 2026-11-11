# UX writing, microcopy e interface orientada à tarefa

Texto de interface é **ação funcional**. Uma mensagem simpática que não diz o que aconteceu, o que fazer ou como recuperar um erro é inadequada. Usar microcopy da marca sem sacrificar legibilidade, acessibilidade, consentimento ou controle.

## Processo

1. Definir papel do usuário, etapa do fluxo, estado atual e próxima decisão. Não redigir botão sem conhecer a ação real.
2. Perguntar o que a pessoa espera que aconteça ao tocar/clicar; evitar ações com nomes vagos como "Continuar" se houver alternativa específica.
3. Construir rótulo, texto de ajuda, estado de loading, sucesso, erro e recuperação quando fizerem parte do pedido.
4. Incluir aviso de consequência irreversível e alternativa segura antes de exclusão, cancelamento ou alteração sensível.
5. Checar idioma, termos conhecidos pelo público, comprimento responsivo, consistência, foco e leitura por tecnologias assistivas. WCAG 2.2 AA é a referência de implementação, **não conformidade automática desta skill**.
6. Validar com pessoas reais: "o que acontece se escolher isto?", "onde corrigiria?", "o que foi salvo?". Tratar erro de compreensão como falha de microcopy/fluxo a investigar.

## Casos de exemplo

| Contexto | Frase vaga | Frase proposta |
|---|---|---|
| Falha ao salvar | "Ops! Algo deu errado" | "Não foi possível salvar agora. Suas alterações continuam nesta tela. Tente novamente." **Somente se o sistema realmente preservar o conteúdo.** |
| Botão de exclusão | "Confirmar" | "Excluir relatório" com explicação de irreversibilidade **se for irreversível** |
| Busca sem resultados | "Nenhum dado" | "Não encontramos resultados para este filtro. Remova um filtro ou revise a busca." |
| Consentimento | "Aceite para uma experiência incrível" | Explicar finalidade, escolha e consequência; nunca esconder a recusa |
| Recuperação | "Erro 403" | "Você não tem permissão para abrir este conteúdo. Solicite acesso ao responsável." quando essa for a solução confirmada |

Os exemplos são condicionais: não inventar comportamento do software. Evitar "dark patterns" (urgência fabricada, consentimento confuso, vergonha na recusa, botões assimétricos enganosos).

## Critérios de revisão

- **Compreensão**: usuário consegue parafrasear ação e consequência?
- **Recuperação**: erro diz como prosseguir sem culpabilização?
- **Acessibilidade**: contraste verificado na UI real, rótulos programáticos, foco visível, teclado e descrição textual de informação visual?
- **Voz**: faz sentido no produto sem sacrificar clareza ou segurança?
- **Coerência**: microcopy bate com o comportamento implementado?

Sem protótipo ou teste, entregar uma **proposta de microcopy e critérios para QA**, não declarar que a interface está acessível ou validada.
