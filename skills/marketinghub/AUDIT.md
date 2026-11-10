# Auditoria de arquitetura — MarketingHub 2.0

Data: 2026-11-10. Escopo: revisão da versão editorial especializada anterior, reconstrução neutra e validação de pacote. Esta auditoria **não** é um teste de desempenho real em contas conectadas nem uma homologação de loja de plugins.

## Problemas encontrados e correções

| Problema da versão anterior | Correção no 2.0 |
|---|---|
| Quatro marcas e nicho embutidos | Nenhuma marca real pré-configurada. Onboarding adaptativo e ficha opcional por marca. |
| Estilo editorial transferido entre emissores | `brand_id`, emissor versus assunto, e regras explícitas de isolamento. |
| Configuração dependente da conversa anterior | Perfil JSON exportável e documentação para reapresentar em outras sessões. |
| 17 métodos apenas agrupados | Tabela de rastreabilidade, roteador e instruções executáveis por formato. |
| Possível excesso de formulários | Resposta direta para pedidos simples; perguntas somente diante de lacunas materiais. |
| Possibilidade de confundir texto e ação externa | Estados separados de rascunho, pronto editorialmente, agendado e publicado. |
| Supor métricas, tendências ou funcionalidades | Evidências, datas, denominadores e experimentos explicitamente tratados. |
| Arte, prompt e arquivo confundidos | Diferenciação de entrega e QA visual. |
| Sem ficha validável e contratos de dados | Template JSON, JSON Schema e script de validação offline. |
| Referências específicas de cliente na descrição da skill | Metadados, README, roteador e exemplos neutros. |

## Testes executados

- `scripts/selftest.py`: existência de referências, cobertura dos 17 métodos, único `SKILL.md`, neutralidade dos guias, JSONs válidos, sucesso de perfil válido e falha de perfil inválido.
- `quick_validate.py`: frontmatter de skill e nomenclatura aprovados.
- Leitura dos manifests: `plugin.json` em formato Agent Plugins 1.0 e manifesto legado `.codex-plugin/plugin.json` compatível com a estrutura do plugin anterior.
- ZIPs: integridade CRC, arquivos essenciais e apenas uma skill no ZIP de distribuição.

**16 cenários de aceitação estão documentados em `tests/test_cases.json` para execução funcional futura com o modelo.** São *casos especificados*, não 16 testes reais de comportamento de LLM já executados. Não atribuir sucesso funcional automático a eles.

## Limites restantes

- O MarketingHub não guarda automaticamente perfis fora da conversa/arquivo conectado e não cria banco de dados próprio.
- Publicar/agendar, buscar dados sociais, gerar artes e obter estatísticas dependem das ferramentas disponíveis, de autenticação e de autorização.
- Sem exemplos da marca, a primeira versão editorial é aproximada e precisa de ajuste humano.
- O plugin ZIP não incorpora logotipo particular de clientes nem conector externo. Ícone de produto pode ser configurado posteriormente.
- O arquivo plugin ZIP está estruturalmente pronto, mas sua aceitação definitiva depende da importação/homologação pela plataforma.
