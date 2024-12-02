import csv
import json
import os

AMBIENTE = "windows"


def process_stdout(stdout):
    """
    Processa a string stdout para extrair os valores das métricas em formato JSON.
    """
    try:
        # Filtra apenas a linha contendo JSON
        json_lines = [
            line for line in stdout.splitlines() if line.strip().startswith("{")
        ]
        if json_lines:
            return json.loads(json_lines[0])  # Carrega o primeiro JSON encontrado
        print(stdout)
        return {}
    except (ValueError, json.JSONDecodeError):
        return {}


def save_csv(new_output):
    """
    Salva os dados de saída em um arquivo CSV
    """
    # Define os campos para o CSV
    fields = [
        "execution_location",
        "requests",
        "command",
        "keep",
        "print_written",
        "file_written",
        "verbose",  # Adicionado aqui
        "tempo_de_execucao_total_ms",
        "tempo_medio_ms",
        "tempo_minimo_ms",
        "tempo_maximo_ms",
        "desvio_padrao_ms",
        "stderr",
        "returncode",
    ]

    # Processa o stdout para extrair métricas
    metrics = process_stdout(new_output.get("stdout", ""))

    # Monta os dados para a linha do CSV
    csv_row = {
        "execution_location": new_output.get("execution_location", ""),
        "requests": new_output.get("requests", ""),
        "command": new_output.get("command", ""),
        "keep": new_output.get("keep", ""),
        "verbose": new_output.get("verbose", ""),
        "file_written": new_output.get("file_written", ""),
        "tempo_de_execucao_total_ms": metrics.get("tempo_de_execucao_total_ms", ""),
        "tempo_medio_ms": metrics.get("tempo_medio_ms", ""),
        "tempo_minimo_ms": metrics.get("tempo_minimo_ms", ""),
        "tempo_maximo_ms": metrics.get("tempo_maximo_ms", ""),
        "desvio_padrao_ms": metrics.get("desvio_padrao_ms", ""),
        "stderr": new_output.get("stderr", ""),
        "returncode": new_output.get("returncode", ""),
    }

    # Criar o nome do arquivo dinamicamente
    folder = "metricas/linux" if AMBIENTE == "linux" else "metricas/windows"
    file_name = f"{AMBIENTE}_{new_output['execution_location']}_{new_output['requests']}_{new_output['command']}_{new_output['keep']}_verbose:{str(new_output['verbose'])}.csv"
    output_path = os.path.join(folder, file_name)

    # Garante que o diretório existe
    os.makedirs(folder, exist_ok=True)

    # Abre ou cria o arquivo CSV
    file_exists = os.path.isfile(output_path)
    with open(output_path, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # Escreve o cabeçalho apenas na primeira vez
        if not file_exists:
            writer.writeheader()

        # Adiciona a nova linha com os dados
        writer.writerow(csv_row)

    print(f"Saída adicionada ao arquivo {output_path}")
