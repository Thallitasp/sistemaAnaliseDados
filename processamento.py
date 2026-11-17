# processamento.py
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from modelo import Produto, RepositorioDados, Venda


def filtrar_vendas_por_periodo(
    vendas: List[Venda],
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
) -> List[Venda]:
    """
    Filtra uma lista de vendas dentro de um intervalo de datas (inclusive).

    Args:
        vendas: Lista completa de vendas
        data_inicio: Data inicial do filtro (opcional)
        data_fim: Data final do filtro (opcional)

    Returns:
        List[Venda]: Vendas ocorridas no período especificado
    """
    vendas_filtradas = []
    for venda in vendas:
        data_venda = venda.data.date()
        if data_inicio and data_venda < data_inicio.date():
            continue
        if data_fim and data_venda > data_fim.date():
            continue
        vendas_filtradas.append(venda)
    return vendas_filtradas


def calcular_total_vendas(
    repositorio: RepositorioDados,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
) -> float:
    """
    Calcula o valor total de todas as vendas (ou dentro de um período).

    Args:
        repositorio: Repositório contendo produtos e vendas
        data_inicio: Data inicial opcional
        data_fim: Data final opcional

    Returns:
        float: Valor total das vendas
    """
    vendas = filtrar_vendas_por_periodo(repositorio.vendas, data_inicio, data_fim)
    total = 0.0
    for venda in vendas:
        produto = repositorio.buscar_produto_por_id(venda.produto_id)
        if produto:
            total += produto.preco * venda.quantidade
    return total


def calcular_vendas_por_categoria(
    repositorio: RepositorioDados,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
) -> Dict[str, float]:
    """
    Calcula o total de vendas por categoria.

    Args:
        repositorio: Repositório contendo produtos e vendas
        data_inicio: Data inicial opcional
        data_fim: Data final opcional

    Returns:
        Dict[str, float]: Dicionário mapeando categorias para valores totals
    """
    vendas = filtrar_vendas_por_periodo(repositorio.vendas, data_inicio, data_fim)
    vendas_por_categoria: Dict[str, float] = {}

    for venda in vendas:
        produto = repositorio.buscar_produto_por_id(venda.produto_id)
        if produto:
            valor_venda = produto.preco * venda.quantidade
            vendas_por_categoria[produto.categoria] = (
                vendas_por_categoria.get(produto.categoria, 0.0) + valor_venda
            )

    return vendas_por_categoria


def calcular_produtos_mais_vendidos(
    repositorio: RepositorioDados,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
) -> List[Tuple[Produto, int]]:
    """
    Retorna os produtos ordenados pela quantidade total vendida (decrescente).

    Args:
        repositorio: Repositório contendo produtos e vendas
        data_inicio: Data inicial opcional
        data_fim: Data final opcional

    Returns:
        List[Tuple[Produto, int]]: Lista de tuplas (Produto, quantidade_vendida)
    """
    vendas = filtrar_vendas_por_periodo(repositorio.vendas, data_inicio, data_fim)
    contagem_produtos: Dict[int, int] = {}

    for venda in vendas:
        contagem_produtos[venda.produto_id] = (
            contagem_produtos.get(venda.produto_id, 0) + venda.quantidade
        )

    ranking: List[Tuple[Produto, int]] = []
    for produto_id, qtd in contagem_produtos.items():
        produto = repositorio.buscar_produto_por_id(produto_id)
        if produto:
            ranking.append((produto, qtd))

    ranking.sort(key=lambda item: item[1], reverse=True)
    return ranking


def analisar_tendencia_vendas(
    repositorio: RepositorioDados,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
) -> List[Tuple[datetime, float]]:
    """
    Agrupa o faturamento diário em ordem cronológica para análise de tendência.

    Args:
        repositorio: Repositório contendo produtos e vendas
        data_inicio: Data inicial opcional
        data_fim: Data final opcional

    Returns:
        List[Tuple[datetime, float]]: Lista de tuplas (data, valor_total_dia)
    """
    vendas = filtrar_vendas_por_periodo(repositorio.vendas, data_inicio, data_fim)
    vendas_por_dia: Dict[datetime, float] = {}

    for venda in vendas:
        produto = repositorio.buscar_produto_por_id(venda.produto_id)
        if produto:
            dia = datetime(venda.data.year, venda.data.month, venda.data.day)
            valor = produto.preco * venda.quantidade
            vendas_por_dia[dia] = vendas_por_dia.get(dia, 0.0) + valor

    return sorted(vendas_por_dia.items(), key=lambda item: item[0])