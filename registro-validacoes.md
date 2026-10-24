# Registro de validações do Estoque Fácil

## Validações executadas

- `python3 -m unittest -v`: 10 testes executados com resultado `OK`.
- `python3 -m py_compile database.py estoque.py main.py test_estoque.py`: compilação concluída sem erros.
- `python3 -c "import tkinter"`: Tkinter disponível após a instalação do pacote nativo.
- Inicialização da janela com `xvfb-run`: interface Tkinter inicializada e encerrada com sucesso em tela virtual.
- Repositório GitHub: conferido na branch `main`, com visibilidade pública e arquivos do projeto disponíveis.

## Limites da validação

A tela virtual confirma a construção básica da interface, mas não substitui a execução visual no Windows nem as capturas reais das telas de cadastro, consulta, movimentação e histórico. Essas evidências devem ser produzidas no computador usado para a apresentação.
