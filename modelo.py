# modelo.py
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class Produto:
    """Representa um produto no sistema."""

    def __init__(self, id: int, nome: str, categoria: str, preco: float):
        """
        Inicializa um novo produto.

        Args:
            id: Identificador único do produto
            nome: Nome do produto
            categoria: Categoria à qual o produto pertence
            preco: Preço unitário do produto
        """
        if not nome or not nome.strip():
            raise ValueError("O nome do produto não pode ser vazio.")
        if not categoria or not categoria.strip():
            raise ValueError("A categoria do produto não pode ser vazia.")
        if preco <= 0:
            raise ValueError("O preço do produto deve ser maior que zero.")

        self.id = id
        self.nome = nome.strip()
        self.categoria = categoria.strip()
        self.preco = float(preco)

    def to_dict(self) -> Dict:
        """Converte o produto para dicionário serializável em JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
        }

    @classmethod
    def from_dict(cls, dados: Dict) -> "Produto":
        """Reconstrói um objeto Produto a partir de um dicionário."""
        return cls(
            id=int(dados["id"]),
            nome=str(dados["nome"]),
            categoria=str(dados["categoria"]),
            preco=float(dados["preco"]),
        )

    def __str__(self) -> str:
        """Retorna uma representação em string do produto."""
        return f"Produto(id={self.id}, nome={self.nome}, categoria={self.categoria}, preco={self.preco:.2f})"


class Venda:
    """Representa uma transação de venda."""

    def __init__(self, id: int, data: datetime, produto_id: int, quantidade: int):
        """
        Inicializa uma nova venda.

        Args:
            id: Identificador único da venda
            data: Data e hora da venda
            produto_id: ID do produto vendido
            quantidade: Quantidade vendida
        """
        if quantidade <= 0:
            raise ValueError("A quantidade vendida deve ser maior que zero.")

        self.id = id
        self.data = data
        self.produto_id = produto_id
        self.quantidade = int(quantidade)

    def to_dict(self) -> Dict:
        """Converte a venda para dicionário serializável em JSON."""
        return {
            "id": self.id,
            "data": self.data.strftime("%Y-%m-%d %H:%M:%S"),
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
        }

    @classmethod
    def from_dict(cls, dados: Dict) -> "Venda":
        """Reconstrói um objeto Venda a partir de um dicionário."""
        return cls(
            id=int(dados["id"]),
            data=datetime.strptime(dados["data"], "%Y-%m-%d %H:%M:%S"),
            produto_id=int(dados["produto_id"]),
            quantidade=int(dados["quantidade"]),
        )

    def __str__(self) -> str:
        """Retorna uma representação em string da venda."""
        data_fmt = self.data.strftime("%d/%m/%Y %H:%M")
        return f"Venda(id={self.id}, data={data_fmt}, produto_id={self.produto_id}, qtd={self.quantidade})"


class RepositorioDados:
    """Gerencia o armazenamento, persistência em JSON e consulta de produtos e vendas."""

    def __init__(self, arquivo_json: str = "dados_vendas.json"):
        """Inicializa o repositório de dados."""
        self.produtos: List[Produto] = []
        self.vendas: List[Venda] = []
        self.arquivo_json = arquivo_json

    def adicionar_produto(self, nome: str, categoria: str, preco: float) -> Produto:
        """Cria e registra um novo produto com ID sequencial."""
        novo_id = max((p.id for p in self.produtos), default=0) + 1
        produto = Produto(novo_id, nome, categoria, preco)
        self.produtos.append(produto)
        return produto

    def registrar_venda(
        self, produto_id: int, quantidade: int, data: Optional[datetime] = None
    ) -> Venda:
        """Valida o produto e registra uma nova transação de venda."""
        produto = self.buscar_produto_por_id(produto_id)
        if not produto:
            raise LookupError(f"Produto com ID {produto_id} não encontrado.")

        novo_id = max((v.id for v in self.vendas), default=0) + 1
        data_venda = data if data is not None else datetime.now()
        venda = Venda(novo_id, data_venda, produto_id, quantidade)
        self.vendas.append(venda)
        return venda

    def buscar_produto_por_id(self, produto_id: int) -> Optional[Produto]:
        """Busca um produto pelo seu identificador único."""
        for produto in self.produtos:
            if produto.id == produto_id:
                return produto
        return None

    def salvar_dados(self) -> None:
        """Salva produtos e vendas em arquivo JSON."""
        dados = {
            "produtos": [p.to_dict() for p in self.produtos],
            "vendas": [v.to_dict() for v in self.vendas],
        }
        try:
            with open(self.arquivo_json, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        except OSError as e:
            raise IOError(f"Erro ao salvar dados no arquivo '{self.arquivo_json}': {e}")

    def carregar_dados(self) -> bool:
        """
        Carrega produtos e vendas de um arquivo JSON existente.

        Returns:
            bool: True se carregou do arquivo com sucesso, False se o arquivo não existir.
        """
        if not os.path.exists(self.arquivo_json):
            return False

        try:
            with open(self.arquivo_json, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                self.produtos = [Produto.from_dict(p) for p in dados.get("produtos", [])]
                self.vendas = [Venda.from_dict(v) for v in dados.get("vendas", [])]
            return True
        except (OSError, json.JSONDecodeError, KeyError, ValueError) as e:
            raise RuntimeError(f"Arquivo JSON corrompido ou inválido: {e}")

    def carregar_dados_exemplo(self) -> None:
        """Popula o repositório com produtos e vendas iniciais de demonstração."""
        self.produtos = [
            Produto(1, "Notebook Pro", "Eletrônicos", 4500.00),
            Produto(2, "Mouse Sem Fio", "Periféricos", 120.00),
            Produto(3, "Teclado Mecânico", "Periféricos", 350.00),
            Produto(4, "Monitor 27'", "Eletrônicos", 1400.00),
            Produto(5, "Cadeira Ergonômica", "Móveis", 980.00),
        ]

        hoje = datetime.now()
        self.vendas = [
            Venda(1, hoje - timedelta(days=6), 1, 2),
            Venda(2, hoje - timedelta(days=5), 2, 5),
            Venda(3, hoje - timedelta(days=4), 3, 3),
            Venda(4, hoje - timedelta(days=3), 4, 2),
            Venda(5, hoje - timedelta(days=2), 5, 1),
            Venda(6, hoje - timedelta(days=1), 2, 4),
            Venda(7, hoje, 1, 1),
        ]