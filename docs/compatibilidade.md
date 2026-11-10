# Compatibilidade: o que e nativo, o que e portátil

O Marketing Hub não é um modelo nem um aplicativo web conectado a todas as IAs. O recurso principal é uma skill em formato `SKILL.md`, acompanhada de uma instrução autocontida que pode ser copiada em qualquer IA capaz de processar texto.

| Ambiente | Integracao documentada | Como usar | Status desta distribuição |
|---|---|---|---|
| OpenAI Codex | Agent Skills | instalar em `.agents/skills/` | formato preparado, não testado ponta a ponta |
| Claude Code | Agent Skills | instalar em `.claude/skills/` | formato preparado, não testado ponta a ponta |
| Gemini CLI | Agent Skills | instalar em `.gemini/skills/` | formato preparado, não testado ponta a ponta |
| GitHub Copilot | Agent Skills em clientes compatíveis | instalar em `.github/skills/` | formato preparado, não testado ponta a ponta |
| Cursor | regras/contexto, variavel por versão | ler `.cursor/rules/` ou prompt | fallback fornecido |
| ChatGPT, Claude, Gemini (web) | campos de instrução ou mensagens | colar `prompts/marketinghub-universal.md` | fallback textual, não nativo |
| LLM local ou outro chat | prompt de texto | colar prompt + briefing | resultado depende do modelo |

O instalador cópia arquivos; ele não detecta nem instala o cliente de IA em si. Caminhos e modos podem mudar em novas versões, por isso confira a documentação oficial.

## Fontes oficiais consultadas (novembro de 2026)

- OpenAI: https://learn.chatgpt.com/docs/build-skills
- Visual Studio Code (suporte a diferentes clientes): https://code.visualstudio.com/docs/agent-customization/agent-skills
- Gemini CLI: https://geminicli.com/docs/cli/skills/

**Não declaramos testes reais em todos os provedores.** A existencia de um padrão de arquivos não significa que todos os produtos o suportem na interface web ou que recursos como geracao de imagem e publicação estejám incluídos.
