from database import Database


LOW_STOCK_LIMIT = 5
CATEGORY = "Perfumes"


class EstoqueError(Exception):
    """Erro esperado apresentado ao usuário."""


class ValidationError(EstoqueError):
    pass


class DuplicateProductError(EstoqueError):
    pass


class ProductNotFoundError(EstoqueError):
    pass


class InsufficientStockError(EstoqueError):
    pass


class EstoqueService:
    def __init__(self, database=None):
        self.database = database or Database()

    @staticmethod
    def _positive_integer(value, field_name):
        if isinstance(value, bool):
            raise ValidationError(f"{field_name} deve ser um número inteiro.")
        try:
            number = int(value)
        except (TypeError, ValueError):
            raise ValidationError(f"{field_name} deve ser um número inteiro.")
        if str(value).strip() != str(number):
            raise ValidationError(f"{field_name} deve ser um número inteiro.")
        if number <= 0:
            raise ValidationError(f"{field_name} deve ser maior que zero.")
        return number

    @staticmethod
    def _non_negative_integer(value):
        if isinstance(value, bool):
            raise ValidationError("A quantidade deve ser um número inteiro não negativo.")
        try:
            number = int(value)
        except (TypeError, ValueError):
            raise ValidationError("A quantidade deve ser um número inteiro não negativo.")
        if str(value).strip() != str(number) or number < 0:
            raise ValidationError("A quantidade deve ser um número inteiro não negativo.")
        return number

    def cadastrar_produto(self, nome, categoria, quantidade_inicial):
        nome = (nome or "").strip()
        categoria = (categoria or "").strip()
        if not nome:
            raise ValidationError("Informe o nome do produto.")
        if categoria != CATEGORY:
            raise ValidationError("Nesta versão, a categoria deve ser Perfumes.")
        quantidade = self._non_negative_integer(quantidade_inicial)

        try:
            with self.database.connect() as connection:
                cursor = connection.execute(
                    "INSERT INTO produtos (nome, categoria, quantidade_atual) VALUES (?, ?, ?)",
                    (nome, categoria, quantidade),
                )
                produto_id = cursor.lastrowid
                if quantidade > 0:
                    connection.execute(
                        """INSERT INTO movimentacoes
                           (produto_id, tipo, quantidade, observacao)
                           VALUES (?, 'ENTRADA', ?, 'Cadastro inicial')""",
                        (produto_id, quantidade),
                    )
        except Exception as error:
            if "UNIQUE constraint failed" in str(error):
                raise DuplicateProductError("Já existe um produto com esse nome.")
            raise
        return produto_id

    def listar_produtos(self, busca=""):
        termo = f"%{(busca or '').strip()}%"
        with self.database.connect() as connection:
            return connection.execute(
                """SELECT id, nome, categoria, quantidade_atual,
                          CASE
                            WHEN quantidade_atual = 0 THEN 'Sem estoque'
                            WHEN quantidade_atual < ? THEN 'Estoque baixo'
                            ELSE 'Estoque normal'
                          END AS situacao
                   FROM produtos
                   WHERE ativo = 1 AND nome LIKE ? COLLATE NOCASE
                   ORDER BY nome""",
                (LOW_STOCK_LIMIT, termo),
            ).fetchall()

    def movimentar(self, produto_id, tipo, quantidade):
        tipo = (tipo or "").strip().upper()
        if tipo not in {"ENTRADA", "SAIDA"}:
            raise ValidationError("O tipo deve ser ENTRADA ou SAIDA.")
        quantidade = self._positive_integer(quantidade, "A quantidade")

        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            produto = connection.execute(
                "SELECT id, quantidade_atual FROM produtos WHERE id = ? AND ativo = 1",
                (produto_id,),
            ).fetchone()
            if produto is None:
                raise ProductNotFoundError("Produto não encontrado.")
            atual = produto["quantidade_atual"]
            if tipo == "SAIDA" and quantidade > atual:
                raise InsufficientStockError("Estoque insuficiente para essa saída.")
            nova_quantidade = atual + quantidade if tipo == "ENTRADA" else atual - quantidade
            connection.execute(
                "UPDATE produtos SET quantidade_atual = ? WHERE id = ?",
                (nova_quantidade, produto_id),
            )
            connection.execute(
                "INSERT INTO movimentacoes (produto_id, tipo, quantidade) VALUES (?, ?, ?)",
                (produto_id, tipo, quantidade),
            )
        return nova_quantidade

    def historico(self):
        with self.database.connect() as connection:
            return connection.execute(
                """SELECT m.id, p.nome, m.tipo, m.quantidade,
                          m.data_hora, COALESCE(m.observacao, '') AS observacao
                   FROM movimentacoes m
                   JOIN produtos p ON p.id = m.produto_id
                   ORDER BY m.id DESC"""
            ).fetchall()
