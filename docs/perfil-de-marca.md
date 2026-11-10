# A identidade da marca vem primeiro

O Marketing Hub deve adaptar suas entregas ao usuário, nunca o contrario. Para um post simples, um briefing é suficiente. Para uma rotina recorrente, use uma ficha portátil.

## Perguntas que ajudam a calibrar a voz

1. O que a marca oferece e a quem?
2. Qual deve ser a sensacao de ler um post dela?
3. Como a marca fala (formal, brincalhona, técnica, próxima)?
4. Quais frases soam como ela, e quais jamais seriam publicadas?
5. Quais afirmacoes devem ser evitadas ou verificadas antes de publicar?

A pessoa pode responder gradualmente. **Não exijá preencher um formulario extenso para entregar uma única legenda.**

## Ficha JSON

- `skills/marketinghub/templates/brand-profile.template.json`: ficha para preencher; contem campos vazios e não passa na validação antes de completada.
- `skills/marketinghub/templates/brand-profile.schema.json`: contrato de estrutura.
- `examples/brand-profile-ficticio.json`: arquivo completo validavel, sem clientes reais.

Valide com:

```bash
python skills/marketinghub/scripts/validate_brand_profile.py examples/brand-profile-ficticio.json
```

A verificação basica só usa Python. Para validação completa do JSON Schema, `jsonschema` e opcional (`python -m pip install jsonschema`). **O comando não envia o perfil a nenhum servidor.**

## Como usar em plataformas de chat

1. Cole o prompt universal.
2. Cole os campos mais importantes da sua ficha ou anexe o JSON, se suportado.
3. Peça para o assistente confirmar o tom antes de produzir um lote grande.
4. Salve a ficha no seu próprio armazenamento; não assuma que a IA vai lembrar em outro chat.

Com mais de uma marca, sempre diga o nome/ID da que publica. Separe perfis e exemplos para evitar contaminacao de tom e fatos.
