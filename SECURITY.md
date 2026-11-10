# Segurança e divulgação responsável

## Versões abrangidas
A versão oficial do Marketing Hub e seus pacotes de distribuição são mantidos neste repositório. As versões suportadas são indicadas na [página de releases](https://github.com/paulopizzatto-del/marketing-hub/releases); por padrão, priorizamos correções na versão oficial mais recente.

## Como relatar uma vulnerabilidade
Use o recurso **Report a vulnerability / Relatar vulnerabilidade** na aba **Security** do GitHub, **quando estiver habilitado**. O mantenedor precisa ativar *Private vulnerability reporting* nas configurações do repositório.

Se o botão não estiver disponível, abra uma issue solicitando **um canal privado de contato**, mas **não publique detalhes exploráveis, tokens, dados pessoais ou provas de conceito sensíveis** na issue. Não há SLA formal de resposta.

Para problemas editoriais, documentação, instalação e recursos, use as [issues públicas](https://github.com/paulopizzatto-del/marketing-hub/issues).

## Arquitetura e privacidade
Este é um conjunto de instruções, modelos e scripts locais, não um serviço de hospedagem de perfis. O instalador usa apenas biblioteca padrão Python, copia a skill no computador e não solicita tokens nem acessa redes sociais.

- Não adicione credenciais, cookies, dados de clientes, contratos, fotos privadas ou históricos reais às issues e commits.
- Os perfis de marca ficam no ambiente do usuário; não há garantia de persistência automática entre chats.
- A publicação ou agendamento em plataformas externas exige ferramenta conectada e autorização específica.
- Leia os scripts antes de executar código de fontes de terceiros.
- Confira o arquivo `SHA256SUMS.txt` da release para verificar integridade do download; hashes sem assinatura não demonstram, por si sós, autoria.
- O histórico público de commits contém metadados dos autores. Configure um endereço `noreply` no GitHub para novos commits se desejar privacidade do e-mail.

## Boas práticas de manutenção
Workflows devem usar permissões mínimas e ações do GitHub fixadas por SHA completo. Contribuições devem passar pela verificação automatizada antes do merge. O mantenedor deve configurar regras de proteção da branch `main`, alertas de segurança e reportes privados onde disponíveis.
