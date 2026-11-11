# Instalação do Marketing Hub

O projeto tem dois modos. Escolha o que seu ambiente realmente suporta.

## Studio de briefing no navegador

O Studio é uma página HTML independente. Ele funciona **localmente, sem cadastro ou instalação de pacotes**. O GitHub exibe arquivos `.html` como código-fonte, e não como uma demonstração executável. Para usá-lo:

1. Abra [`docs/studio.html`](studio.html) no repositório.
2. No GitHub, clique em **Download raw file** (ícone de download) para salvar `studio.html` no computador. Não copie o código exibido no navegador.
3. Abra o arquivo baixado com o navegador (Chrome, Firefox, Edge ou Safari).
4. Preencha o briefing, clique em **Gerar prompt**, copie o resultado e cole no assistente de IA. Se quiser guardar o contexto, use **Baixar briefing .json**.

O arquivo prepara textos e JSON localmente; ele não conecta uma IA nem publica conteúdos. Evite inserir dados confidenciais de clientes em perfis ou exemplos que serão compartilhados. Se o projeto ativar o GitHub Pages, um endereço online poderá ser oferecido **após sua verificação**.

## 1. Sem instalação (qualquer chat com entrada de texto)

1. Abra `prompts/marketinghub-universal.md`.
2. Copie o texto completo e cole como instrução da conversa ou do assistente, se houver campo apropriado.
3. Envie sua marca, público, canal e tema. Pode começar com duas ou três frases.
4. Opcional: forneça uma ficha JSON de marca ou três exemplos aprovados.

**Importante:** o prompt não baixa automaticamente arquivos adicionais. Para respostas mais personalizadas, forneça o briefing e o perfil de marca na conversa. Não há memória permanente garantida.

## 2. Skill nativa (ambientes de agente)

Obtenha o repositório do GitHub e use Python 3 (biblioteca padrão):

```bash
python scripts/install.py --platform codex --scope user
```

Troque `codex` por `claude`, `gemini`, `copilot` ou `cursor`. Codex, Gemini, Copilot e Cursor convergem para o caminho interoperável `.agents/skills`; Claude Code usa `.claude/skills`. Para instalar somente no projeto corrente:

```bash
python scripts/install.py --platform gemini --scope project --project .
```

O instalador copia somente os arquivos de runtime e metadados. `--force` prepara uma nova cópia e preserva a instalação anterior em uma pasta de backup. Não pede credenciais nem executa modelo de IA.

### Caminhos usados

| Plataforma/alias | Projeto | Usuário |
|---|---|---|
| Codex / Gemini CLI / GitHub Copilot / Cursor | `.agents/skills/marketinghub` | `~/.agents/skills/marketinghub` |
| Claude Code | `.claude/skills/marketinghub` | `~/.claude/skills/marketinghub` |

**Cursor e outros editores:** o instalador usa `.agents/skills` para Cursor local compatível. Cloud Agents e outras superfícies podem ter regras próprias; o prompt universal continua como fallback. Não garantimos autoativação sem teste de ponta a ponta.

## 3. Plugin ChatGPT/Codex

`plugin.json` e `.codex-plugin/plugin.json` estão preparados para o formato de plugin. Rode `python scripts/build_release.py` e use o arquivo `dist/marketing-hub-plugin.zip` no fluxo de importação disponível na plataforma. Um ZIP criado localmente não significa que o plugin foi aprovado ou publicado no diretório.

## 4. Validação

```bash
python scripts/check_repo.py
python -m unittest discover -s tests -v
python scripts/build_release.py
```

Antes de instalar, leia as instruções de skills e não execute scripts de repositórios desconhecidos sem revisão. Perfis de marcas reais devem permanecer em arquivos privados.

## Schema completo (desenvolvimento)

`python -m pip install -r requirements-dev.txt`

`python skills/marketinghub/scripts/validate_brand_profile.py --require-full examples/brand-profile-ficticio.json`

O modo essencial continua funcionando sem essa dependência.
