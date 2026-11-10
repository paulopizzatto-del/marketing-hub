# Como contribuir

Obrigado por contribuir com o Marketing Hub!

1. Para bugs, abra uma issue com passos de reproducao. Diga qual modelo/cliente foi usado e qual comportamento esperava, sem dados pessoais ou credenciais.
2. Para mudancas editoriais, edite a skill canônica em `skills/marketinghub/` e os seus guias relevantes. Evite cópias independentes da mesma regra.
3. Nunca adicioné uma marca real ao conjunto padrão, nem afirmacoes comerciais não comprovadas.
4. Não invente integrações, estados de login ou métricas na documentação.
5. Execute os testes locais antes de abrir PR:

```bash
python scripts/check_repo.py
python -m unittest discover -s tests -v
```

6. No PR, explique mudancas, compatibilidade, testes, riscos e licenças envolvidas.

Ativos de marca devem ser mantidos com fidelidade aos arquivos originais; propostas de alteracao da identidade visual exigem aprovacao do titular.
