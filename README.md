<p align="center">
  <img src="assets/brand/marketinghub-horizontal-fundo-rosa.png" alt="Marketing Hub — identidade oficial sobre fundo rosa" width="620">
</p>

<h1 align="center">Escreva com a voz da marca. Não com a voz de qualquer IA.</h1>

<p align="center">
  <strong>Um kit editorial open-source para orientar conteúdo e social media com amostras reais, contexto e revisão.</strong>
</p>

<p align="center">
  <a href="prompts/marketinghub-universal.md"><strong>Experimentar sem instalar</strong></a>
  · <a href="#comece-por-aqui">Começar</a>
  · <a href="https://github.com/paulopizzatto-del/marketing-hub/releases/latest">Baixar a versão oficial</a>
  · <a href="README.en.md">English</a>
</p>

---

## O que é o Marketing Hub?

O **Marketing Hub** é uma skill e um prompt portátil que organizam a forma como sua marca se comunica. Em vez de pedir à IA apenas “escreva uma legenda criativa”, você fornece fatos, objetivo, público e textos que a marca já aprovou. O Hub transforma essas referências em um **cartão de voz editável** e usa esse contexto para criar ou revisar conteúdo.

**A proposta:** menos decisões editoriais no improviso, mais consistência e controle sobre aquilo que será publicado. O texto final continua dependendo do briefing, do modelo utilizado e da revisão humana.

### O que você recebe

| Recurso | Para que serve |
| :--- | :--- |
| **Cartão de voz** | Registrar ritmo, vocabulário, tom, escolhas recorrentes e o que evitar |
| **Escrita e revisão** | Produzir posts, legendas, respostas e roteiros com referência à voz e aos fatos fornecidos |
| **Pautas e adaptação** | Organizar ideias, variar ângulos e adaptar mensagens a canais |
| **Briefing visual** | Planejar hierarquia, sequência e orientação editorial para peças |
| **Análise de métricas** | Interpretar dados fornecidos, com definições e denominadores explícitos |
| **Revisão de riscos** | Sinalizar alegações, credenciais, dados pessoais aparentes e possíveis conflitos entre marcas |

## Comece por aqui

**Sem instalação (recomendado para a primeira experiência):**

1. [Abra o prompt portátil](prompts/marketinghub-universal.md) e copie seu conteúdo para um assistente de texto.
2. Informe **marca, público, objetivo e fatos confirmados**. Para calibrar a voz, acrescente três textos previamente aprovados.
3. Peça um cartão de voz e, em seguida, uma peça nova ou a revisão de um rascunho.

```text
Tenho uma pequena oficina de bicicletas.
Público: pessoas que usam bicicleta no dia a dia.
Objetivo: avisar sobre o novo horário de atendimento.
Vou enviar três textos aprovados para você identificar nossa voz.
Não invente preços, serviços nem horários; pergunte o que faltar.
```

**Com skill instalada:** para ambientes que aceitam esse formato, confira [instalação](docs/instalacao.md) e [compatibilidade](docs/compatibilidade.md). Um exemplo de instalação local é:

```bash
python scripts/install.py --platform codex --scope user
```

O prompt portátil pode funcionar em assistentes que aceitam instruções coladas. **Instalação de arquivos não garante descoberta da skill nem desempenho idêntico em cada cliente.**

## Como fica na prática?

**Exemplo ilustrativo e fictício**, não resultado de experimento comparativo.

**Informações confirmadas:** padaria recebe encomendas para retirada; pedidos são combinados pelo WhatsApp. **Voz desejada:** próxima, simples, sem exageros.

| Rascunho genérico | Revisão com contexto |
| :--- | :--- |
| “Soluções completas para transformar sua experiência.” | “Vai receber gente em casa? Você pode encomendar os pães e retirar na padaria. Chame no WhatsApp para combinar o pedido.” |

A revisão troca expressões vagas por informações verificáveis e um próximo passo concreto. Veja o [exemplo completo de amostras → cartão de voz → peça](skills/marketinghub/references/voice-lab.md).

## Antes de publicar: o que o Hub verifica?

O conjunto de verificações pode apontar **sinais de segurança**, **alegações que precisam de comprovação** e **preferências de formato**. Ele não substitui uma revisão jurídica ou editorial, não garante ausência de erros e não “certifica” conteúdo.

O processo recomenda preservar as amostras originais, separar marcas, conferir afirmações comerciais e revisar a peça quando as informações disponíveis forem insuficientes.

## Escopo, compatibilidade e evidências

| Questão | Estado atual |
| :--- | :--- |
| **Versão pública** | [2.3.2](https://github.com/paulopizzatto-del/marketing-hub/releases/tag/v2.3.2) |
| **Idioma principal** | Português brasileiro; outros idiomas dependem de validação |
| **Publicação automática** | Não incluída |
| **Conexão direta a redes sociais/CRM** | Não incluída por padrão |
| **Memória permanente entre conversas** | Não garantida |
| **Qualidade superior a uma IA bem instruída** | **Ainda não demonstrada** por comparação real controlada |

O código tem [testes de contrato e integridade](tests/contracts/README.md), mas esses testes **não são uma avaliação humana da qualidade dos textos**. O [protocolo de comparação](evaluation/pilot-144/PLAN.md) foi criado justamente para medir ganho incremental sem transformar fixtures sintéticas em publicidade.

## Documentação para uso e desenvolvimento

**Para começar:** [instalação](docs/instalacao.md) · [compatibilidade](docs/compatibilidade.md) · [FAQ](docs/faq.md) · [perfil de marca](docs/perfil-de-marca.md)

**Para auditar:** [arquitetura](docs/arquitetura.md) · [testes reais com modelos](docs/testes-reais-com-modelos.md) · [segurança](SECURITY.md) · [guia de contribuição](CONTRIBUTING.md)

Para reproduzir as verificações técnicas no repositório:

```bash
python scripts/check_repo.py
python -m unittest discover -s tests -v
python scripts/build_release.py
```

## Ajude a desenvolver o Marketing Hub

Sugestões, correções, testes de usabilidade e contribuições são bem-vindos nas [issues](https://github.com/paulopizzatto-del/marketing-hub/issues) e no [guia de contribuição](CONTRIBUTING.md). Contato para colaboração: **[paulo.pizzatto@sdssolucoes.com.br](mailto:paulo.pizzatto@sdssolucoes.com.br)**.

## Identidade, autoria e licenças

A identidade é usada uma única vez como assinatura visual nesta página. As demais variações permanecem disponíveis para referência, **sem transformar o README em uma prancha de logos**. Confira o [guia de aplicação da marca](docs/identidade-visual.md), a [procedência dos assets](assets/ASSET-PROVENANCE.md) e os [termos específicos das artes](BRAND-ASSETS-LICENSE.md).

Código e documentação: [MIT](LICENSE). Métodos e atribuições: [NOTICE](NOTICE.md). **A licença MIT não inclui as artes de marca.** As imagens foram fornecidas pelo responsável e criadas com apoio de IA sob sua direção.
