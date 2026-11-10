# Modelo de perfil de marca — regras e interoperabilidade

## Filosofia

O perfil é uma **ficha portável**, não um cadastro obrigatório. Seu papel é reduzir inconsistências entre conversas e autores quando fornecido como arquivo de projeto ou anexado ao chat. O MarketingHub não possui banco de marcas próprio; não afirmar que uma alteração foi persistida sem execução real.

## Núcleo de identidade

| Campo | Obrigatório para ficha formal? | Observação |
|---|---|---|
| `brand_id` | Sim | Slug local, exclusivo no conjunto de perfis informado |
| `display_name` | Sim | Nome pelo qual a marca se apresenta |
| `brand_type` | Sim | `company`, `personal`, `nonprofit`, `product`, `other` |
| `description` | Sim | O que oferece ou comunica, sem promessas não comprovadas |
| `primary_audience` | Sim | Público que a marca quer alcançar |
| `default_language` | Sim | Ex. `pt-BR`, `en-US`; respeitar idioma do pedido atual |
| `voice.attributes` | Sim | Até cinco adjetivos, úteis se exemplificados |
| `voice.sample_rules` | Sim | Instruções concretas sobre ritmo, termos e sintaxe |
| `channels` | Não | Canais ativos conhecidos, não presumir presença |
| `goals` | Não | Objetivos da produção editorial |
| `offers` | Não | Ofertas confirmadas e alegações permitidas |
| `visual_identity` | Não | Paleta, tipografia, logo e referências, quando fornecidos |
| `editorial_limits` | Não | Assuntos, promessas, claims, estilo a evitar |
| `source_notes` | Não | Evidência, data e grau de certeza |

JSON Schema em `templates/brand-profile.schema.json`. A ficha exemplo vazia está em `templates/brand-profile.template.json`.

## Regra de evidências

Quando um material afirma que a marca é "líder do mercado", "a mais rápida" ou "a primeira", não repetir sem fonte sólida. Perguntar por comprovação ou substituir por descrição funcional. Não usar popularidade, preço, tempo de entrega, datas, resultados e depoimentos sem fonte adequada. Registrar origem material quando houver.

Marcar internamente:

- **Confirmado:** fornecido diretamente pela pessoa como política/posição da marca ou verificado em fonte pertinente.
- **Inferido:** proposta editorial, hipótese sobre tom, ou sugestão que ainda precisa de validação.
- **Desconhecido:** não foi fornecido nem verificado; não apresentar como fato.

A opinião ou escolha editorial da pessoa pode ser confirmada como preferência; isso não confirma fatos do mundo afirmados na preferência.

## Perfis pessoais

Em `brand_type=personal`, priorizar valores e histórias efetivamente fornecidos, objetivos profissionais, linguagem e limites pessoais. Não inferir idade, formação, biografia, vivências ou cargos. Não inventar "eu estava lá" nem depoimentos em nome da pessoa.

## Instruções de edição da ficha

- Preservar campos que não foram alterados.
- Atualizar `updated_at` apenas quando houver alteração real e data conhecida.
- Trocar `brand_id` apenas a pedido, verificando conflitos.
- Não enviar um perfil de cliente a outra marca nem anexá-lo a conteúdo público.
- O arquivo pode ser validado pelo script `scripts/validate_brand_profile.py`, quando houver execução de código; se não houver, conferir manualmente ou explicar limitação.

## Níveis de maturidade

- **Rascunho**: perfil parcial, suficiente para conteúdo piloto; lacunas abertas.
- **Calibrado**: amostras reais de voz e regras explícitas, testadas em 2 peças.
- **Operacional**: canais, objetivos, fontes, processo de aprovação e limitações definidos.

Nenhum nível autoriza publicação automática.
