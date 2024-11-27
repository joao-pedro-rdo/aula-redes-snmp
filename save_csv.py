import csv
import json
import os


def process_stdout(stdout):
    """
    Processa a string stdout para extrair os valores das métricas em formato JSON.
    """
    try:
        # Tenta localizar e carregar o JSON presente no stdout
        if "{" in stdout and "}" in stdout:
            start_index = stdout.index("{")
            json_data = json.loads(stdout[start_index:])
            return json_data
        else:
            return {}
    except (ValueError, json.JSONDecodeError):
        return {}


def save_csv(output_file, new_output):
    # Define os campos para o CSV
    fields = [
        "execution_location",
        "requests",
        "command",
        "keep",
        "print_written",
        "file_written",
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
        "print_written": new_output.get("print_written", ""),
        "file_written": new_output.get("file_written", ""),
        "tempo_de_execucao_total_ms": metrics.get("tempo_de_execucao_total_ms", ""),
        "tempo_medio_ms": metrics.get("tempo_medio_ms", ""),
        "tempo_minimo_ms": metrics.get("tempo_minimo_ms", ""),
        "tempo_maximo_ms": metrics.get("tempo_maximo_ms", ""),
        "desvio_padrao_ms": metrics.get("desvio_padrao_ms", ""),
        "stderr": new_output.get("stderr", ""),
        "returncode": new_output.get("returncode", ""),
    }

    # Abre ou cria o arquivo CSV
    file_exists = os.path.isfile(output_file)
    with open(output_file, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # Escreve o cabeçalho apenas na primeira vez
        if not file_exists:
            writer.writeheader()

        # Adiciona a nova linha com os dados
        writer.writerow(csv_row)

    print(f"Saída adicionada ao arquivo {output_file}")
