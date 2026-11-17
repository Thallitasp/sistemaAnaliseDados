# 📊 Sistema de Análise de Dados de Vendas (`sistemaAnaliseDados`)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Licença](https://img.shields.io/badge/Licença-Acadêmica-lightgrey)

Sistema modular desenvolvido em **Python** para gerenciamento, processamento estatístico e visualização de dados de vendas via interface de linha de comando (CLI). O projeto aplica estruturas de dados básicas, programação orientada a objetos, tipagem estática (*type hints*), documentação padronizada (*docstrings*), validação de entradas, tratamento de exceções e persistência local em arquivo **JSON**.

> **Contexto Acadêmico:** Atividade Prática 2 — Disciplina de *Algoritmos e Estrutura de Dados* | Curso de Análise e Desenvolvimento de Sistemas (2026).

---

## 📑 Índice

1. [Objetivo do Projeto](#-objetivo-do-projeto)
2. [Funcionalidades](#-funcionalidades)
3. [Arquitetura e Estrutura de Pastas](#-arquitetura-e-estrutura-de-pastas)
4. [Detalhamento dos Módulos](#-detalhamento-dos-módulos)
5. [Modelo de Persistência (JSON)](#-modelo-de-persistência-json)
6. [Como Executar](#-como-executar)
7. [Exemplos de Uso e Saída](#-exemplos-de-uso-e-saída)
8. [Tratamento de Erros e Validações](#-tratamento-de-erros-e-validações)
9. [Autoria](#-autoria)

---

## 🎯 Objetivo do Projeto

Demonstrar na prática a construção de um sistema de software limpo e desacoplado utilizando apenas a biblioteca padrão do Python, estruturando a lógica em camadas independentes (dados, processamento, apresentação e controle) para transformar registros brutos de transações em indicadores gerenciais claros.

---

## ✨ Funcionalidades

- **Análises Estatísticas Completas:**
  - **Total de Vendas:** Cálculo consolidado do faturamento bruto (`R$`).
  - **Vendas por Categoria:** Agrupamento de receita por segmento com cálculo de participação percentual (`%`) ordenado do maior para o menor.
  - **Ranking de Produtos:** Classificação dos itens mais vendidos por volume de unidades comercializadas.
  - **Tendência Temporal:** Agrupamento cronológico do faturamento diário acompanhado de gráfico de barras horizontal renderizado no terminal.
- **Filtragem Dinâmica por Período:**
  - Permite aplicar recortes de data inicial e/ou final (`DD/MM/AAAA`) sobre todas as métricas analíticas simultaneamente, aceitando intervalos abertos.
- **Operações de Cadastro e Movimentação:**
  - Inclusão de novos produtos com atribuição automática de identificador único (`id`).
  - Registro de novas vendas vinculadas a produtos existentes, com suporte a data personalizada ou captura automática de data/hora atual.
  - Consulta tabulada de todo o catálogo de produtos cadastrados.
- **Persistência Automática:**
  - Leitura e gravação automática do estado do sistema em `dados_vendas.json`.
  - Carga inicial de dados de exemplo caso o arquivo JSON ainda não exista.

---

## 📁 Arquitetura e Estrutura de Pastas

text
sistemaAnaliseDados/
├── modelo.py           # Camada de Dados: entidades Produto, Venda e RepositorioDados
├── processamento.py    # Camada de Negócio: filtros e algoritmos de cálculo estatístico
├── visualizacao.py     # Camada de Apresentação: menus, tabelas e gráficos ASCII
├── main.py             # Camada de Controle: orquestração do fluxo e validação de inputs
├── dados_vendas.json   # Banco de dados local em JSON (criado automaticamente)
└── README.md           # Documentação técnica do projeto

---

## 🧩 Detalhamento dos Módulos

### 1. `modelo.py`
Define as estruturas de dados e gerencia a persistência em disco:
- **`Produto`:** Representa um item do catálogo (`id: int`, `nome: str`, `categoria: str`, `preco: float`), com métodos `to_dict()` e `from_dict()` para serialização.
- **`Venda`:** Representa uma transação comercial (`id: int`, `data: datetime`, `produto_id: int`, `quantidade: int`).
- **`RepositorioDados`:** Centraliza as listas em memória (`produtos` e `vendas`), realiza buscas por ID, gera novos registros sequenciais e executa `salvar_dados()` / `carregar_dados()` em JSON.

### 2. `processamento.py`
Contém funções puras de análise e agregação de dados:
- `filtrar_vendas_por_periodo()`: Filtra transações dentro de um intervalo de datas (`data_inicio` e `data_fim`).
- `calcular_total_vendas()`: Soma o valor monetário (`preco * quantidade`) das vendas válidas.
- `calcular_vendas_por_categoria()`: Retorna um dicionário `Dict[str, float]` mapeando cada categoria ao seu faturamento.
- `calcular_produtos_mais_vendidos()`: Retorna uma lista ordenada `List[Tuple[Produto, int]]` do produto mais vendido ao menos vendido.
- `analisar_tendencia_vendas()`: Consolida o faturamento por dia em ordem cronológica `List[Tuple[datetime, float]]`.

### 3. `visualizacao.py`
Responsável exclusivamente pela formatação visual no console:
- `exibir_menu()`: Renderiza o menu principal interativo.
- `exibir_total_vendas()`, `exibir_vendas_por_categoria()`, `exibir_produtos_mais_vendidos()`: Formatam os indicadores com alinhamento e casas decimais padronizadas.
- `exibir_tendencia_vendas()`: Gera barras proporcionais (`█`) para facilitar a leitura visual da evolução diária.
- `exibir_lista_produtos()`: Lista todos os produtos cadastrados em formato de tabela.

### 4. `main.py`
Controla o ciclo de vida da aplicação:
- Inicializa o repositório e carrega ou cria o arquivo `dados_vendas.json`.
- Implementa funções auxiliares de leitura segura (`ler_data`, `ler_inteiro`, `ler_float`).
- Gerencia o loop principal do menu e conecta as entradas do usuário às funções de processamento e visualização.

---

## 💾 Modelo de Persistência (JSON)

Os dados são armazenados localmente no arquivo `dados_vendas.json` seguindo a estrutura abaixo:

json
{
    "produtos": [
        {
            "id": 1,
            "nome": "Notebook Pro",
            "categoria": "Eletrônicos",
            "preco": 4500.0
        }
    ],
    "vendas": [
        {
            "id": 1,
            "data": "2026-11-10 14:30:00",
            "produto_id": 1,
            "quantidade": 2
        }
    ]
}

---

## 🚀 Como Executar

### Pré-requisitos
- **Python 3.8 ou superior** instalado.
- Não há dependências externas (`pip install` não é necessário).

### Passo a passo
1. Clone o repositório ou baixe os arquivos para sua máquina:
   bash
   git clone [https://github.com/seu-usuario/sistema-analise-dados.git](https://github.com/seu-usuario/sistema-analise-dados.git)
   
2. Acesse o diretório do projeto no terminal:
   bash
   cd sistemaAnaliseDados
   
3. Execute o arquivo principal:
   - **Windows (PowerShell / CMD):**
     powershell
     py main.py
     
   - **Linux / macOS:**
     bash
     python3 main.py
     

---

## 🖥️ Exemplos de Uso e Saída

### Menu Principal
text
==================================================
           SISTEMA DE ANÁLISE DE VENDAS
==================================================
1 - Exibir Total de Vendas
2 - Exibir Vendas por Categoria
3 - Exibir Produtos Mais Vendidos
4 - Exibir Tendência de Vendas
5 - Filtrar Análises por Período
6 - Adicionar Novo Produto
7 - Registrar Nova Venda
8 - Listar Produtos Cadastrados
0 - Salvar e Sair
==================================================
Escolha uma opção:

### Exemplo de Relatório — Vendas por Categoria
text
==================================================
               VENDAS POR CATEGORIA
==================================================
Eletrônicos: R$ 16300.00 (86.4%)
Periféricos: R$ 2130.00 (11.3%)
Móveis: R$ 980.00 (5.2%)

### Exemplo de Relatório — Tendência de Vendas Diárias
text
==================================================
           TENDÊNCIA DE VENDAS DIÁRIAS
==================================================
10/11/2026 | R$   9000.00 | ████████████████████
11/11/2026 | R$    600.00 | █
12/11/2026 | R$   1050.00 | ██

---

## 🛡️ Tratamento de Erros e Validações

O sistema foi projetado para impedir falhas inesperadas durante o uso:
- **Validação de Tipos e Domínio (`ValueError`):** Bloqueia preços ou quantidades menores ou iguais a zero, nomes/categorias em branco, textos digitados em campos numéricos e datas fora do padrão `DD/MM/AAAA`.
- **Integridade Referencial (`LookupError`):** Impede o registro de vendas para IDs de produtos inexistentes.
- **Consistência Temporal:** Impede consultas onde a data inicial seja posterior à data final.
- **Resiliência de Arquivo (`IOError`, `RuntimeError`, `JSONDecodeError`):** Caso o arquivo `dados_vendas.json` esteja corrompido ou ilegível, o sistema informa o usuário e restaura automaticamente a base padrão sem interromper a execução.

---

## 👩‍💻 Autoria

Desenvolvido por **Thallita da Silva Pedreira**  
Curso de **Análise e Desenvolvimento de Sistemas** — 2026