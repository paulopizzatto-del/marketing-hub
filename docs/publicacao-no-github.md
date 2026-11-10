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

- **Description:** Conteúdo e social media com cartão de voz, escrita e revisão.
- **Topics:** `marketing`, `agent-skills`, `prompt-engineering`, `branding`, `social-media`, `ai`, `content-creation`, `pt-br`.
- **Social preview:** Settings → General → Social preview; remova a arte antiga, se configurada. O arquivo em `assets/archive/` está retirado de uso; aguarde uma nova arte aprovada.
- **Site GitHub Pages (opcional):** Settings → Pages → Deploy from a branch → `main` → `/docs`. Após ativado, o endereço esperado é https://paulopizzatto-del.github.io/marketing-hub/. Verifique a publicação antes de divulgá-lo.
- **Issues e segurança:** habilite relato privado de vulnerabilidades quando disponível, e mantenha o CI em pull requests.
- **Branch protection:** quando disponível, exija o CI verde e revisão das alterações antes de mesclar.

## Download e distribuição

A versão oficial está em [Releases](https://github.com/paulopizzatto-del/marketing-hub/releases/latest), com `skill.zip`, `marketing-hub-plugin.zip`, `marketing-hub-repository.zip` e `SHA256SUMS.txt`. Verifique as somas de arquivos depois do download.

Não confundir GitHub público com aprovação na loja de plugins, integração de APIs ou compatibilidade de recursos nativos de todas as IAs.
