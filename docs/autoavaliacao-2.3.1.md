# Autoavaliação da distribuição 2.3.1

**Data:** 10/11/2026. **Natureza:** autoavaliação técnica e revisão crítica da apresentação; não é parecer independente nem benchmark de qualidade editorial.

**Fonte auditada:** commit `acb9e0d98c8c61b02e1de8adc95a67c295774253`, correspondente à [release v2.3.1](https://github.com/paulopizzatto-del/marketing-hub/releases/tag/v2.3.1). A `main` consultada antes desta nota estava em `9deaec9460f83b1bbd592d2366de8d8f7e0fb956`.

## Parecer

**Aprovada para distribuição técnica como kit de conteúdo e social media, com limites declarados.** Não foi identificada falha bloqueadora no escopo executado. A aprovação não comprova vantagem sobre uma IA competente com o mesmo briefing, compatibilidade de ponta a ponta, robustez universal nem retorno comercial. Alegações comparativas dependem do piloto real.

A release já estava pública, sem marcação de rascunho ou pré-lançamento, e indicada como a mais recente quando esta autoavaliação começou. Não foi necessário duplicá-la ou trocar os pacotes publicados.

## Verificações executadas

| Verificação | Resultado observado | Alcance |
|---|---|---|
| Suíte de unidade local | 48 testes aprovados em Python 3.13.5 | Software, não 48 execuções de IA |
| CI remoto consultado | Python 3.10, 3.11 e 3.13 aprovados | [Execução verificada](https://github.com/paulopizzatto-del/marketing-hub/actions/runs/42923933708) |
| Versão e estrutura | `sync_version.py --check` e `check_repo.py` aprovados | Arquivos e manifestos |
| Schema completo | Aprovado com `jsonschema==4.26.0` e `--require-full` | Perfil de exemplo |
| Reconstrução local | Dois builds idênticos aos quatro arquivos publicados | Determinismo e integridade |
| Skill instalada | 23 arquivos; ZIP com 26.026 bytes; sem imagens ou testes internos | Runtime reduzido |
| Instalador | Quatro destinos locais correspondem ao runtime | Aplicativos de IA não executados |
| Regressões editoriais | LinkedIn de 1.200 caracteres e inglês sem palavras obrigatórias aceitos | Não mede a qualidade dos textos |
| Sinais de risco | Quatro percentuais sintéticos sinalizados; credencial sintética e mistura de marcas detectadas | Heurísticas, não cobertura universal |
| Resultados ausentes | Conjunto vazio de respostas e template humano incompleto recusados | Falha segura de registros |
| Piloto | 144 células planejadas; zero respostas reais | Agenda, não resultado |
| Revalidação remota adicional | Testes, build, download e comparação byte a byte aprovados | [Execução concluída](https://github.com/paulopizzatto-del/marketing-hub/actions/runs/42926381870) |

Além da suíte existente, foram repetidas 13 checagens direcionadas, todas atendidas. Algumas cobrem riscos já presentes nos 48 testes; não são 61 provas independentes.

## Revisão editorial da própria ferramenta

A apresentação delimita conteúdo/social media; a contagem de métodos ficou no material de atribuição. As fixtures de 20 marcas/60 textos aparecem como contrato interno, não vantagem comercial. O banner com promessa não demonstrada foi retirado da apresentação; seus arquivos históricos estão identificados como retirados.

A procedência declara apoio de IA sob direção do responsável, sem confundir hash com autoria. A regra de idioma define precedência entre pedido e perfil. O cartão em Markdown e os quatro exemplos trabalhados ensinam a transferir escolhas de escrita. Isso melhora a especificação; o efeito sobre os textos ainda não foi medido.

O avaliador separa erros de segurança, sinais de revisão e avisos de formato. Percentuais não são automaticamente falsos. `human_approved` e referências de evidência são declarações fornecidas, não autenticação independente de julgamento humano.

## Ajuste aplicado nesta rodada

As notas da release usavam links relativos que não apontavam para os arquivos do repositório quando lidos na página de Releases. Os links foram substituídos por endereços absolutos vinculados à tag auditada, e a autoavaliação foi ligada à apresentação da versão.

Antes dessa alteração de metadados, o GitHub Actions baixou os quatro arquivos publicados, comparou-os byte a byte com uma nova reconstrução e conferiu `SHA256SUMS.txt`. O procedimento terminou com sucesso. A versão permanece oficial, pública e marcada como a mais recente. **Tag, ZIPs e imagens não foram substituídos.** O workflow temporário foi removido após concluir.

## Limitações e pendências

1. Não executei comparação controlada modelo sem Hub versus modelo com Hub, nem julgamento cego por humanos. O ponto central do parecer independente continua aberto.
2. Não executei descoberta/ativação nos clientes de IA, revisão por falantes nativos, teste adversarial generativo ou cronometragem de onboarding com pessoas.
3. Detecção de segredos e alegações é heurística: passar nos sinais mecânicos não comprova verdade, privacidade absoluta ou adequação jurídica.
4. O protocolo original compara o Hub com e sem amostras; não isola o cartão de voz. A alternativa documentada deve ser decidida antes da coleta.
5. Não houve nova varredura integral do histórico Git, reescrita de e-mails ou alteração de permissões, rulesets, Social Preview e segurança da conta.
6. A origem das artes foi declarada pelo responsável/revisor; titularidade jurídica não foi certificada.
7. Esta autoavaliação não atualizou o plugin privado anteriormente instalado no ChatGPT e não constitui aprovação em diretório de plugins.

## Integridade dos pacotes

```text
5aeacee7a6937e3a7b11afca09eafaeefe67513d1afe613bc2d496de722747bb  skill.zip
25e3d16ebc0934b717efad10178398e3ae0943ab50b29cecd6104e0179dc0cd6  marketing-hub-plugin.zip
6e78a5fb8c1e3accddf200a3be9a2a2393025a02f7e7d2cbb09eca8070786689  marketing-hub-repository.zip
08b1bccf7075175e2af26cd0af51481d404c8d23c0d0021d8b7d3e2e5571461f  SHA256SUMS.txt
```

## Reproduzir

Na fonte da tag `v2.3.1`, em ambiente isolado:

```bash
python -m pip install -r requirements-dev.txt
python scripts/sync_version.py --check
python scripts/check_repo.py
python skills/marketinghub/scripts/validate_brand_profile.py --require-full examples/brand-profile-ficticio.json
python -m unittest discover -s tests -v
python scripts/build_release.py
```

Compare dois builds e os pacotes da release. Uma `main` posterior pode gerar um ZIP do repositório diferente por incluir documentação nova; isso não demonstra alteração dos pacotes originais.

## Próxima evidência necessária

Executar o [piloto controlado](https://github.com/paulopizzatto-del/marketing-hub/blob/v2.3.1/evaluation/pilot-144/PLAN.md) e obter avaliação humana independente. Publicar resultados favoráveis, inconclusivos ou desfavoráveis pelo mesmo critério. Até lá, comunicar capacidades e limites — não superioridade demonstrada.
