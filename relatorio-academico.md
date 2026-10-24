# Relatório acadêmico — Estoque Fácil

## 1. Identificação do projeto

**Nome:** Estoque Fácil  
**Tipo:** MVP de aplicação desktop  
**Área:** Controle de estoque para salão de beleza  
**Tecnologias:** Python 3.12, Tkinter, SQLite, unittest e Git/GitHub.

## 2. Contexto e problema

O salão de beleza considerado no projeto também comercializa perfumes e body splash. O controle manual por planilhas e contagem física pode tornar a consulta mais lenta e favorecer divergências entre o estoque registrado e a quantidade disponível.

O Estoque Fácil foi proposto para organizar esse controle em uma aplicação local simples, permitindo cadastrar produtos, consultar quantidades e registrar entradas e saídas.

## 3. Objetivo

O objetivo é desenvolver um MVP que facilite o controle local de produtos, mantenha os dados salvos em um banco SQLite e impeça operações que deixariam o estoque inconsistente.

O sistema pode contribuir para uma gestão mais organizada e consultas mais rápidas. Ele não pretende resolver sozinho os problemas do negócio nem comprovar impacto econômico.

## 4. Requisitos implementados

### RF01 — Cadastro de produtos

O sistema permite cadastrar nome, categoria e quantidade inicial. A categoria aceita nesta versão é `Perfumes`. O nome é obrigatório, a quantidade deve ser um número inteiro não negativo e duplicidades não são aceitas sem diferenciar maiúsculas e minúsculas.

Quando a quantidade inicial é maior que zero, ela também é registrada no histórico como uma entrada de cadastro inicial.

### RF02 — Consulta de estoque

A consulta apresenta produto, categoria, quantidade atual e situação. O limite de estoque baixo é de 5 unidades:

- quantidade igual a zero: sem estoque;
- quantidade entre 1 e 4: estoque baixo;
- quantidade igual ou superior a 5: estoque normal.

Também foi implementada busca pelo nome do produto.

### RF03 — Entradas e saídas

O sistema permite registrar movimentações dos tipos `ENTRADA` e `SAIDA`. A quantidade movimentada precisa ser inteira e positiva. Uma saída superior ao estoque disponível é recusada, evitando estoque negativo.

A atualização da quantidade e o registro do histórico são realizados na mesma transação SQLite.

### RF04 — Histórico

O histórico apresenta o produto, o tipo, a quantidade, a data e hora e uma observação quando aplicável.

## 5. Arquitetura

Foi utilizada uma arquitetura monolítica em camadas:

- **Apresentação:** `main.py`, responsável pela interface Tkinter.
- **Regras de negócio:** `estoque.py`, responsável por validações, cadastro, consulta e movimentações.
- **Persistência:** `database.py`, responsável pelo SQLite, tabelas e chaves estrangeiras.
- **Testes:** `test_estoque.py`, responsável pelos testes automatizados das regras.

Essa separação permite testar as regras de negócio sem abrir a janela gráfica.

## 6. Banco de dados

O banco local possui as tabelas `produtos` e `movimentacoes`. A tabela de movimentações possui uma chave estrangeira para produtos, e as chaves estrangeiras são ativadas em cada conexão.

As consultas utilizam parâmetros SQLite, evitando a concatenação de dados informados pelo usuário.

O arquivo `estoque_facil.db` é criado localmente e não deve ser enviado ao GitHub. O backup pode ser feito copiando esse arquivo com o programa fechado.

## 7. Testes realizados

Foram criados testes para cadastro válido, campos vazios, quantidades inválidas, categoria incorreta, duplicidade, entrada, saída, saída superior ao estoque, produto inexistente e histórico.

No ambiente de desenvolvimento, o comando abaixo foi executado com sucesso:

```text
python3 -m unittest -v
```

Resultado registrado: **10 testes executados e aprovados**. A compilação dos arquivos Python também foi verificada com `py_compile`. A janela Tkinter também foi inicializada e encerrada com sucesso em uma tela virtual (`xvfb`), confirmando a construção básica da interface.

A execução visual no Windows e as respectivas capturas de tela ainda devem ser realizadas no computador de apresentação. A validação em tela virtual não substitui essas evidências.

## 8. Limitações

O MVP funciona localmente em um único computador, não possui login, não possui acesso pela internet, não possui múltiplos usuários e não integra vendas, pagamentos ou relatórios financeiros.

## 9. Relação com o ODS 8

O projeto relaciona-se ao ODS 8 — Trabalho Decente e Crescimento Econômico, especialmente à meta 8.3, por apoiar a organização e a produtividade de um pequeno negócio. Essa relação é uma contribuição potencial do sistema, não uma comprovação de impacto econômico.

## 10. Conclusão

O Estoque Fácil atende ao escopo essencial do MVP: cadastrar produtos, consultar o estoque, registrar entradas e saídas, manter histórico e impedir estoque negativo. A estrutura simples favorece a apresentação acadêmica e permite futuras melhorias sem misturar a interface com as regras de negócio.
