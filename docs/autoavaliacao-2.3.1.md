# Autoavaliação da distribuição 2.3.1

**Data:** 10/11/2026. **Natureza:** autoavaliação técnica e revisão crítica de apresentação; não é parecer independente nem benchmark de qualidade editorial.

**Fonte auditada:** commit `acb9e0d98c8c61b02e1de8adc95a67c295774253`, correspondente à [release v2.3.1](https://github.com/paulopizzatto-del/marketing-hub/releases/tag/v2.3.1). A `main` consultada antes desta nota estava em `9deaec9460f83b1bbd592d2366de8d8f7e0fb956`.

## Parecer

**Aprovada para distribuição técnica como kit de conteúdo e social media, com limites declarados.** Não foi identificada falha bloqueadora no escopo executado. A aprovação não comprova vantagem sobre uma IA competente com o mesmo briefing, compatibilidade de ponta a ponta com clientes, robustez universal nem retorno comercial. Aumentar a divulgação com alegações comparativas depende do piloto real.

A release já estava pública, sem marcação de rascunho ou pré-lançamento, e indicada como a mais recente quando esta autoavaliação começou. Não foi necessário duplicá-la ou trocar os arquivos publicados.

## O que executei

| Verificação | Resultado observado | Alcance |
|---|---|---|
| Suíte de unidade local | 48 testes aprovados em Python 3.13.5 | Testes de software, não 48 execuções de IA |
| CI remoto consultado | Python 3.10, 3.11 e 3.13 aprovados | [Execução verificada](https://github.com/paulopizzatto-del/marketing-hub/actions/runs/42923933708) |
| Versão e estrutura | `sync_version.py --check` e `check_repo.py` aprovados | Consistência dos arquivos e manifestos |
| Schema completo | Aprovado com `jsonschema==4.26.0` e `--require-full` | Validação do perfil de exemplo |
| Reconstrução | Duas reconstruções locais idênticas aos quatro arquivos publicados | Determinismo e integridade, não autoria jurídica |
| Skill instalada | 23 arquivos; `skill.zip` com 26.026 bytes; sem imagens ou testes internos | Runtime reduzido |
| Instalador | Quatro destinos locais correspondem ao runtime | Aplicativos de IA não foram executados |
| Regressões do avaliador | LinkedIn de 1.200 caracteres e inglês sem palavras obrigatórias aceitos | Não é julgamento de qualidade desses textos |
| Sinais de risco | Quatro percentuais sintéticos sinalizados; credencial sintética e referência indevida a outra marca detectadas | Heurísticas, sem garantia de cobertura total |
| Falha segura de resultados | Conjunto vazio de respostas e template humano incompleto recusados | Ausência de resultados não gera aprovação |
| Piloto | 144 células planejadas, todas `not_run`; zero respostas reais | Agenda experimental, não resultado |

Além da suíte existente, repeti 13 checagens direcionadas, todas atendidas. Algumas cobrem riscos já presentes nos 48 testes; não devem ser somadas como 61 provas independentes.

## Revisão editorial da própria ferramenta

A apresentação atual delimita conteúdo/social media; a contagem de métodos ficou no material de atribuição. As fixtures de 20 marcas/60 textos aparecem como contrato interno, não vantagem comercial. O banner com promessa não demonstrada foi retirado da apresentação; arquivos históricos permanecem identificados como retirados.

A procedência declara apoio de IA sob direção do responsável, sem confundir hash com autoria. A regra de idioma tem precedência definida entre pedido e perfil. O cartão de voz em Markdown e os quatro exemplos trabalhados ensinam como transferir escolhas de escrita. Isso melhora a especificação do produto; a melhora efetiva dos textos ainda não foi medida.

O avaliador separa erros de segurança, sinais de revisão e avisos de formato. Percentuais não são automaticamente falsos. Campos como `human_approved` e referências de evidência são declarações fornecidas, não comprovação independente de revisão humana.

## Pendências e restrições

1. Não executei comparação controlada entre modelo sem Hub e modelo com Hub, nem julgamento cego por humanos. O ponto central do parecer independente continua aberto.
2. Não executei descoberta/ativação da skill nos clientes de IA, teste linguístico por falantes nativos, ensaio adversarial generativo ou cronometragem de onboarding com pessoas.
3. A detecção de segredos e alegações é heurística: passar nos sinais mecânicos não comprova verdade, privacidade absoluta ou adequação jurídica.
4. O protocolo original de 144 saídas compara o Hub com e sem amostras; ele não isola o cartão de voz. A alternativa está documentada e deve ser decidida antes da coleta.
5. Não fiz nova varredura integral do histórico Git, não reescrevi e-mails e não alterei permissões, rulesets, Social Preview ou configurações de segurança da conta.
6. A origem das artes foi declarada pelo responsável/revisor. Sua titularidade jurídica não foi certificada nesta revisão.
7. Identifiquei links relativos nas notas da release, que não resolvem para a documentação do repositório quando lidos naquela página. A correção de apresentação deve usar links absolutos para a tag auditada, sem alterar ZIPs ou a tag.

## Integridade dos pacotes auditados

```text
5aeacee7a6937e3a7b11afca09eafaeefe67513d1afe613bc2d496de722747bb  skill.zip
25e3d16ebc0934b717efad10178398e3ae0943ab50b29cecd6104e0179dc0cd6  marketing-hub-plugin.zip
6e78a5fb8c1e3accddf200a3be9a2a2393025a02f7e7d2cbb09eca8070786689  marketing-hub-repository.zip
08b1bccf7075175e2af26cd0af51481d404c8d23c0d0021d8b7d3e2e5571461f  SHA256SUMS.txt
```

## Reproduzir as verificações principais

Na fonte exata da tag `v2.3.1`, em ambiente local isolado:

```bash
python -m pip install -r requirements-dev.txt
python scripts/sync_version.py --check
python scripts/check_repo.py
python skills/marketinghub/scripts/validate_brand_profile.py --require-full examples/brand-profile-ficticio.json
python -m unittest discover -s tests -v
python scripts/build_release.py
```

Compare os hashes do primeiro build com um segundo build e com os pacotes da release. Não use os hashes de um ZIP gerado a partir de uma `main` posterior para reprovar uma release antiga: documentação posterior altera legitimamente o arquivo do repositório.

## Próxima evidência necessária

Executar o [piloto controlado](https://github.com/paulopizzatto-del/marketing-hub/blob/v2.3.1/evaluation/pilot-144/PLAN.md) e obter avaliação humana independente. Publicar o resultado favorável, inconclusivo ou desfavorável com o mesmo critério. Até lá, comunicar capacidades e limites — não superioridade demonstrada.
