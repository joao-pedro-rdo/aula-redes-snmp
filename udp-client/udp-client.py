import socket
import time
import argparse
import json
import statistics


# Função para enviar uma requisição e receber a resposta
def send_request(sock, server_address, request):
    sock.sendto(request.encode(), server_address)
    response, _ = sock.recvfrom(1024)
    return response.decode()


# Função para executar múltiplas requisições ao servidor
def execute_requests(host, port, num_requests, verbose, command):
    times = []
    server_address = (host, port)
    command = " ".join(command)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for _ in range(num_requests):
        start_time = time.time()  # Marca o tempo de início
        response = send_request(sock, server_address, command)  # Envia a requisição
        elapsed_time = time.time() - start_time  # Calcula o tempo de resposta
        times.append(elapsed_time)  # Adiciona o tempo à lista
        if verbose:
            print(
                f"Response: {response}"
            )  # Exibe a resposta se `verbose` estiver ativado

    sock.close()
    return times


# Função para calcular estatísticas de desempenho
def log_performance(times, log_file=None):
    if not times or not all(isinstance(t, (int, float)) for t in times):
        print("Invalid or empty times list provided.")  # Lista vazia ou inválida
        return {}

    # Converte tempos para milissegundos para melhorar a apresentação
    times_ms = [t * 1000 for t in times]

    # Calcula as estatísticas em milissegundos
    stats = {
        "tempo_de_execucao_total_ms": round(sum(times_ms), 3),
        "tempo_medio_ms": round(statistics.mean(times_ms), 3),
        "tempo_minimo_ms": round(min(times_ms), 3),
        "tempo_maximo_ms": round(max(times_ms), 3),
        "desvio_padrao_ms": round(
            statistics.stdev(times_ms) if len(times_ms) > 1 else 0, 3
        ),
    }

    # Salva as estatísticas em um arquivo, se especificado
    if log_file:
        try:
            with open(log_file, "w") as file:
                file.write(str(stats))
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    return stats


# Função para analisar os argumentos da linha de comando
def parse_arguments():
    parser = argparse.ArgumentParser(description="Cliente UDP para enviar comandos.")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Endereço do servidor"
    )
    parser.add_argument("--port", type=int, default=8081, help="Porta do servidor")
    parser.add_argument(
        "--requests", type=int, default=10, help="Número de requisições"
    )
    parser.add_argument("--verbose", action="store_true", help="Imprimir respostas")
    parser.add_argument("--log", type=str, help="Arquivo de log para resultados")
    parser.add_argument(
        "--command", type=str, nargs="+", default="INFO", help="Comando a ser enviado"
    )
    parser.add_argument("--keep")
    parser.add_argument("--session")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    times = execute_requests(
        args.host, args.port, args.requests, args.verbose, args.command
    )
    stats = log_performance(times, args.log)
    print(json.dumps(stats))
