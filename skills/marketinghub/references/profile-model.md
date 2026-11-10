# Perfis portáteis

Priorizar Markdown para uso manual; usar JSON quando a equipe quiser identificação de marcas e validação de campos. O schema do perfil tem versão própria em `schema_version`, independente da release do produto.

## Estrutura

Registrar nome/identificador, oferta, público, idioma, autoria, preferências de escrita, exemplos aprovados e limitações. Atribuir a cada informação material o status confirmado, inferido ou desconhecido. Uma ficha parcial continua útil.

## Operação

Selecionar explicitamente a ficha ativa. Quando uma pessoa comenta numa publicação de uma empresa, a voz é da pessoa, não da empresa citada. Copiar o modelo antes de editar; manter perfis reais fora do repositório público.

Usar `templates/brand-profile.template.json` e `templates/brand-profile.schema.json` para fichas estruturadas. `scripts/validate_brand_profile.py` verifica invariantes essenciais sem bibliotecas externas; `--require-full` exige `jsonschema` para conferir o schema inteiro. Aprovação de campos não comprova veracidade ou qualidade da marca.

**Exemplo:** uma agência trabalha com um ateliê delicado e uma oficina direta. O identificador de cada ficha evita misturar ofertas; exemplos e instruções de voz são carregados somente para a marca que publica.
