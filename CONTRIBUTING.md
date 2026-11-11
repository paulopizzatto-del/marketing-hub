# Como contribuir

Obrigado por contribuir com o Marketing Hub!

## Contato para colaboração

Quer ajudar no desenvolvimento, propor melhorias ou colaborar com código, documentação e testes? Fale com **Paulo Pizzatto** pelo e-mail **[paulo.pizzatto@sdssolucoes.com.br](mailto:paulo.pizzatto@sdssolucoes.com.br)**.

Para relatar um problema reproduzível, as [issues do projeto](https://github.com/paulopizzatto-del/marketing-hub/issues/new/choose) continuam disponíveis. Não inclua credenciais ou dados confidenciais de clientes.

## Orientações para contribuir

1. Para bugs, abra uma issue com passos para reproduzir o problema. Diga qual modelo/cliente foi usado e qual comportamento esperava, sem dados pessoais ou credenciais.
2. Para mudanças editoriais, edite a skill canônica em `skills/marketinghub/` e os seus guias relevantes. Evite cópias independentes da mesma regra.
3. Nunca adicione uma marca real ao conjunto padrão, nem afirmações comerciais não comprovadas.
4. Não invente integrações, estados de login ou métricas na documentação.
5. Execute os testes locais antes de abrir PR:

```bash
python scripts/check_repo.py
python -m unittest discover -s tests -v
```

6. No PR, explique mudanças, compatibilidade, testes, riscos e licenças envolvidas.

Ativos de marca devem ser mantidos com fidelidade aos arquivos originais; propostas de alteração da identidade visual exigem aprovação do titular.
