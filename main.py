# main.py
from datetime import datetime
from typing import Optional
from modelo import RepositorioDados
import processamento
import visualizacao


def ler_data(mensagem: str) -> Optional[datetime]:
    """Lê e valida uma data no formato DD/MM/AAAA."""
    while True:
        entrada = input(mensagem).strip()
        if not entrada:
            return None
        try:
            return datetime.strptime(entrada, "%d/%m/%Y")
        except ValueError:
            print("Formato inválido! Use DD/MM/AAAA (ex: 16/11/2026) ou Enter para ignorar.")


def ler_inteiro(mensagem: str) -> int:
    """Lê e valida um número inteiro positivo."""
    while True:
        try:
            valor = int(input(mensagem).strip())
            if valor <= 0:
                print("Digite um número inteiro maior que zero.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")


def ler_float(mensagem: str) -> float:
    """Lê e valida um número decimal positivo."""
    while True:
        try:
            entrada = input(mensagem).strip().replace(",", ".")
            valor = float(entrada)
            if valor <= 0:
                print("Digite um valor maior que zero.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida! Digite um valor numérico válido.")


def fluxo_adicionar_produto(repositorio: RepositorioDados) -> None:
    """Coleta dados do usuário e cadastra um novo produto."""
    visualizacao.exibir_titulo("CADASTRAR NOVO PRODUTO")
    try:
        nome = input("Nome do produto: ").strip()
        categoria = input("Categoria: ").strip()
        preco = ler_float("Preço unitário (R$): ")

        produto = repositorio.adicionar_produto(nome, categoria, preco)
        repositorio.salvar_dados()
        print(f"\nProduto cadastrado com sucesso! {produto}")
    except ValueError as e:
        print(f"\nErro de validação: {e}")
    except IOError as e:
        print(f"\nAviso ao salvar: {e}")


def fluxo_registrar_venda(repositorio: RepositorioDados) -> None:
    """Coleta dados do usuário e registra uma nova venda."""
    visualizacao.exibir_titulo("REGISTRAR NOVA VENDA")
    if not repositorio.produtos:
        print("Cadastre ao menos um produto antes de registrar vendas.")
        return

    visualizacao.exibir_lista_produtos(repositorio)
    try:
        produto_id = ler_inteiro("\nInforme o ID do produto vendido: ")
        quantidade = ler_inteiro("Informe a quantidade vendida: ")
        data_venda = ler_data("Data da venda (DD/MM/AAAA) [Enter para data/hora atual]: ")

        venda = repositorio.registrar_venda(produto_id, quantidade, data_venda)
        repositorio.salvar_dados()
        print(f"\nVenda registrada com sucesso! {venda}")
    except (ValueError, LookupError) as e:
        print(f"\nErro ao registrar venda: {e}")
    except IOError as e:
        print(f"\nAviso ao salvar: {e}")


def fluxo_analise_por_periodo(repositorio: RepositorioDados) -> None:
    """Executa todas as análises filtradas por um intervalo de datas."""
    visualizacao.exibir_titulo("ANÁLISE POR PERÍODO")
    print("Pressione Enter para deixar uma das extremidades em aberto.")
    data_inicio = ler_data("Data inicial (DD/MM/AAAA): ")
    data_fim = ler_data("Data final (DD/MM/AAAA): ")

    if data_inicio and data_fim and data_inicio > data_fim:
        print("\nErro: A data inicial não pode ser posterior à data final.")
        return

    total = processamento.calcular_total_vendas(repositorio, data_inicio, data_fim)
    por_categoria = processamento.calcular_vendas_por_categoria(
        repositorio, data_inicio, data_fim
    )
    mais_vendidos = processamento.calcular_produtos_mais_vendidos(
        repositorio, data_inicio, data_fim
    )
    tendencia = processamento.analisar_tendencia_vendas(
        repositorio, data_inicio, data_fim
    )

    visualizacao.exibir_total_vendas(total)
    visualizacao.exibir_vendas_por_categoria(por_categoria)
    visualizacao.exibir_produtos_mais_vendidos(mais_vendidos)
    visualizacao.exibir_tendencia_vendas(tendencia)


def main() -> None:
    """Função principal do sistema."""
    repositorio = RepositorioDados()

    try:
        if not repositorio.carregar_dados():
            repositorio.carregar_dados_exemplo()
            repositorio.salvar_dados()
            print("Base inicial de exemplo criada em 'dados_vendas.json'.")
        else:
            print("Dados carregados de 'dados_vendas.json'.")
    except RuntimeError as e:
        print(f"Aviso: {e}. Carregando dados padrão de exemplo.")
        repositorio.carregar_dados_exemplo()

    while True:
        opcao = visualizacao.exibir_menu()

        if opcao == "0":
            try:
                repositorio.salvar_dados()
                print("\nDados salvos com sucesso. Encerrando o sistema... Até logo!")
            except IOError as e:
                print(f"\nErro ao salvar antes de sair: {e}")
            break

        elif opcao == "1":
            total = processamento.calcular_total_vendas(repositorio)
            visualizacao.exibir_total_vendas(total)

        elif opcao == "2":
            vendas_por_categoria = processamento.calcular_vendas_por_categoria(repositorio)
            visualizacao.exibir_vendas_por_categoria(vendas_por_categoria)

        elif opcao == "3":
            produtos_mais_vendidos = processamento.calcular_produtos_mais_vendidos(
                repositorio
            )
            visualizacao.exibir_produtos_mais_vendidos(produtos_mais_vendidos)

        elif opcao == "4":
            tendencia = processamento.analisar_tendencia_vendas(repositorio)
            visualizacao.exibir_tendencia_vendas(tendencia)

        elif opcao == "5":
            fluxo_analise_por_periodo(repositorio)

        elif opcao == "6":
            fluxo_adicionar_produto(repositorio)

        elif opcao == "7":
            fluxo_registrar_venda(repositorio)

        elif opcao == "8":
            visualizacao.exibir_lista_produtos(repositorio)

        else:
            print("\nOpção inválida! Escolha uma opção entre 0 e 8.")


if __name__ == "__main__":
    main()