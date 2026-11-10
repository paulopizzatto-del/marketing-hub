<p align="center">
  <img src="assets/banner.png" alt="Marketing Hub: identidade adaptável, criação de conteúdo, planejamento e estrutura portátil para diferentes assistentes de IA" width="100%">
</p>

<p align="center">
  <strong>Seu marketing, num lugar só.</strong><br>
  Conteúdo e estratégia com a personalidade da sua marca, sem complicação.
</p>

<p align="center">
  <a href="#como-começar">Como começar</a> ·
  <a href="#o-que-tem-aqui">Arquivos do projeto</a> ·
  <a href="#compatibilidade">Compatibilidade</a> ·
  <a href="README.en.md">English</a> ·
  <a href="docs/index.html">Vitrine</a> ·
  <a href="https://github.com/paulopizzatto-del/marketing-hub/releases/tag/v2.3.0-beta.1">Baixar beta</a> ·
  <a href="docs/faq.md">FAQ</a>
</p>

<p align="center"><strong>Marketing Hub 2.3.0 · prévia pública (beta)</strong><br>
Uma ferramenta editorial aberta para aprender a voz da sua marca. Sem promessas de viralização ou de compatibilidade idêntica entre IAs.</p>

---

## O que é

O **Marketing Hub** reúne uma skill editorial e um prompt portátil para ajudar a planejar, criar e revisar conteúdos com o jeito de falar de **cada marca**. Você pode pedir ideias, legendas, roteiros de Reels, campanhas, calendários e análise de materiais já existentes.

Você fornece o contexto: o que seu negócio faz, seu público, seu tom e exemplos de comunicação. O Marketing Hub usa isso como referência. **Não impõe a mesma voz a todas as marcas e não armazena automaticamente um perfil entre conversas.**

Os recursos editoriais foram organizados a partir de **17 métodos de social media**, em uma única skill generalista. O resultado depende do modelo utilizado, do briefing e das ferramentas disponíveis.

## Por que usar

- **Identidade adaptável:** respeita o posicionamento, o vocabulário e as preferências da marca.
- **Produção prática:** sugere posts, legendas, roteiros, comentários, campanhas e revisões.
- **Planejamento com critério:** estrutura pautas e calendários sem inventar resultados ou tendências.
- **Dois modos de uso:** skill nativa em ambientes compatíveis ou prompt em assistentes de IA que aceitam texto.
- **Distribuição aberta do projeto:** documentação, modelos, testes e versões organizados no GitHub.

**Para quem:** agências, equipes de marketing, freelancers, pequenos negócios e criadores independentes.

## Como começar

