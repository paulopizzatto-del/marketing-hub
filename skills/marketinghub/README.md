# Marketing Hub 2.0 — Social media com identidade própria

O Marketing Hub transforma materiais de uma marca (descrição, amostras de posts, público, ofertas e preferências) em conteúdo, estratégia e análise sem impor uma personalidade genérica. Pode atender marcas comerciais, negócios locais, criadores, entidades e perfis profissionais — uma ou várias, desde que cada voz seja identificada.

## Primeiro uso

**Se quiser começar logo:** "Marketing Hub, crie uma legenda para [marca], que vende [produto], falando com [público]. Instagram, tom [adjetivos]." Uma configuração formal não é obrigatória.

**Se quiser configurar:** "Marketing Hub, monte o perfil editorial da minha marca. Aqui estão meu site, posts e briefing." Ele organiza informações fornecidas, diferencia fatos de hipóteses e, quando pedido, prepara uma ficha reutilizável em JSON.

**Se tiver várias marcas:** envie uma ficha para cada uma e indique sempre quem assina a publicação. Um texto de marca não deve herdar voz de um criador pessoal ou de outra empresa.

## Casos de uso

- "Aprenda meu tom de voz a partir destes 4 posts e crie um guia."
- "Reescreva esta legenda para Instagram, mais curta e humana, sem listas."
- "Crie 12 pautas para o próximo mês com objetivos, públicos e formatos."
- "Transforme este artigo em um roteiro de Reel de 30 segundos."
- "Planeje um carrossel educativo em seis telas, sem inventar estatísticas."
- "Revise os dados reais do meu CSV e sugira três testes editoriais."
- "Compare estas duas versões com os critérios de qualidade editorial."
- "Faça um briefing de imagem com base no meu manual de marca."

## O que acompanha o pacote

`SKILL.md` com o roteador de tarefas; `references/` com fluxos especializados; `templates/` com perfil, briefing e calendário; `scripts/` com validador independente; `tests/` com cenários de aceitação; `LICENSE`, `NOTICE.md` e `CHANGELOG.md`.

## Persistência e integrações

A instalação **não configura automaticamente marcas, não lê contas privadas e não armazena dados em servidores próprios**. O template JSON começa intencionalmente incompleto e deve ser preenchido antes da validação. O perfil é aplicado enquanto estiver disponível no contexto, arquivo ou conexão autorizada. Se a pessoa desejar reutilizá-lo em outro ambiente, exporte e reapresente a ficha. Publicar/agendar, gerar imagem, examinar sites, buscar tendências ou analisar contas depende das ferramentas e permissões disponíveis naquele ambiente.

## Instalação

- **Skill:** importe `skill.zip` se a sua plataforma permitir skills personalizadas. O diretório interno único é `marketinghub`.
- **Plugin:** `marketinghub-plugin-v2-branded.zip` contém manifesto de plugin e a skill integrada. Importe pelo criador de plugins compatível. `skill.zip` e plugin ZIP têm propósitos diferentes.
- A disponibilidade e a interface de importação variam por plataforma e plano. A validação estrutural local não garante aprovação no catálogo do produto.

## Licença e crédito

Parte da arquitetura editorial deriva dos 17 workflows públicos de Charlie Hills, MIT, com crédito em `NOTICE.md` e cópia da licença em `LICENSE`. Sem exposição de exemplos ou dados de marcas reais.

## Identidade do produto

Veja `BRAND.md`. O símbolo original e os logotipos aprovados estão em `assets/`. A ferramenta não aplica automaticamente sua identidade visual aos clientes.
