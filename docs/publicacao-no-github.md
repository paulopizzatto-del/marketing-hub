# Publicar o repositório no GitHub

## Revisão final antes de tornar público

- Confirme que é o titular ou tem autorização para publicar os logotipos e arquivos de marca.
- Revise a proposta de MIT para o código e a documentação; os ativos de marca estão excluidos da licença aberta.
- Preserve a licença MIT e a atribuição a Charlie Hills pelas 17 métodos originais.
- Garanta que nenhum perfil real, token, imagem privada, email pessoal desnecessario ou contrato foi incluído.
- Rode CI localmente: `python scripts/check_repo.py` e `python -m unittest discover -s tests -v`.
- Teste ao menos um ambiente de skill nativa e um chat com o prompt universal antes de dizer que o produto foi testado com outras IAs.

## Subir o código com Git

1. Crie no GitHub um repositório vazio chamado `marketing-hub` (sem README ou .gitignore gerados pela interface, pois eles já existem neste pacote).
2. Extraia **o conteúdo** do ZIP deste projeto em uma pasta chamada `marketing-hub`.
3. Na pasta extraída, execute:

```bash
git init
git add .
git commit -m "feat: launch Marketing Hub portable editorial toolkit"
git branch -M main
git remote add origin URL_DO_GITHUB.git
git push -u origin main
```

Substitua `URL_DO_GITHUB.git` pelo endereço indicado na sua conta. Não coloque token em comando, arquivo ou captura de tela. Para repositórios públicos, revise o log de arquivos antes do push: `git status` e `git diff --cached --stat`.

**Alternativa pelo navegador:** abra um novo repositório no GitHub e use **Add file > Upload files** depois de **extrair o ZIP**. O GitHub não descompacta automaticamente um ZIP enviado como um arquivo comum.

## Configurar a vitrine

O banner do README utiliza `assets/banner.png`, sem alterações. **Não trocar pelas imagens geradas em conversas de IA**: o padrão aprovado usa somente os arquivos originais enviados pelo proprietário. A imagem social é selecionada manualmente em **Settings > General > Social preview**, de acordo com as opções disponíveis no GitHub.

- **Description:** `Seu marketing, num lugar só. Skill e prompt portátil que se adaptam à identidade da sua marca.`
- **Topics:** `marketing`, `agent-skills`, `prompt-engineering`, `branding`, `social-media`, `ai`, `content-creation`, `pt-br`.
- **Social preview:** use `assets/social-preview-1280x640.png` (arte original fornecida no kit do GitHub).
- **Website:** opcionalmente publique o conteúdo de `docs/` via GitHub Pages, ajustando links quando souber a URL real do repositório.
- **Issues/Discussions:** habilite conforme capacidade de manutenção da equipe.

## Releases

```bash
python scripts/build_release.py
```

Isso gera `dist/skill.zip`, `dist/marketing-hub-plugin.zip` e `dist/marketing-hub-repository.zip`. Use as versões em GitHub Releases, em vez de pedir aos usuários para baixar um arquivo de código sem instrução.

A workflow de release pode criar os ZIPs em tags `v*`, mas o dono deve revisar permissões, secrets e configuração do repositório antes da primeira execução.

## O que o GitHub não faz

Abrir um repositório no GitHub **não** publica automaticamente o plugin no diretório do ChatGPT, instala em modelos de IA, registra uma marca ou disponibiliza uma API. São processos separados.
