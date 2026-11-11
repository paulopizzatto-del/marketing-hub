# Vitrine pública do Marketing Hub no GitHub

Este guia documenta **a apresentação do projeto**, não as etapas internas da skill. A versão que está efetivamente publicada é a indicada em [Releases](https://github.com/paulopizzatto-del/marketing-hub/releases/latest).

## Primeiro contato: critérios editoriais

O visitante deve descobrir, sem rolar a página inteira:

1. **O que é:** um kit editorial open-source formado por skill e prompt portátil.
2. **Para quem:** quem cria ou revisa conteúdo e social media com uma voz de marca reconhecível.
3. **Por que usar:** transformar briefing, fatos e amostras aprovadas em um cartão de voz e textos para revisão.
4. **Como experimentar:** uma ação direta e sem instalação, com exemplo copiável.
5. **O que não promete:** publicação automática, conexões não configuradas ou superioridade editorial ainda não medida.

O README deve priorizar a pessoa que vai usar. Arquitetura, testes e proveniência ficam em documentos aprofundados, acessíveis por links. Não inserir gráficos de pontuação, fixtures como "prova" de desempenho, nem galerias decorativas de logos.

## Texto pronto para a caixa *About*

**Description sugerida:**

> Kit editorial open-source para conteúdo e social media com voz de marca, cartão de voz portátil e revisão de textos com IA.

**Topics sugeridos (em inglês, para busca):** `branding`, `social-media`, `content-creation`, `agent-skills`, `prompt-engineering`, `marketing`, `pt-br`, `open-source`.

**Website:** deixar vazio enquanto GitHub Pages não estiver habilitado. Depois de publicado e verificado, usar o endereço real do site (não um endereço presumido).

Essas informações aparecem na lateral do repositório e **não são alteradas por editar o README**. Para configurá-las, o proprietário deve abrir o repositório, clicar na engrenagem da seção *About*, editar Description, Website e Topics e salvar.

## Identidade visual no repositório

- **README:** mostrar uma única assinatura com fundo sólido rosa no topo. Evitar a logo transparente com letras escuras diretamente no tema escuro do GitHub.
- **Texto:** hierarquia de título, proposta, exemplo de uso, início rápido, recursos, limites, documentação e contribuição.
- **Cor e respiro:** usar os assets originais; não redesenhar nem distorcer a marca para criar um novo banner.
- **Galeria de logos:** manter `previa-marca.png` e as variantes como arquivo de identidade, **não como ilustração entre os passos de instalação**.
- **Rodapé do README:** documentação de autoria/licença com links; sem repetir imagens grandes.
- **Site em `docs/`:** logo legível no cabeçalho e ícone de produto em contexto. Não mostrar a prancha de identidades como se fosse funcionalidade.

Veja o [guia visual](identidade-visual.md), a [procedência](../assets/ASSET-PROVENANCE.md) e os [termos separados das artes](../BRAND-ASSETS-LICENSE.md).

## Configurações do GitHub que exigem acesso de administrador

**Social preview:** no repositório, abra *Settings → Social preview*. Remova a imagem antiga caso esteja configurada; só carregue uma nova imagem aprovada, com fundo sólido e texto legível no tema claro e escuro. A prévia social é independente do README e das tags Open Graph do site. Veja [orientação oficial do GitHub](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).

**GitHub Pages (opcional):** *Settings → Pages → Deploy from a branch → main → /docs*. Verifique a página online antes de preencher o campo Website ou anunciar seu endereço. A pasta `docs/` sozinha não significa que um site esteja no ar.

**Segurança e contribuição:** mantenha o CI em PRs e o [SECURITY.md](../SECURITY.md) acessível. Relatos sensíveis não devem ser publicados nas issues.

## Checklist antes de divulgar

- [ ] Uma logo principal visível e legível em temas claro e escuro
- [ ] Sem imagens repetidas nem prancha de logos no fluxo do README
- [ ] Botão/link "experimentar" acessível sem instalação
- [ ] Passos de uso testados com os arquivos da versão pública
- [ ] Nenhum link a recurso que só exista numa candidata não publicada
- [ ] Nenhuma alegação de ganho editorial ainda sem experimento real
- [ ] Atribuição de métodos, licença MIT e termos das artes separados
- [ ] Canal de colaboração e contato disponíveis
- [ ] CI verde e arquivos da release identificados em Releases
- [ ] About/topics/social preview conferidos no GitHub, manualmente se necessário

## Integridade da distribuição

A publicação oficial inclui `skill.zip`, `marketing-hub-plugin.zip`, `marketing-hub-repository.zip` e `SHA256SUMS.txt`. Verifique hashes antes de recomendar instalações. A publicação no GitHub não equivale a disponibilização no Diretório de Plugins nem a suporte nativo idêntico entre assistentes.
