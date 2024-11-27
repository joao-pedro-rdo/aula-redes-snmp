import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi


def generate_graphics(arquivo_csv):
    """
    Gera gráficos avançados para análise de desempenho a partir de um arquivo CSV.

    Parâmetros:
    - arquivo_csv (str): Caminho para o arquivo CSV contendo os dados.
    """
    try:
        # Carregar o CSV em um DataFrame
        df = pd.read_csv(arquivo_csv)

        # Configuração do estilo do gráfico
        plt.style.use("ggplot")

        # 1. Resumo Estatístico
        summary = df.groupby(["local_execucao", "comando"]).agg(
            media=("tempo_execucao_total_ms", "mean"),
            mediana=("tempo_execucao_total_ms", "median"),
            minimo=("tempo_execucao_total_ms", "min"),
            maximo=("tempo_execucao_total_ms", "max"),
            desvio=("tempo_execucao_total_ms", "std"),
        )
        print("Resumo Estatístico:")
        print(summary)

        # 2. Heatmap para Comparação de Desempenho
        pivot = df.pivot_table(
            index="comando",
            columns="numero_requisicoes",
            values="tempo_execucao_total_ms",
            aggfunc="mean",
        )
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Heatmap: Tempo Médio de Execução por Comando e Requisição")
        plt.xlabel("Número de Requisições")
        plt.ylabel("Comando")
        plt.tight_layout()
        plt.savefig("heatmap_tempo_execucao.png")

        # 3. Gráfico de Velocidade Relativa
        df["relativo"] = df.groupby("comando")["tempo_execucao_total_ms"].transform(
            lambda x: x / x.min()
        )
        plt.figure(figsize=(10, 6))
        sns.boxplot(
            x="local_execucao",
            y="relativo",
            data=df,
            palette="muted",
        )
        plt.title("Velocidade Relativa por Local de Execução")
        plt.xlabel("Local de Execução")
        plt.ylabel("Velocidade Relativa")
        plt.tight_layout()
        plt.savefig("velocidade_relativa.png")

        # 4. Distribuição de Tempos com Violin Plot
        plt.figure(figsize=(12, 8))
        sns.violinplot(
            x="numero_requisicoes",
            y="tempo_execucao_total_ms",
            hue="local_execucao",
            data=df,
            split=True,
            palette="muted",
        )
        plt.title("Distribuição de Tempo por Número de Requisições e Local")
        plt.xlabel("Número de Requisições")
        plt.ylabel("Tempo Total de Execução (ms)")
        plt.tight_layout()
        plt.savefig("distribuicao_tempo.png")

        # 5. Evolução do Tempo Médio com Erro
        means = df.groupby("numero_requisicoes")["tempo_execucao_total_ms"].mean()
        stds = df.groupby("numero_requisicoes")["tempo_execucao_total_ms"].std()
        plt.figure(figsize=(10, 6))
        plt.errorbar(
            means.index,
            means,
            yerr=stds,
            fmt="o-",
            capsize=5,
            label="Tempo Médio (ms)",
        )
        plt.title("Evolução do Tempo Médio com Margem de Erro")
        plt.xlabel("Número de Requisições")
        plt.ylabel("Tempo Médio de Execução (ms)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("evolucao_tempo_medio.png")

        # 6. Radar Chart para Comparação Geral
        metrics = ["tempo_execucao_total_ms", "tempo_medio_ms", "desvio_padrao_ms"]
        summary_radar = df.groupby("local_execucao")[metrics].mean()

        # Preparar dados para radar
        labels = summary_radar.columns
        num_vars = len(labels)
        angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
        angles += angles[:1]

        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, polar=True)
        for idx, row in summary_radar.iterrows():
            values = row.tolist() + row.tolist()[:1]
            ax.plot(angles, values, label=idx)
            ax.fill(angles, values, alpha=0.1)

        plt.xticks(angles[:-1], labels)
        plt.title("Comparação de Desempenho por Local")
        plt.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig("radar_comparacao.png")

        print("Gráficos avançados gerados com sucesso e salvos como imagens!")

    except Exception as e:
        print(f"Erro ao gerar gráficos: {e}")


# Exemplo de uso
# generate_advanced_graphics("resultados.csv")
