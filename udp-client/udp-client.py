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
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command = " ".join(command)
    for _ in range(num_requests):
        start_time = time.time()
        response = send_request(sock, server_address, command)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        if verbose:
            print(f"Response: {response}")

    sock.close()
    return times

def log_performance(times, log_file=None):
    if not times or not all(isinstance(t, (int, float)) for t in times):
        print("Invalid or empty times list provided.")  # Lista vazia ou inválida
        return {}

    # Converte tempos para milissegundos para melhorar a apresentação
    times_ms = [t * 1000 for t in times]  # Converte segundos para milissegundos

    # Calcula as estatísticas em milissegundos
    execution_time = sum(times_ms)
    avg_time = statistics.mean(times_ms)
    min_time = min(times_ms)
    max_time = max(times_ms)
    std_dev = statistics.stdev(times_ms) if len(times_ms) > 1 else 0

    # # Calcula as estatísticas dos tempos
    # execution_time = sum(times)  # Tempo total de execução
    # avg_time = statistics.mean(times)  # Tempo médio
    # min_time = min(times)  # Tempo mínimo
    # max_time = max(times)  # Tempo máximo
    # std_dev = statistics.stdev(times) if len(times) > 1 else 0  # Desvio padrão

    # Cria um dicionário de estatísticas
    stats = {
        "tempo_de_execucao_total_ms": round(execution_time, 3),
        "tempo_medio_ms": round(avg_time, 3),
        "tempo_minimo_ms": round(min_time, 3),
        "tempo_maximo_ms": round(max_time, 3),
        "desvio_padrao_ms": round(std_dev, 3),
    }

    # Imprime as estatísticas formatadas
    # print("Performance statistics (in milliseconds):")
    # for key, value in stats.items():
    #     print(f"{key}: {value} ms")

    # Salva as estatísticas em um arquivo, se especificado
    if log_file:
        try:
            with open(log_file, "w") as file:
                file.write(str(stats))  # Escreve os resultados no arquivo
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    return stats

# Função para analisar os argumentos da linha de comando
def parse_arguments():
    parser = argparse.ArgumentParser(description="Cliente UDP para enviar comandos.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Endereço do servidor")
    parser.add_argument("--port", type=int, default=5000, help="Porta do servidor")
    parser.add_argument("--requests", type=int, default=10, help="Número de requisições")
    parser.add_argument("--verbose", action="store_true", help="Imprimir respostas")
    parser.add_argument("--log", type=str, help="Arquivo de log para resultados")
    parser.add_argument("--command", type=str,nargs="+", default="INFO", help="Comando a ser enviado")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    times = execute_requests(args.host, args.port, args.requests, args.verbose, args.command)
    stats = log_performance(times, args.log)
    print(json.dumps(stats))
