<p align="center"><img src="assets/brand/marketinghub-horizontal.png" width="380" alt="Marketing Hub"></p>

# Conteúdo e social media com a voz da sua marca

Cole textos que sua marca aprova, organize um cartão de voz e use-o para escrever ou revisar posts, legendas, roteiros e respostas. O **Marketing Hub** orienta o assistente de IA que você já utiliza.

**[Abrir o prompt para copiar](prompts/marketinghub-universal.md)** · [Como usar](#comece-sem-instalar) · [Versão oficial](https://github.com/paulopizzatto-del/marketing-hub/releases/latest) · [Ajude no desenvolvimento](#ajude-no-desenvolvimento) · [English](README.en.md)

## Comece sem instalar

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

O exemplo mostra a troca de uma abstração por produto e ação concretos. Veja [amostras → cartão → texto](skills/marketinghub/references/voice-lab.md).

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

## Para equipes e clientes de agentes

A skill é única e seleciona os guias necessários. O pacote instalado contém apenas instruções, modelos, metadados e validador, sem imagens promocionais ou testes internos.

```bash
python scripts/install.py --platform codex --scope user
```

O instalador aceita destinos de clientes compatíveis; leia [instalação](docs/instalacao.md) e [compatibilidade](docs/compatibilidade.md). A cópia de arquivos foi testada; a descoberta e a qualidade em cada cliente ainda precisam de verificação. Perfis reais ficam no seu ambiente privado.

## Escopo e evidência

A documentação editorial é prioritariamente pt-BR. A instrução de idioma segue o pedido, mas isso não equivale a validação linguística em outros idiomas. Este é um kit de conteúdo/social media, não uma plataforma completa de marketing.

**Ainda não medimos se o Hub escreve melhor do que uma IA competente com o mesmo briefing.** [O piloto planejado](evaluation/pilot-144/PLAN.md) separa essa pergunta dos testes de software. Não há publicação automática, memória permanente garantida nem integração nativa universal. Pesquisa e ações externas dependem das ferramentas e permissões do assistente.

## Contribuir e verificar

Os testes de contrato usam **20 perfis fictícios e 60 textos autorados** para checar dados e sinais mecânicos, não voz de marca ou superioridade de modelos. Ficam em `tests/`; veja [o contrato e suas limitações](tests/contracts/README.md).

```bash
python scripts/check_repo.py
python -m unittest discover -s tests -v
python scripts/build_release.py
```

Veja [CONTRIBUTING](CONTRIBUTING.md), [SECURITY](SECURITY.md), [SUPPORT](SUPPORT.md) e [o mapa de correções da revisão](docs/revisao-2.3.1.md).

## Ajude no desenvolvimento

Quer contribuir com código, documentação, testes ou sugestões para o Marketing Hub? Entre em contato com **Paulo Pizzatto** pelo e-mail **[paulo.pizzatto@sdssolucoes.com.br](mailto:paulo.pizzatto@sdssolucoes.com.br)**.

Para começar, consulte o [guia de contribuição](CONTRIBUTING.md). Bugs e melhorias também podem ser registrados nas [issues do projeto](https://github.com/paulopizzatto-del/marketing-hub/issues/new/choose), sem credenciais ou dados confidenciais de clientes.

## Identidade e licenças

Artes fornecidas pelo responsável, criadas com apoio de IA sob sua direção e preservadas sem alteração de bytes. A vitrine usa a logo aprovada; o banner anterior foi [retirado de divulgação](assets/archive/v2.3.0/README.md). Consulte [procedência](assets/ASSET-PROVENANCE.md) e [termos da marca](BRAND-ASSETS-LICENSE.md).

Código e documentação: [MIT](LICENSE). Atribuição dos métodos de origem: [NOTICE](NOTICE.md). A licença de software não cobre as artes.
