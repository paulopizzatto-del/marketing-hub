# Correções a partir do parecer independente

**Base:** parecer do Claude entregue pelo mantenedor em 10/11/2026, sobre o commit `f5f82a8`. **Release corretiva:** fonte em `VERSION`. Esta tabela registra o que foi implementado e o que ainda precisa de observação externa. A correção não é evidência de superioridade editorial.

| Achado | Correção | Verificação / limite |
|---|---|---|
| Fixtures usadas como prova | Retiradas da vitrine; documentadas em `tests/contracts/` | Tests mecânicos; resultados reais permanecem pendentes |
| Banner promete compatibilidade | Retirado do README/site/plugin; preservado em arquivo | Testes impedem uso das peças retiradas; nova arte depende do responsável |
| Procedência ambígua | Apoio de IA sob direção do responsável declarado | Hash verifica bytes, não autoria ou direitos |
| Avaliador rejeita textos adequados | Segurança, sinais de revisão e formato separados | Regressões para LinkedIn de 1.200 caracteres, inglês sem palavras obrigatórias e percentuais |
| Idioma contraditório | Regra única; conteúdo segue pedido/perfil | A regra foi corrigida; cinco execuções reais em inglês ainda não realizadas |
| Runtime pesado | Allowlist comum ao ZIP e instalador | Sem imagens, auditoria, changelog e testes; metadados obrigatórios preservados |
| Primeiro uso complexo | Prompt para copiar e cartão Markdown | Experiência em menos de dois minutos não foi medida com pessoas |
| Versão espalhada | `VERSION`, gerador e verificação de manifestos | Schema do perfil segue versão independente |
| Proibições sem ensino | Regras comuns e exemplos trabalhados | Quatro transferências de voz + revisão, pauta, roteiro, visual, comunidade e métricas; sem nota de ganho inventada |
| Jargão do criador | Termos genéricos em dados/atendimento | Conteúdo da skill inspecionado; histórico Git preservado |
| Schema completo fora do CI | Dependência fixada e `--require-full` | Caminho completo falha se dependência faltar; modo essencial testado separadamente |
| Produção dependia de testes | `scripts/editorial_checks.py` | Avaliador não importa `tests/` |
| Instrução externa podia virar comando | Regra no SKILL e prompt | Presença testada; robustez generativa contra injeção ainda exige ensaio |

## Decisões de implementação

Preservados uma skill e seu roteador, isolamento de marcas, métricas, instalador e determinismo. As sete capacidades aparecem como serviços; os 17 métodos permanecem no mapa de atribuição. Não foi adotada uma cota arbitrária de negações como indicador de qualidade.

O pacote mantém `agents/openai.yaml` porque é metadado de descoberta; esta é uma adaptação intencional da allowlist sugerida pelo parecer. A skill continua autocontida. O plugin conserva o ícone necessário à sua apresentação e os termos das artes.

O piloto conserva as condições propostas pelo Claude. A alternativa para isolar o cartão de voz está descrita como proposta separada, a decidir antes da execução. Nenhum dado real ou aprovação humana foi fabricado.

## Pendências que esta release não resolve sozinha

Amostras e julgadores humanos do piloto; execuções em modelos reais; verificação linguística; novo banner aprovado; Social preview e regras de administração no GitHub. O histórico mantém e-mails anteriores: não foi reescrito. Commits de conteúdo feitos pelo workflow usam identidade `noreply`; commits da integração podem seguir a configuração da conta, fora do alcance dos scripts locais.

## Como reproduzir

```bash
python scripts/sync_version.py --check
python scripts/check_repo.py
python -m unittest discover -s tests -v
python scripts/build_release.py
python scripts/prepare_pilot.py --out dist/pilot-plan.json
```

Para schema completo: instalar `requirements-dev.txt` e executar o validador com `--require-full`. Para o piloto, preencher e revisar as entradas antes de chamar qualquer modelo; ver `evaluation/pilot-144/PLAN.md`.
