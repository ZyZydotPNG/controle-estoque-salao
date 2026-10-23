# Fluxograma — Estoque Fácil

```mermaid
flowchart TD
    A[Usuária abre o Estoque Fácil] --> B{Escolhe uma operação}
    B -->|Cadastrar produto| C[Informar nome, categoria e quantidade inicial]
    C --> D{Dados válidos?}
    D -->|Não| E[Exibir mensagem de erro]
    E --> B
    D -->|Sim| F[Gravar produto no SQLite]
    F --> G{Quantidade inicial maior que zero?}
    G -->|Sim| H[Registrar entrada inicial no histórico]
    G -->|Não| I[Finalizar cadastro]
    H --> I
    I --> J[Exibir confirmação]
    J --> B
    B -->|Consultar estoque| K[Buscar produtos no SQLite]
    K --> L[Exibir nome, categoria, quantidade e situação]
    L --> B
    B -->|Movimentar estoque| M[Selecionar produto, tipo e quantidade]
    M --> N{Produto ativo e quantidade válida?}
    N -->|Não| E
    N -->|Sim| O{É saída maior que o estoque?}
    O -->|Sim| P[Exibir estoque insuficiente]
    P --> B
    O -->|Não| Q[Iniciar transação SQLite]
    Q --> R[Atualizar quantidade]
    R --> S[Registrar movimentação]
    S --> T[Confirmar transação]
    T --> U[Exibir confirmação]
    U --> B
    B -->|Histórico| V[Consultar movimentações]
    V --> W[Exibir produto, tipo, quantidade e data]
    W --> B
    B -->|Sair| X[Encerrar aplicação]
```

## Fluxo resumido

```text
Usuária → Interface Tkinter → Regras de negócio → SQLite
                                      ↓
                              Validação e transação
                                      ↓
                               Mensagem de retorno
```