**[Acessar os pacotes do beta](https://github.com/paulopizzatto-del/marketing-hub/releases/tag/v2.3.0-beta.1)** — skill, plugin e código-fonte. Você também pode usar o prompt portátil sem instalar nada.


### Opção A — Sem instalar nada

1. Abra [`prompts/marketinghub-universal.md`](prompts/marketinghub-universal.md) e copie todo o conteúdo.
2. Cole as instruções no assistente de IA que você já usa.
3. Apresente a sua marca e peça uma tarefa. Por exemplo:

> Tenho uma cafeteria de bairro. Meu público é a vizinhança e gosto de um tom acolhedor, direto e sem frases prontas. Me dá cinco ideias de post para esta semana.

Esse caminho é **portátil**, não uma integração nativa com todas as IAs. Se abrir outra conversa ou usar outro modelo, talvez seja necessário informar o contexto novamente.

### Opção B — Instalar como skill

Na página do repositório, clique em **Code → Download ZIP**, extraia o projeto e abra um terminal dentro da pasta `marketing-hub`. Com Python 3:

```bash
python scripts/install.py --platform codex --scope user
```

Troque `codex` por `claude`, `gemini` ou `copilot`, conforme o **cliente local compatível** que utiliza. O instalador copia os arquivos da skill; ele não instala o aplicativo de IA. Consulte o [passo a passo](docs/instalacao.md).

### Personalize a voz da sua marca

Para uso recorrente, comece pelo [`modelo de perfil de marca`](skills/marketinghub/templates/brand-profile.template.json) ou pelos [exemplos de configuração](docs/perfil-de-marca.md). Você também pode fornecer um briefing simples, sem precisar de JSON.

> **Privacidade:** nunca publique no repositório perfis reais de clientes, senhas, tokens ou dados confidenciais. A ficha de exemplo é fictícia.

## O que tem aqui

```text
marketing-hub/
├── assets/                         artes e logos originais fornecidos pelo criador
│   ├── banner.png
│   ├── icone.png
│   └── social-preview-1280x640.png
├── skills/marketinghub/             skill canônica, referências e modelos
├── prompts/marketinghub-universal.md
├── docs/                           instalação, compatibilidade e vitrine
├── examples/                       exemplos fictícios, sem dados de clientes
├── scripts/                        instalador, verificações e releases
├── tests/                          testes automatizados
├── .github/                        CI, modelos de issues e PRs
└── plugin.json                     manifesto para importação compatível
```

## Compatibilidade

| Ambiente | Como utilizar | Situação |
|---|---|---|
| Codex | Skill em `.agents/skills/` | Estrutura e instalador testados localmente; cliente não testado de ponta a ponta |
| Claude Code | Skill em `.claude/skills/` | Estrutura e instalador testados localmente; cliente não testado de ponta a ponta |
| Gemini CLI | Skill em `.gemini/skills/` | Estrutura e instalador testados localmente; cliente não testado de ponta a ponta |
| GitHub Copilot compatível | Skill em `.github/skills/` | Estrutura e instalador testados localmente; depende do cliente |
| ChatGPT, Claude e Gemini na web | Prompt de texto | Caminho portátil; integração nativa não garantida |
| Outros assistentes de texto | Prompt de texto | Depende do modelo e dos limites de contexto |

Veja a [matriz de compatibilidade](docs/compatibilidade.md). **O Marketing Hub não publica nem agenda posts automaticamente, não acessa contas e não promete viralização.** Isso exige integrações externas autorizadas.

## Exemplo de uso

O projeto traz um [briefing de uma cafeteria fictícia](examples/brief-instagram.md), com entrada e texto de demonstração. É **um exemplo ilustrativo, não um case real nem prova de desempenho**.

Para avaliar a qualidade em situações reais, experimente diferentes marcas e compare o resultado com textos aprovados por cada negócio. Veja o [plano de testes](docs/plano-de-testes.md).

## Como contribuir

Correções, melhorias em linguagem, testes de compatibilidade e novos modelos são bem-vindos. Leia [`CONTRIBUTING.md`](CONTRIBUTING.md) e [`SECURITY.md`](SECURITY.md) antes de abrir um pull request ou relatar vulnerabilidades.

Confira a [auditoria de 20 marcas fictícias](docs/qa-20-marcas.md), com 60 amostras editoriais e limitações explicitadas. Para validar saídas reais, use o [protocolo multimodelo](docs/testes-reais-com-modelos.md). **Os testes offline não comprovam desempenho em todos os modelos.** A edição 2.3.0 é uma prévia pública: ainda falta a avaliação controlada das respostas reais de cada provedor. Veja [limites e próximos passos](docs/lancamento-publico.md).

Rode as verificações locais:

```bash
python scripts/check_repo.py
python -m unittest discover -s tests -v
```

## Identidade visual

<p align="center">
  <img src="assets/brand/marketinghub-horizontal.png" alt="Assinatura horizontal original do Marketing Hub" width="360">
</p>

Todas as imagens publicadas neste repositório são **arquivos fornecidos pelo responsável pelo projeto**, preservados sem geração, alteração ou substituição. O banner, o ícone e a imagem de compartilhamento vêm do kit oficial enviado para o GitHub. Consulte o [guia de aplicação](docs/identidade-visual.md) e o [registro de procedência dos arquivos](assets/ASSET-PROVENANCE.md).

O social preview é configurado manualmente nas definições do GitHub usando [`assets/social-preview-1280x640.png`](assets/social-preview-1280x640.png); incluí-lo no repositório não o ativa automaticamente.

## Ajuda e evolução

Veja as [perguntas frequentes](docs/faq.md), o [roteiro de evolução](docs/roadmap.md) e o [suporte](SUPPORT.md). Para colaboração, use issues e pull requests sem enviar informações confidenciais.

## Licença e créditos

O projeto inclui uma licença [MIT](LICENSE) para código e documentação, **para código e documentação; as artes ficam sob termos separados**. O logotipo e as artes da marca têm termos separados em [`BRAND-ASSETS-LICENSE.md`](BRAND-ASSETS-LICENSE.md). A adaptação editorial atribui os métodos originais de *Social Media Skills for AI Agents*, de Charlie Hills, em [`NOTICE.md`](NOTICE.md).

---

<p align="center">
  <img src="assets/icone.png" width="44" alt="Ícone original do Marketing Hub"><br>
  <sub>Feito para criar comunicação com clareza, personalidade e método.</sub>
</p>
