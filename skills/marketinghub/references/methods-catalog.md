# Mapa de atribuição dos métodos de origem

**Proveniência:** *Social Media Skills for AI Agents*, Charlie Hills (2026), MIT. Fonte recebida do usuário. Os métodos foram reescritos e reorganizados para uso **genérico por qualquer marca**, sem a dependência original de LinkedIn, British English, Claude, Codex, Gemini, Apify, templates de um criador ou chaves de API específicas. Licença preservada em `LICENSE` e atribuição em `NOTICE.md`.

| # | Método | Princípio operacional implementado | Módulo de destino |
|---|---|---|---|
| 1 | `voice-builder` | Aprender atributos de voz por amostras e comparação; gerar ficha portável | `onboarding.md`, `voice-lab.md` |
| 2 | `newsletter-voice` | Manter promessa, abertura e ritmo de newsletter de modo consistente | `community-formats.md` |
| 3 | `profile-optimizer` | Revisar headline, resumo, destaques e clareza da proposta sem inventar currículo | `community-formats.md` |
| 4 | `post-writer` | Público + objetivo + ângulo + fatos + revisão -> post publicável | `copywriting.md` |
| 5 | `graphic-designer` | Decidir mensagem visual, hierarquia e formato, com QA móvel | `visual-production.md` |
| 6 | `post-scorer` | Revisar hook, voz, utilidade, ritmo, fechamento e suporte factual | `quality-assurance.md` |
| 7 | `reels-scripting` | Roteiro por tempo/cena ou legenda de vídeo, sem scraping obrigatório | `video-reels.md` |
| 8 | `youtube-thumbnail` | Capa coerente com vídeo, tipografia grande e foco claro | `visual-production.md` |
| 9 | `pinned-comment` | Complementar publicação com comentário útil ou humor contextual | `community-formats.md` |
| 10 | `hook-generator` | Explorar ganchos de famílias diferentes sem clickbait | `copywriting.md` |
| 11 | `post-formatter` | Aplicar PAS/AIDA/BAB/STAR/SLAY apenas se estrutura ajudar | `copywriting.md` |
| 12 | `content-matrix` | Cruzar pilares editoriais e formatos por público e objetivo | `strategy-research.md` |
| 13 | `niche-research` | Pesquisar fontes atuais, datas e oportunidades verificáveis | `strategy-research.md` |
| 14 | `gemini-infographic` | Converter conteúdo factual em hierarquia visual, sem serviço obrigatório | `visual-production.md` |
| 15 | `gemini-carousel` | Narrativa em sequência, uma ideia por página e revisão do conjunto | `visual-production.md` |
| 16 | `quote-post` | Frases curtas originais e atribuições verificáveis | `visual-production.md` |
| 17 | `analytics-dashboard` | Auditoria de exportações, métricas consistentes e testes editoriais | `analytics-experiments.md` |

## Seleção de referências por intenção

1. **Legenda simples:** 4 + 10 + 11 + 6 (sem expor nomes dos métodos ao usuário).
2. **Configurar marca:** 1 + 4 + 6, aprofundar perfis pessoais ou newsletters se necessário.
3. **Planejamento editorial:** 12 + 13 + 6; 17 apenas quando houver dados reais.
4. **Reel:** 7 + 10 + 6; arte/capa sob demanda.
5. **Arte/carrossel:** 5 + 14/15/16/8 conforme o formato; revisar legibilidade.
6. **Comunidade/repost:** 9 + 4 + 6; foco em autoria e relevância.
7. **Performance:** 17 + 12, com dados reais e hipóteses testáveis.

## O que foi deliberadamente descartado

- Dependência de `about-me.md`, `voice.md` ou um projeto específico para cada ação.
- A obrigação de sempre entrevistar, pedir aprovação intermediária ou usar arquivos mesmo numa legenda simples.
- Hooks chamados de clickbait, estruturas repetitivas, afirmações de viralização e previsão de algoritmo.
- Idioma inglês imposto, números fixos de palavras, emojis e hashtags universais.
- Integrações fictícias ou credenciais exigidas só para revisar um post.
- Imagem-prompt apresentada como imagem final, analytics sem dados e publicação presumida.

## Critério de qualidade da integração

Uma skill é considerada "implementada" somente quando existe **uma instrução operacional aplicável** e uma saída correspondente, não apenas uma menção ao nome. Este catálogo mapeia cada método aos workflows que efetivamente o incorporam. O pacote é uma única skill, não 17 `SKILL.md` concorrentes.

## Capacidades do produto

A vitrine apresenta sete capacidades: voz de marca; escrita/revisão; pautas; vídeos curtos; briefing visual; comunidade/perfil; métricas. Os 17 nomes acima registram a origem intelectual, não 17 produtos independentes ou evidência de desempenho.
