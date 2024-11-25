import pandas as pd
import matplotlib.pyplot as plt


def genrate_praphics(arquivo_csv):
    """
    Gera gráficos a partir de um arquivo CSV com métricas de desempenho.

    Parâmetros:
    - arquivo_csv (str): Caminho para o arquivo CSV contendo os dados.
    """
    try:
        # Carregar o CSV em um DataFrame
        df = pd.read_csv(arquivo_csv)

        # Configuração do estilo do gráfico (opcional)
        plt.style.use("ggplot")

        # 1. Gráfico de Linha para o Tempo Total de Execução
        plt.figure(figsize=(10, 6))
        plt.plot(
            df["indentifier"],
            df["tempo_de_execucao_total_ms"],
            marker="o",
            label="Tempo Total de Execução (ms)",
        )
        plt.title("Tempo Total de Execução por Identificador")
        plt.xlabel("Identificador")
        plt.ylabel("Tempo Total de Execução (ms)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("tempo_total_execucao.png")
        plt.show()

        # 2. Gráfico de Dispersão para Tempo Médio vs Tempo Máximo
        plt.figure(figsize=(10, 6))
        plt.scatter(
            df["tempo_medio_ms"], df["tempo_maximo_ms"], color="blue", alpha=0.7
        )
        plt.title("Tempo Médio vs Tempo Máximo")
        plt.xlabel("Tempo Médio (ms)")
        plt.ylabel("Tempo Máximo (ms)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("tempo_medio_vs_maximo.png")
        plt.show()

        # 3. Gráfico de Barras para Desvio Padrão
        plt.figure(figsize=(10, 6))
        plt.bar(
            df["indentifier"],
            df["desvio_padrao_ms"],
            color="orange",
            label="Desvio Padrão (ms)",
        )
        plt.title("Desvio Padrão por Identificador")
        plt.xlabel("Identificador")
        plt.ylabel("Desvio Padrão (ms)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig("desvio_padrao.png")
        plt.show()

        print("Gráficos gerados com sucesso e salvos como imagens!")

    except Exception as e:
        print(f"Erro ao gerar gráficos: {e}")
