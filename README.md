# Estoque Fácil

MVP desktop para controle de estoque de perfumes e body splash de um salão de beleza.

## Objetivo

O sistema facilita o cadastro de produtos, a consulta das quantidades disponíveis e o registro de entradas e saídas. Ele busca reduzir a dependência de planilhas e tornar a consulta do estoque mais organizada. Não é uma solução empresarial completa e não comprova, sozinho, impacto econômico no negócio.

A proposta se relaciona ao ODS 8, especialmente à meta 8.3, por apoiar a organização e a produtividade de pequenos negócios.

## Funcionalidades

- Cadastro de produtos da categoria `Perfumes`.
- Validação de nome, categoria, quantidade e duplicidade.
- Consulta do estoque com busca por nome.
- Situações: sem estoque, estoque baixo (menos de 5 unidades) e estoque normal.
- Registro de entradas e saídas.
- Bloqueio de saída maior que o estoque disponível.
- Histórico de movimentações.
- Persistência local em SQLite.
- Recurso de acessibilidade para ampliar a fonte e os controles da interface.

## Tecnologias

- Python 3.12+
- Tkinter
- SQLite com `sqlite3`
- `unittest`
- Git e GitHub

Não são necessárias dependências externas.

## Organização dos arquivos

- `main.py`: interface gráfica Tkinter.
- `database.py`: conexão, tabelas e configuração do SQLite.
- `estoque.py`: regras de negócio e validações.
- `test_estoque.py`: testes automatizados isolados.
- `estoque_facil.db`: banco local criado ao executar o sistema; não deve ser enviado ao Git.

## Requisitos

Windows 10 ou superior com Python 3.12 ou mais recente instalado. O Git é necessário apenas para controle de versão e envio ao GitHub.

## Execução no Windows

Abra o PowerShell na pasta do projeto e execute:

```powershell
python main.py
```

Ao iniciar, o banco `estoque_facil.db` será criado automaticamente na pasta do projeto. Cadastre, por exemplo, `Perfume Flor de Cerejeira` ou `Body Splash Lavanda`, sempre com a categoria `Perfumes`.

## Passo a passo de utilização

1. Na tela inicial, clique em **Cadastrar produto**.
2. Informe o nome do perfume ou body splash, mantenha a categoria `Perfumes` e digite a quantidade inicial. Em seguida, clique em **Salvar**.
3. Confira o produto na tabela principal. A coluna **Situação** informa se o estoque está normal, baixo ou zerado.
4. Para localizar um item, digite parte do nome no campo **Buscar produto** e clique em **Buscar**. Use **Atualizar consulta** para retornar à lista completa.
5. Para registrar uma reposição ou uma venda, clique em **Movimentar estoque**, selecione o produto, escolha `ENTRADA` ou `SAIDA`, informe a quantidade e clique em **Salvar**.
6. Depois da movimentação, confira a nova quantidade na tabela principal. O sistema não permite registrar uma saída maior que o estoque disponível.
7. Clique em **Histórico** para consultar as movimentações, com produto, tipo, quantidade, data e observação.
8. Para facilitar a leitura, clique em **Acessibilidade: fonte maior**. O tamanho dos textos, botões e linhas da tabela será ampliado. Clique novamente, agora em **Acessibilidade: fonte normal**, para retornar ao tamanho padrão.
9. Para encerrar, clique em **Sair** ou feche a janela.

## Testes

Os testes usam um banco temporário e não alteram o banco real:

```powershell
python -m unittest -v
```

## Backup

Feche o programa e copie o arquivo `estoque_facil.db` para uma pasta segura ou para um dispositivo de backup. Para restaurar, feche o programa e substitua o arquivo atual por uma cópia válida. O arquivo do banco não deve ser versionado no Git.

## Limitações do MVP

- Uso local em um único computador.
- Sem login e sem múltiplos usuários.
- Sem acesso pela internet.
- Sem relatórios financeiros ou integração com vendas.
- Exclusão física de produtos não está disponível; esta versão trabalha apenas com produtos ativos.

## Git

Sugestão de commits pequenos e descritivos:

```text
docs: adiciona documentação inicial
feat: cria estrutura do banco de dados
feat: implementa regras de estoque
test: adiciona testes das regras de estoque
feat: cria interface gráfica
```

Antes do primeiro envio, confira se o banco e caches não aparecem no `git status`.
