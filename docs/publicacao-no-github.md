# Publicação e configuração do Marketing Hub no GitHub

Repositório oficial: https://github.com/paulopizzatto-del/marketing-hub  
Edição: 2.3.0 (prévia pública, beta)

## Verificações antes de abrir ao público

1. Confirme que arquivos pessoais, tokens, perfis de clientes e dados confidenciais não estão no código **nem no histórico do Git e dos Actions**.
2. Execute `python scripts/check_repo.py`, `python -m unittest discover -s tests -v` e `python scripts/build_release.py`. Verifique que o CI está verde.
3. Consulte [LICENSE](../LICENSE), [NOTICE](../NOTICE.md) e [termos da marca](../BRAND-ASSETS-LICENSE.md). As imagens originais do Marketing Hub não são software MIT.
4. Não apresente o beta como validado em todos os modelos. Os ensaios reais ficam documentados em [testes-reais-com-modelos.md](testes-reais-com-modelos.md).

## Tornar público

No repositório, abra **Settings → General → Danger Zone → Change repository visibility → Public** e confirme. A conta proprietária deve executar essa ação no GitHub. Isso expõe também o histórico do Git e os logs de Actions. A alteração é separada da publicação do plugin no Diretório do ChatGPT.

## Configurar a apresentação

- **Description:** Seu marketing, num lugar só. Skill e prompt portátil que se adaptam à identidade da sua marca.
- **Topics:** `marketing`, `agent-skills`, `prompt-engineering`, `branding`, `social-media`, `ai`, `content-creation`, `pt-br`.
- **Social preview:** Settings → General → Social preview; faça upload de `assets/social-preview-1280x640.png` (arquivo original, 1280 × 640).
- **Site GitHub Pages (opcional):** Settings → Pages → Deploy from a branch → `main` → `/docs`. Após ativado, o endereço esperado é https://paulopizzatto-del.github.io/marketing-hub/. Verifique a publicação antes de divulgá-lo.
- **Issues e segurança:** habilite relato privado de vulnerabilidades quando disponível, e mantenha o CI em pull requests.
- **Branch protection:** quando disponível, exija o CI verde e revisão das alterações antes de mesclar.

## Download e distribuição

A versão beta fica em [Releases](https://github.com/paulopizzatto-del/marketing-hub/releases/tag/v2.3.0-beta.1), com `skill.zip`, `marketing-hub-plugin.zip`, `marketing-hub-repository.zip` e `SHA256SUMS.txt`. Verifique as somas de arquivos depois do download.

Não confundir GitHub público com aprovação na loja de plugins, integração de APIs ou compatibilidade de recursos nativos de todas as IAs.
