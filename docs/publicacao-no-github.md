# Publicação e configuração do Marketing Hub no GitHub

Repositório oficial: https://github.com/paulopizzatto-del/marketing-hub
Edição: versão definida em `VERSION`

## Verificações antes de abrir ao público

1. Confirme que arquivos pessoais, tokens, perfis de clientes e dados confidenciais não estão no código **nem no histórico do Git e dos Actions**.
2. Execute `python scripts/check_repo.py`, `python -m unittest discover -s tests -v` e `python scripts/build_release.py`. Verifique que o CI está verde.
3. Consulte [LICENSE](../LICENSE), [NOTICE](../NOTICE.md) e [termos da marca](../BRAND-ASSETS-LICENSE.md). As imagens originais do Marketing Hub não são software MIT.
4. Não apresente a versão oficial como certificação de qualidade em todos os modelos. Os ensaios reais ficam documentados em [testes-reais-com-modelos.md](testes-reais-com-modelos.md).

## Tornar público

No repositório, abra **Settings → General → Danger Zone → Change repository visibility → Public** e confirme. A conta proprietária deve executar essa ação no GitHub. Isso expõe também o histórico do Git e os logs de Actions. A alteração é separada da publicação do plugin no Diretório do ChatGPT.

## Configurar a apresentação

- **Description:** Kit editorial open-source para conteúdo e social media com voz de marca, cartão de voz portátil e revisão de textos com IA.
- **Topics:** `branding`, `social-media`, `content-creation`, `agent-skills`, `prompt-engineering`, `marketing`, `pt-br`, `open-source`.
- **Social preview:** Settings → General → Social preview; remova a arte antiga, se configurada. O arquivo em `assets/archive/` está retirado de uso; aguarde uma nova arte aprovada.
- **Site GitHub Pages (opcional, ainda não habilitado na revisão pré-lançamento):** Settings → Pages → Deploy from a branch → `main` → `/docs`. Após ativado, o endereço esperado é https://paulopizzatto-del.github.io/marketing-hub/. Teste a página inicial e `/studio.html` no celular e no desktop antes de divulgar. Até então, compartilhe a release ou o repositório, não a URL do Studio como ferramenta online.
- **Issues e segurança:** habilite relato privado de vulnerabilidades quando disponível, e mantenha o CI em pull requests.
- **Branch protection:** quando disponível, exija o CI verde e revisão das alterações antes de mesclar.

## Download e distribuição

A versão oficial está em [Releases](https://github.com/paulopizzatto-del/marketing-hub/releases/latest), com `skill.zip`, `marketing-hub-plugin.zip`, `marketing-hub-repository.zip` e `SHA256SUMS.txt`. Verifique as somas de arquivos depois do download.

Não confundir GitHub público com aprovação na loja de plugins, integração de APIs ou compatibilidade de recursos nativos de todas as IAs.

## Curadoria da vitrine

O README não deve exibir o mosaico de logos `previa-marca.png` nem repetir logos na seção de licenças. Uma assinatura com fundo sólido legível na abertura é suficiente. A página deve conduzir o visitante de **proposta de valor → experimento sem instalar → capacidades → limites → documentação e contato**.

A alteração do arquivo README não modifica os campos **About, Topics, Website ou Social preview** do repositório: editar essas configurações manualmente em Settings / About quando houver acesso administrativo.
