<p align="center">
  <img src="assets/brand/marketinghub-horizontal-fundo-rosa.png" width="620" alt="Marketing Hub — identidade oficial sobre fundo rosa">
</p>

<h1 align="center">Mais contexto na criação. Mais critério na revisão.</h1>

<p align="center"><strong>Um kit editorial open-source para transformar estratégia, fatos e voz de marca em conteúdo revisável.</strong></p>

<p align="center">
  <a href="docs/studio.html"><strong>Preparar um briefing no Studio</strong></a> ·
  <a href="prompts/marketinghub-universal.md">Experimentar o prompt</a> ·
  <a href="#comece-sem-instalar">Como usar</a> ·
  <a href="https://github.com/paulopizzatto-del/marketing-hub/releases/latest">Versão pública</a> ·
  <a href="README.en.md">English</a>
</p>

> **Estado:** esta pasta descreve a **2.4.0 candidata**. A release pública continua sendo a versão apontada em [Releases](https://github.com/paulopizzatto-del/marketing-hub/releases/latest). Este material não afirma superioridade editorial comprovada.

## O que é o Marketing Hub?

O Marketing Hub é uma skill e um prompt portátil para o assistente de IA que você já usa. Ele começa pelo **público, pela proposta de valor e pelos fatos que a marca pode afirmar**, observa amostras de escrita aprovadas e orienta a produção ou a revisão de peças para canais diferentes.

A proposta é tornar o briefing mais claro, a voz mais reconhecível e a aprovação humana mais informada, sem vender o método como um modelo próprio ou uma plataforma que publica automaticamente.

## Comece sem instalar

**Studio de briefing:** [abra a ferramenta](docs/studio.html). É uma página estática que organiza oferta, público, posicionamento, fatos e três amostras para gerar um prompt e um JSON reutilizável, sem chamar IA ou enviar dados. Funciona localmente no navegador. Abra o arquivo ou, quando GitHub Pages estiver habilitado, use a página hospedada.

1. Abra o [prompt portátil](prompts/marketinghub-universal.md), copie todo o texto e cole no seu assistente.
2. Descreva o negócio, o público e a tarefa. Para calibrar a voz, cole três textos que você aprova.
3. Peça seu cartão de voz ou sua primeira peça. Guarde o cartão para os próximos pedidos.

> “Tenho uma oficina de bicicletas. Vou colar três posts aprovados. Identifique nosso jeito de escrever e revise a legenda que envio depois, sem acrescentar serviços ou promessas.”

Para uma legenda pontual, você pode começar direto pelo briefing, sem cadastro.

## Veja a abordagem

**Exemplo fictício de revisão, não comparação medida entre modelos.**

Fatos fornecidos: padaria aceita encomendas para retirada; pedidos pelo WhatsApp. Voz: próxima e direta.

**Rascunho genérico:** “Soluções completas para transformar sua experiência.”

**Revisão orientada pelo briefing:** “Vai receber gente em casa? Você pode encomendar os pães e retirar na padaria. Chame no WhatsApp para combinar o pedido.”

O exemplo mostra a troca de abstração por produto e ação concretos; não comprova melhora contra um modelo de referência. Veja [amostras → cartão → texto](skills/marketinghub/references/voice-lab.md).

## O que você pode fazer

| Capacidade | Entrega |
|---|---|
| Voz de marca | Cartão em Markdown extraído de amostras |
| Escrita e revisão | Posts e legendas com fatos e preferências do briefing |
| Pautas | Temas e reaproveitamento por objetivo |
| Vídeos curtos | Roteiros, cenas e legendas |
| Briefing visual | Hierarquia, sequência e orientação de produção |
| Comunidade e perfil | Respostas, bio e clareza de apresentação |
| Métricas | Leitura dos dados fornecidos, com denominadores definidos |
| Estratégia de marca | Público, proposta de valor, diferenciação, jornada e contexto de mercado |
| UX writing | Estados de interface, erros, recuperação, mensagens claras e revisão de acessibilidade |
| Evidência editorial | Registro de alegações, fontes, riscos e aprovação proporcional |

## Para equipes e clientes de agentes

A skill é única e seleciona os guias necessários. O pacote instalado contém apenas instruções, modelos, metadados e validador, sem imagens promocionais ou testes internos.

```bash
python scripts/install.py --platform codex --scope user
```

O instalador aceita destinos de clientes compatíveis; leia [instalação](docs/instalacao.md) e [compatibilidade](docs/compatibilidade.md). A cópia de arquivos foi testada; a descoberta e a qualidade em cada cliente ainda precisam de verificação. Perfis reais ficam no seu ambiente privado.

## Escopo e evidência

A documentação editorial é prioritariamente pt-BR. A instrução de idioma segue o pedido, mas isso não equivale a validação linguística em outros idiomas. É um kit editorial estratégico, não uma plataforma de publicação, CRM ou analytics conectado.

**Ainda não medimos se o Hub escreve melhor do que uma IA competente com o mesmo briefing.** [O programa de 50 marcas em preparação](evaluation/lab50/README.md) separa essa pergunta dos testes de software. Não há publicação automática, memória permanente garantida nem integração nativa universal. Pesquisa e ações externas dependem das ferramentas e permissões do assistente.

## Contribuir e verificar

Os [testes de contrato](tests/contracts/README.md) verificam regras mecânicas, isolamento e integridade. **Não medem a qualidade editorial produzida por modelos reais.**

```bash
python scripts/check_repo.py
python -m unittest discover -s tests -v
python scripts/build_release.py
```

Veja [o guia estratégico 2.4](docs/guia-estrategico-2.4.md), [a autoavaliação](docs/autoavaliacao-2.4.md), [CONTRIBUTING](CONTRIBUTING.md), [SECURITY](SECURITY.md) e [SUPPORT](SUPPORT.md).

## Ajude no desenvolvimento

Quer contribuir com código, documentação, testes ou sugestões para o Marketing Hub? Entre em contato com **Paulo Pizzatto** pelo e-mail **[paulo.pizzatto@sdssolucoes.com.br](mailto:paulo.pizzatto@sdssolucoes.com.br)**.

Para começar, consulte o [guia de contribuição](CONTRIBUTING.md). Bugs e melhorias também podem ser registrados nas [issues do projeto](https://github.com/paulopizzatto-del/marketing-hub/issues/new/choose), sem credenciais ou dados confidenciais de clientes.

## Identidade e licenças

Artes fornecidas pelo responsável, criadas com apoio de IA sob sua direção e preservadas sem alteração de bytes. A vitrine usa **uma única assinatura visual legível em temas claro e escuro**, sem prancha de variações; o banner anterior foi [retirado de divulgação](assets/archive/v2.3.0/README.md). Consulte [procedência](assets/ASSET-PROVENANCE.md) e [termos da marca](BRAND-ASSETS-LICENSE.md).

Código e documentação: [MIT](LICENSE). Atribuição dos métodos de origem: [NOTICE](NOTICE.md). A licença de software não cobre as artes.