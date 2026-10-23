import os
import tempfile
import unittest

from database import Database
from estoque import (
    DuplicateProductError,
    EstoqueService,
    InsufficientStockError,
    ProductNotFoundError,
    ValidationError,
)


class EstoqueServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.service = EstoqueService(Database(self.temp_file.name))

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_cadastra_produto_valido(self):
        produto_id = self.service.cadastrar_produto(
            "Perfume Flor de Cerejeira", "Perfumes", 3
        )
        produto = self.service.listar_produtos()[0]
        self.assertEqual(produto_id, produto["id"])
        self.assertEqual(produto["quantidade_atual"], 3)
        self.assertEqual(produto["situacao"], "Estoque baixo")

    def test_rejeita_nome_vazio(self):
        with self.assertRaises(ValidationError):
            self.service.cadastrar_produto("", "Perfumes", 1)

    def test_rejeita_quantidade_negativa(self):
        with self.assertRaises(ValidationError):
            self.service.cadastrar_produto("Body Splash Lavanda", "Perfumes", -1)

    def test_rejeita_categoria_diferente_de_perfumes(self):
        with self.assertRaises(ValidationError):
            self.service.cadastrar_produto("Produto inválido", "Cosméticos", 1)

    def test_rejeita_produto_duplicado_sem_diferenciar_maiusculas(self):
        self.service.cadastrar_produto("Body Splash Lavanda", "Perfumes", 1)
        with self.assertRaises(DuplicateProductError):
            self.service.cadastrar_produto("body splash lavanda", "Perfumes", 2)

    def test_registra_entrada_e_aumenta_estoque(self):
        produto_id = self.service.cadastrar_produto("Body Splash Lavanda", "Perfumes", 1)
        nova_quantidade = self.service.movimentar(produto_id, "ENTRADA", 4)
        self.assertEqual(nova_quantidade, 5)
        self.assertEqual(self.service.listar_produtos()[0]["quantidade_atual"], 5)

    def test_registra_saida_e_reduz_estoque(self):
        produto_id = self.service.cadastrar_produto("Perfume Flor de Cerejeira", "Perfumes", 5)
        nova_quantidade = self.service.movimentar(produto_id, "SAIDA", 2)
        self.assertEqual(nova_quantidade, 3)

    def test_impede_saida_superior_ao_estoque(self):
        produto_id = self.service.cadastrar_produto("Body Splash Lavanda", "Perfumes", 2)
        with self.assertRaises(InsufficientStockError):
            self.service.movimentar(produto_id, "SAIDA", 3)
        self.assertEqual(self.service.listar_produtos()[0]["quantidade_atual"], 2)

    def test_impede_produto_inexistente(self):
        with self.assertRaises(ProductNotFoundError):
            self.service.movimentar(9999, "ENTRADA", 1)

    def test_historico_registra_cadastro_e_movimentacao(self):
        produto_id = self.service.cadastrar_produto("Body Splash Lavanda", "Perfumes", 2)
        self.service.movimentar(produto_id, "SAIDA", 1)
        historico = self.service.historico()
        self.assertEqual(len(historico), 2)
        self.assertEqual(historico[0]["tipo"], "SAIDA")
        self.assertEqual(historico[1]["observacao"], "Cadastro inicial")


if __name__ == "__main__":
    unittest.main()
