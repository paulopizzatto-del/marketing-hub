# Arquitetura editorial

Uma única fonte de regras: `skills/marketinghub/SKILL.md`. As referências da skill são carregadas apenas conforme a tarefa; isso reduz repetição e instruções desnecessárias. O prompt universal é uma **versão condensada autocontida**, criada para ambientes que não carregam arquivos de skill.

## Fluxos

1. Entender objetivo, canal, marca e evidência.
2. Configurar voz por exemplo ou perfil, quando necessário.
3. Roteamento para escrita, estratégia, vídeo, visual, comunidade ou analytics.
4. Criar uma entrega específica sem impor o mesmo formato a todos os casos.
5. Validar fatos, riscos, naturalidade, clareza e restrições de marca.
6. Entregar; publicar apenas se houver ferramenta autorizada e consentimento.

## Módulos

- **Skill**: 17 métodos integrados e referências especializadas.
- **Perfil de marca**: estrutura JSON portátil; sem banco de dados obrigatório.
- **Instalador**: copia arquivos para pastas padrão de agentes; sem rede.
- **Prompt portátil**: pode ser colado em chat sem suporte a skills.
- **Validadores**: testes estruturais, verificação do JSON e de empacotamento.
- **Plugin**: manifesto para ambientes que aceitam empacotamento, sem conectores criados por este pacote.

## O que não existe aqui

Não há backend, endpoint, credencial, banco de dados, rede social conectada, painel de métricas em tempo real, API, robô publicador ou memória persistente automática. Se isso for criado no futuro, deverá ser implementado e documentado separadamente.
