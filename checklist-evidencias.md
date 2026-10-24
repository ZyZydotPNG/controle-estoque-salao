# Checklist de evidências acadêmicas

As capturas abaixo devem ser feitas no computador Windows onde a aplicação for executada. Não use imagens simuladas.

## Validações já realizadas no ambiente de desenvolvimento

- 10 testes `unittest` executados com resultado `OK`.
- Compilação dos arquivos Python verificada com `py_compile`.
- Tkinter importado com sucesso.
- Janela Tkinter inicializada e encerrada em tela virtual.
- Repositório GitHub conferido na branch `main`, com os arquivos do projeto e três commits remotos.

Essas validações não substituem as capturas reais da aplicação no Windows.

## Evidências do sistema

- [ ] Tela principal do Estoque Fácil aberta.
- [ ] Tela de cadastro com `Perfume Flor de Cerejeira` ou `Body Splash Lavanda`.
- [ ] Mensagem de cadastro realizado com sucesso.
- [ ] Tela de movimentação mostrando uma entrada.
- [ ] Consulta exibindo a quantidade após a entrada.
- [ ] Tela de movimentação mostrando uma saída válida.
- [ ] Consulta exibindo a quantidade reduzida.
- [ ] Mensagem de erro ao tentar retirar quantidade maior que o estoque.
- [ ] Tela de histórico com as movimentações registradas.

## Evidências técnicas

- [ ] Repositório do GitHub aberto mostrando os arquivos.
- [ ] README visível no repositório.
- [ ] Terminal com `python -m unittest -v` e resultado `OK`.
- [ ] Terminal com `git log --oneline` mostrando commits descritivos.
- [ ] Opcional: pasta local mostrando que o arquivo SQLite é criado após executar o programa.

## Sugestão de nomes dos arquivos de captura

```text
01-tela-principal.png
02-cadastro-produto.png
03-cadastro-sucesso.png
04-entrada-estoque.png
05-consulta-apos-entrada.png
06-saida-estoque.png
07-bloqueio-saida.png
08-historico.png
09-github-arquivos.png
10-testes-unittest.png
11-git-log.png
```

## Observação

No ambiente de desenvolvimento foram executados e aprovados 10 testes automatizados. A captura da interface e do terminal no Windows deve ser produzida pela pessoa responsável pela apresentação, no momento em que executar o projeto.
