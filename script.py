import json
import matplotlib.pyplot as plt


def calculate_percentage_difference(tcp_stats, udp_stats):
    """
    Calcula a diferença percentual entre as métricas TCP e UDP.
    """
    comparison = {}
    for key in tcp_stats:
        if key in udp_stats:
            tcp_value = tcp_stats[key]
            udp_value = udp_stats[key]
            if isinstance(tcp_value, (int, float)) and tcp_value != 0:
                percentage_diff = ((udp_value - tcp_value) / tcp_value) * 100
                comparison[key] = round(percentage_diff, 2)
    return comparison


def plot_comparison(tcp_combined_stats, udp_combined_stats, comparison):
    """
    Gera gráficos comparando as métricas TCP e UDP e os salva como arquivos de imagem.
    """
    # Extraindo as chaves e valores das métricas combinadas
    common_keys = list(tcp_combined_stats.keys())
    tcp_values = list(tcp_combined_stats.values())
    udp_values = list(udp_combined_stats.values())
    percentage_diffs = [comparison.get(key, 0) for key in common_keys]

    # Gráfico de barras comparando os valores
    plt.figure(figsize=(12, 8))
    x = range(len(common_keys))
    plt.bar(x, tcp_values, width=0.4, label="TCP", align="center")
    plt.bar([i + 0.4 for i in x], udp_values, width=0.4, label="UDP", align="center")
    plt.xticks([i + 0.2 for i in x], common_keys, rotation=45)
    plt.title("Comparação de Métricas: TCP vs UDP")
    plt.xlabel("Métricas")
    plt.ylabel("Valores (ms)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("tcp_vs_udp_combined_comparison.png")  # Salva o gráfico em um arquivo de imagem
    plt.close()

    # Gráfico de porcentagens
    plt.figure(figsize=(12, 8))
    plt.bar(common_keys, percentage_diffs, color="orange")
    plt.title("Diferença Percentual: TCP vs UDP")
    plt.xlabel("Métricas")
    plt.ylabel("Diferença (%)")
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("percentage_combined_difference.png")  # Salva o gráfico em um arquivo de imagem
    plt.close()


if __name__ == "__main__":
    # Dados originais
    original_data = """
    {
    "tcp_stats": {
        "tempo_de_execucao_total_ms": 66.471,
        "tempo_medio_ms": 0.066,
        "tempo_minimo_ms": 0.054,
        "tempo_maximo_ms": 0.209,
        "desvio_padrao_ms": 0.016
    },
    "udp_stats": {
        "tempo_de_execucao_total_ms": 67.711,
        "tempo_medio_ms": 0.068,
        "tempo_minimo_ms": 0.053,
        "tempo_maximo_ms": 0.28
    }
    }
    """

    # Novos dados para TCP e UDP
    new_data = """
    {
    "tcp_stats": {
        "tempo_de_execucao_total_ms": 92.288,
        "tempo_medio_ms": 0.092,
        "tempo_minimo_ms": 0.061,
        "tempo_maximo_ms": 0.271,
        "desvio_padrao_ms": 0.017
    },
    "udp_stats": {
        "tempo_de_execucao_total_ms": 101.071,
        "tempo_medio_ms": 0.101,
        "tempo_minimo_ms": 0.072,
        "tempo_maximo_ms": 0.273,
        "desvio_padrao_ms": 0.019
    }
    }
    """

    # Parse dos dados JSON para dicionários
    original_parsed = json.loads(original_data)
    new_parsed = json.loads(new_data)

    # Combinação das métricas em um único dicionário
    tcp_combined_stats = {**original_parsed["tcp_stats"], **new_parsed["tcp_stats"]}
    udp_combined_stats = {**original_parsed["udp_stats"], **new_parsed["udp_stats"]}

    # Calcula a diferença percentual entre as métricas combinadas
    combined_comparison = calculate_percentage_difference(tcp_combined_stats, udp_combined_stats)

    # Gera os gráficos e salva os arquivos
    plot_comparison(tcp_combined_stats, udp_combined_stats, combined_comparison)

    print("Gráficos atualizados salvos como 'tcp_vs_udp_combined_comparison.png' e 'percentage_combined_difference.png'.")
