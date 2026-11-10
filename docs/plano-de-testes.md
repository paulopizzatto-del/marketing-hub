# Beta: validacoes antes de anunciar compatibilidade total

Os testes automaticos verificam estrutura, ZIP, exemplo de marca e instalador. Eles **não** avaliam qualidade editorial nem provam suporte real de todas as IAs.

## Cenarios manuais recomendados

1. Perfil novo com briefing pequeno: gerar legenda sem impor formulario.
2. Perfil com três amostras reais (sem dados pessoais): extrair estilo e preservar tom.
3. Duas marcas de segmentos diferentes: não cruzar ofertas, tons nem hashtags.
4. Texto a encurtar: preservar o argumento e eliminar repetições.
5. Foto e legenda: evitar repetir apenas o titulo da imagem.
6. LinkedIn profissional: sem pretender ter experiências que o usuário não relatou.
7. Instagram para pequeno negócio: CTA natural e linguagem simples.
8. Calendário: distribuir pilares editoriais, sem duplicar pautas.
9. Roteiro de Reels: caber no tempo, com cenas e fala naturais.
10. Carrossel: progressao de ideias e leitura no celular.
11. Pesquisa sem acesso web: admitir limite e não inventar tendencias recentes.
12. Analytics: exigir dados reais e não fabricar métricas.
13. Setor regulado: evitar alegações e garantias sem base.
14. Pergunta de instalação: distinguir skill, prompt e plugin.
15. Ambiente sem arquivos: usar prompt universal com contexto colado.
16. Repetir caso em duas IAs distintas e verificar se as instruções centrais se mantem.

**Status em 2026-11-10:** além destes cenários qualitativos, criamos uma matriz offline com 20 marcas fictícias e três amostras por marca (60/60 passaram após duas correções). Os exemplos foram autorados para testar um contrato editorial; **não foram executados em modelos de IA externos**. Consulte [`qa-20-marcas.md`](qa-20-marcas.md). Registrar resultados reais por IA, versão, briefing, saída, acertos e falhas antes do lançamento público.

Veja também [`testes-reais-com-modelos.md`](testes-reais-com-modelos.md) para executar os 60 briefings e avaliar saídas de cada IA.
