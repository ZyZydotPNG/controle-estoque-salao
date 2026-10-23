import tkinter as tk
from tkinter import messagebox, ttk

from estoque import (
    EstoqueError,
    EstoqueService,
)


class EstoqueFacilApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Estoque Fácil")
        self.geometry("820x540")
        self.minsize(760, 480)
        self.service = EstoqueService()
        self._configure_style()
        self._build_interface()
        self.atualizar_estoque()

    def _configure_style(self):
        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Action.TButton", padding=8)

    def _build_interface(self):
        header = ttk.Frame(self, padding=(20, 18, 20, 8))
        header.pack(fill="x")
        ttk.Label(header, text="Estoque Fácil", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Controle simples de perfumes e body splash",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(3, 0))

        buttons = ttk.Frame(self, padding=(20, 8))
        buttons.pack(fill="x")
        for text, command in [
            ("Cadastrar produto", self.abrir_cadastro),
            ("Movimentar estoque", self.abrir_movimentacao),
            ("Atualizar consulta", self.atualizar_estoque),
            ("Histórico", self.abrir_historico),
            ("Sair", self.destroy),
        ]:
            ttk.Button(buttons, text=text, command=command, style="Action.TButton").pack(
                side="left", padx=(0, 8)
            )

        search = ttk.Frame(self, padding=(20, 4, 20, 8))
        search.pack(fill="x")
        ttk.Label(search, text="Buscar produto:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search, textvariable=self.search_var, width=35)
        search_entry.pack(side="left", padx=8)
        search_entry.bind("<Return>", lambda _event: self.atualizar_estoque())
        ttk.Button(search, text="Buscar", command=self.atualizar_estoque).pack(side="left")

        table_frame = ttk.Frame(self, padding=(20, 0, 20, 20))
        table_frame.pack(fill="both", expand=True)
        columns = ("nome", "categoria", "quantidade", "situacao")
        self.stock_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = {
            "nome": "Produto",
            "categoria": "Categoria",
            "quantidade": "Quantidade",
            "situacao": "Situação",
        }
        widths = {"nome": 300, "categoria": 150, "quantidade": 100, "situacao": 160}
        for column in columns:
            self.stock_tree.heading(column, text=headings[column])
            self.stock_tree.column(column, width=widths[column], anchor="w")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=scrollbar.set)
        self.stock_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def atualizar_estoque(self):
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        for produto in self.service.listar_produtos(self.search_var.get()):
            self.stock_tree.insert(
                "", "end", iid=str(produto["id"]),
                values=(produto["nome"], produto["categoria"], produto["quantidade_atual"], produto["situacao"]),
            )

    def abrir_cadastro(self):
        window = tk.Toplevel(self)
        window.title("Cadastrar produto")
        window.resizable(False, False)
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill="both", expand=True)
        nome = tk.StringVar()
        quantidade = tk.StringVar(value="0")
        ttk.Label(frame, text="Nome do produto:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=nome, width=35).grid(row=0, column=1, pady=6)
        ttk.Label(frame, text="Categoria:").grid(row=1, column=0, sticky="w", pady=6)
        categoria = ttk.Combobox(frame, values=("Perfumes",), state="readonly", width=32)
        categoria.set("Perfumes")
        categoria.grid(row=1, column=1, pady=6)
        ttk.Label(frame, text="Quantidade inicial:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=quantidade, width=35).grid(row=2, column=1, pady=6)

        def salvar():
            try:
                self.service.cadastrar_produto(nome.get(), categoria.get(), quantidade.get())
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.", parent=window)
                window.destroy()
                self.atualizar_estoque()
            except EstoqueError as error:
                messagebox.showerror("Não foi possível cadastrar", str(error), parent=window)

        ttk.Button(frame, text="Salvar", command=salvar).grid(row=3, column=1, sticky="e", pady=(14, 0))

    def abrir_movimentacao(self):
        produtos = self.service.listar_produtos()
        if not produtos:
            messagebox.showinfo("Movimentar estoque", "Cadastre um produto antes de movimentar o estoque.")
            return
        window = tk.Toplevel(self)
        window.title("Movimentar estoque")
        window.resizable(False, False)
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill="both", expand=True)
        nomes = [f"{p['id']} - {p['nome']} (atual: {p['quantidade_atual']})" for p in produtos]
        produto_var = tk.StringVar(value=nomes[0])
        tipo_var = tk.StringVar(value="ENTRADA")
        quantidade_var = tk.StringVar()
        ttk.Label(frame, text="Produto:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Combobox(frame, textvariable=produto_var, values=nomes, state="readonly", width=42).grid(row=0, column=1, pady=6)
        ttk.Label(frame, text="Tipo:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(frame, textvariable=tipo_var, values=("ENTRADA", "SAIDA"), state="readonly", width=39).grid(row=1, column=1, pady=6)
        ttk.Label(frame, text="Quantidade:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=quantidade_var, width=42).grid(row=2, column=1, pady=6)

        def salvar():
            try:
                produto_id = int(produto_var.get().split(" - ", 1)[0])
                self.service.movimentar(produto_id, tipo_var.get(), quantidade_var.get())
                messagebox.showinfo("Sucesso", f"{tipo_var.get().capitalize()} registrada com sucesso.", parent=window)
                window.destroy()
                self.atualizar_estoque()
            except (EstoqueError, ValueError) as error:
                messagebox.showerror("Não foi possível movimentar", str(error), parent=window)

        ttk.Button(frame, text="Salvar", command=salvar).grid(row=3, column=1, sticky="e", pady=(14, 0))

    def abrir_historico(self):
        window = tk.Toplevel(self)
        window.title("Histórico de movimentações")
        window.geometry("760x360")
        frame = ttk.Frame(window, padding=12)
        frame.pack(fill="both", expand=True)
        columns = ("produto", "tipo", "quantidade", "data", "observacao")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        labels = {"produto": "Produto", "tipo": "Tipo", "quantidade": "Quantidade", "data": "Data e hora", "observacao": "Observação"}
        for col in columns:
            tree.heading(col, text=labels[col])
            tree.column(col, width=145 if col != "observacao" else 120)
        for movement in self.service.historico():
            tree.insert("", "end", values=tuple(movement[col] for col in columns))
        tree.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = EstoqueFacilApp()
    app.mainloop()
