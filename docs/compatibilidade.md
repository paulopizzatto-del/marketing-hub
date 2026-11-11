# Compatibilidade e idioma

O Marketing Hub é uma skill e um prompt textual de conteúdo/social media. Compatibilidade de arquivos, descoberta pelo cliente, qualidade linguística e qualidade editorial são perguntas diferentes.

| Caminho | O que entregamos | Evidência disponível |
|---|---|---|
| Prompt em chat de texto | Instrução autocontida em pt-BR | Arquivo disponível; depende de contexto e capacidade do modelo |
| Codex / Gemini CLI / Copilot / Cursor | Instalador convergente em `.agents/skills` | Cópia e estrutura testadas; descoberta e execução de ponta a ponta pendentes |
| Claude Code | Instalador em `.claude/skills` | Cópia e estrutura testadas; descoberta e execução de ponta a ponta pendentes |
| Plugin importável | Manifestos e skill compacta | Pacote validado localmente; não representa aprovação em diretório |
| Outros agentes | Arquivos para avaliação de integração | Sem certificação de suporte |

## Idioma

A biblioteca é prioritariamente português brasileiro. A regra manda responder no idioma da última mensagem do usuário e produzir a peça no idioma pedido/perfil. Isso corrige a instrução, mas não comprova cinco execuções corretas em inglês. O README em inglês apresenta o projeto, não um pacote linguístico validado. Mandarim e expansão trilíngue aguardam revisão e prioridade de produto.

## Registrar um teste real

Informar cliente, versão, modelo, data, modo de instalação, entrada e resultado. Manter resultados mecânicos separados da avaliação de voz. Consulte [protocolo](testes-reais-com-modelos.md). As regras do cliente podem mudar; confira suas fontes oficiais antes de instalar.
