# visualizacao.py
from datetime import datetime
from typing import Dict, List, Tuple
from modelo import Produto, RepositorioDados


def exibir_titulo(titulo: str) -> None:
    """Exibe um título formatado."""
    print("\n" + "=" * 50)
    print(f"{titulo.center(50)}")
    print("=" * 50)


def exibir_menu() -> str:
    """Exibe o menu principal e retorna a opção escolhida pelo usuário."""
    exibir_titulo("SISTEMA DE ANÁLISE DE VENDAS")
    print("1 - Exibir Total de Vendas")
    print("2 - Exibir Vendas por Categoria")
    print("3 - Exibir Produtos Mais Vendidos")
    print("4 - Exibir Tendência de Vendas")
    print("5 - Filtrar Análises por Período")
    print("6 - Adicionar Novo Produto")
    print("7 - Registrar Nova Venda")
    print("8 - Listar Produtos Cadastrados")
    print("0 - Salvar e Sair")
    print("=" * 50)
    return input("Escolha uma opção: ").strip()


def exibir_total_vendas(total: float) -> None:
    """Exibe o total de vendas formatado."""
    exibir_titulo("TOTAL DE VENDAS")
    print(f"Valor total: R$ {total:.2f}")


def exibir_vendas_por_categoria(vendas_por_categoria: Dict[str, float]) -> None:
    """Exibe o total de vendas por categoria."""
    exibir_titulo("VENDAS POR CATEGORIA")

    if not vendas_por_categoria:
        print("Nenhuma venda encontrada para exibição.")
        return

    # Calcular o total geral para percentuais
    total_geral = sum(vendas_por_categoria.values())

    for categoria, valor in sorted(
        vendas_por_categoria.items(), key=lambda x: x[1], reverse=True
    ):
        percentual = (valor / total_geral) * 100 if total_geral > 0 else 0
        print(f"{categoria}: R$ {valor:.2f} ({percentual:.1f}%)")


def exibir_produtos_mais_vendidos(
    produtos_mais_vendidos: List[Tuple[Produto, int]]
) -> None:
    """Exibe os produtos mais vendidos."""
    exibir_titulo("PRODUTOS MAIS VENDIDOS")

    if not produtos_mais_vendidos:
        print("Nenhum produto vendido encontrado.")
        return

    for i, (produto, quantidade) in enumerate(produtos_mais_vendidos, 1):
        print(f"{i}. {produto.nome} - {quantidade} unidades (R$ {produto.preco:.2f} cada)")


def exibir_tendencia_vendas(tendencia: List[Tuple[datetime, float]]) -> None:
    """Exibe a tendência de vendas dos últimos dias."""
    exibir_titulo("TENDÊNCIA DE VENDAS DIÁRIAS")

    if not tendencia:
        print("Nenhuma movimentação registrada no período.")
        return

    max_valor = max(valor for _, valor in tendencia)
    for data, valor in tendencia:
        barra = "█" * int((valor / max_valor) * 20) if max_valor > 0 else ""
        print(f"{data.strftime('%d/%m/%Y')} | R$ {valor:9.2f} | {barra}")


def exibir_lista_produtos(repositorio: RepositorioDados) -> None:
    """Exibe todos os produtos cadastrados no repositório."""
    exibir_titulo("PRODUTOS CADASTRADOS")
    if not repositorio.produtos:
        print("Nenhum produto cadastrado.")
        return

    for produto in repositorio.produtos:
        print(
            f"ID: {produto.id:02d} | {produto.nome:<20} | "
            f"Categoria: {produto.categoria:<15} | R$ {produto.preco:.2f}"
        )