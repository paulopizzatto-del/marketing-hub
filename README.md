<p align="center">
  <img src="assets/brand/marketinghub-horizontal-fundo-rosa.png" width="750" alt="Marketing Hub — Seu marketing, num lugar só">
</p>

<p align="center">
  <strong>Conteúdo e social media com a voz da sua marca.</strong><br>
  Um cartão de voz portátil, em pt-BR, para orientar escrita, revisão e consistência sem prender sua marca a uma única plataforma.
</p>

<p align="center">
  <a href="prompts/marketinghub-universal.md"><strong>Abrir o prompt</strong></a> ·
  <a href="#comece-em-2-minutos">Começar</a> ·
  <a href="https://github.com/paulopizzatto-del/marketing-hub/releases/latest">Release oficial</a> ·
  <a href="#ajude-no-desenvolvimento">Contribuir</a> ·
  <a href="README.en.md">English</a>
</p>

---

## A ideia em uma frase

Cole textos que sua marca aprova, organize um **cartão de voz em Markdown** e use esse contexto para escrever ou revisar posts, legendas, roteiros e respostas com mais consistência.

> **Rascunho genérico:** “Soluções completas para transformar sua experiência.”  
> **Revisão orientada pelo briefing:** “Vai receber gente em casa? Você pode encomendar os pães e retirar na padaria. Chame no WhatsApp para combinar o pedido.”

Esse exemplo é fictício e mostra a abordagem — **não é benchmark de superioridade entre modelos**.

## Comece em 2 minutos

1. Abra o [prompt portátil](prompts/marketinghub-universal.md) e cole no assistente que você já usa.
2. Conte o básico da marca, do público e da tarefa.
3. Para calibrar a voz, cole **três textos aprovados** e peça o cartão de voz.
4. Peça a peça nova ou cole um rascunho para revisão.

```text
Tenho uma oficina de bicicletas. Vou colar três posts aprovados.
Identifique nosso jeito de escrever e revise a legenda que envio depois,
sem acrescentar serviços ou promessas.
```

Para uma peça pontual, você pode começar direto pelo briefing — sem cadastro e sem criar perfil antes.

## O que o Hub organiza

| | Capacidade | Entrega |
|---|---|---|
| ✦ | **Voz de marca** | Cartão em Markdown extraído de amostras e regras observáveis |
| ✎ | **Escrita e revisão** | Posts e legendas com fatos, preferências e autocrítica curta de voz |
| ◫ | **Pautas** | Temas, reaproveitamento e organização editorial |
| ▶ | **Vídeos curtos** | Roteiros, cenas, ganchos e legendas |
| ◇ | **Briefing visual** | Hierarquia, sequência e orientação de produção |
| ☵ | **Comunidade e perfil** | Respostas, bio e clareza de apresentação |
| ∿ | **Métricas** | Leitura dos dados fornecidos com denominadores definidos |

## Feito para levar a voz com você

O diferencial pretendido do Marketing Hub é simples: **o cartão de voz é seu**. Ele fica em um arquivo Markdown legível, editável e reutilizável.

Quando o ambiente aceita skills, o instalador usa caminhos compatíveis com agentes atuais; quando não aceita, o prompt portátil continua disponível.

```bash
python scripts/install.py --platform codex --scope user
```

Leia [instalação](docs/instalacao.md) e [compatibilidade](docs/compatibilidade.md). A cópia e o empacotamento foram testados; descoberta e qualidade em cada cliente continuam dependentes do ambiente e precisam de validação própria.

<p align="center">
  <img src="assets/brand/previa-marca.png" width="720" alt="Prévia da identidade visual do Marketing Hub">
</p>

## Segurança editorial antes de publicar

O avaliador não “certifica” um texto. Ele separa:

- **erros bloqueantes**, como sinais de credenciais, mistura de marcas e placeholders;
- **revisão humana obrigatória**, como percentuais sem evidência, preços/ofertas, superlativos objetivos, depoimentos e alguns dados pessoais aparentes;
- **avisos de formato**, que não transformam preferência editorial em erro de segurança.

As regras de marca vêm do cartão/perfil, em vez de depender das fixtures sintéticas usadas nos testes internos.

## Escopo e evidência

A biblioteca editorial é prioritariamente **pt-BR**. O conteúdo pode seguir o idioma solicitado, mas isso não equivale a validação linguística nativa em todos os mercados.

Este é um kit de **conteúdo e social media**, não uma plataforma completa de marketing. Não há publicação automática, memória permanente garantida nem integração nativa universal.

**Ainda não demonstramos que o Hub escreve melhor do que uma IA competente recebendo o mesmo briefing e as mesmas amostras.** O [piloto controlado](evaluation/pilot-144/PLAN.md) existe justamente para responder isso sem transformar testes de software em prova editorial.

## Engenharia verificável

Os testes de contrato usam fixtures sintéticas autoradas somente para checar dados, isolamento e sinais mecânicos. Eles não medem voz de marca nem superioridade de modelos.

```bash
python scripts/check_repo.py
python -m unittest discover -s tests -v
python scripts/build_release.py
```

Consulte [o contrato de testes](tests/contracts/README.md), [a revisão 2.3.2](docs/revisao-2.3.2.md), [SECURITY](SECURITY.md) e [SUPPORT](SUPPORT.md).

## Ajude no desenvolvimento

Quer contribuir com código, documentação, testes ou sugestões? Fale com **Paulo Pizzatto** em **[paulo.pizzatto@sdssolucoes.com.br](mailto:paulo.pizzatto@sdssolucoes.com.br)**.

Veja o [guia de contribuição](CONTRIBUTING.md) ou abra uma [issue](https://github.com/paulopizzatto-del/marketing-hub/issues/new/choose), sem credenciais ou dados confidenciais de clientes.

## Identidade e licenças

<p>
  <img src="assets/brand/marketinghub-horizontal.png" width="430" alt="Logo Marketing Hub">
  <br>
  <img src="assets/brand/marketinghub-horizontal-fundo-escuro.png" width="520" alt="Marketing Hub em fundo escuro">
</p>

Artes fornecidas pelo responsável, criadas com apoio de IA sob sua direção e preservadas sem alteração de bytes. O banner antigo foi [retirado de divulgação](assets/archive/v2.3.0/README.md). Consulte [procedência](assets/ASSET-PROVENANCE.md), [identidade visual](docs/identidade-visual.md) e [termos da marca](BRAND-ASSETS-LICENSE.md).

Código e documentação: [MIT](LICENSE). Atribuição dos métodos de origem: [NOTICE](NOTICE.md). A licença de software não cobre as artes.
