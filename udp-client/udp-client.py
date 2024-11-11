import socket
import time
import argparse
import statistics


# Função para enviar uma requisição e receber a resposta
def send_request(sock, server_address, request):
    sock.sendto(
        request.encode(), server_address
    )  # Envia a requisição para o endereço do servidor
    response, _ = sock.recvfrom(1024)  # Recebe a resposta do servidor
    return response.decode()


# Função para executar múltiplas requisições ao servidor
def execute_requests(host, port, num_requests, verbose, command):
    times = []  # Lista para armazenar os tempos de resposta
    server_address = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP

    for _ in range(num_requests):
        start_time = time.time()  # Marca o tempo de início
        response = send_request(
            sock, server_address, command
        )  # Envia o comando especificado
        elapsed_time = time.time() - start_time  # Calcula o tempo de resposta
        times.append(elapsed_time)  # Armazena o tempo de resposta

        # if verbose:
        #     print(
        #         f"Response: {response}"
        #     )  # Imprime a resposta se o modo verbose estiver ativado

    sock.close()  # Fecha o socket após todas as requisições
    return times  # Retorna a lista de tempos de resposta


# Função para medir o tempo total de execução com estatísticas detalhadas
def log_performance(times, log_file=None):
    if not times:
        print("No times recorded.")
        return {}

    # Calcula as estatísticas dos tempos
    execution_time = sum(times)
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0

    # Cria um dicionário de estatísticas
    stats = {
        "total_execution_time": f"{execution_time:.2f} seconds",
        "average_time": f"{avg_time:.2f} seconds",
        "minimum_time": f"{min_time:.2f} seconds",
        "maximum_time": f"{max_time:.2f} seconds",
        "standard_deviation": f"{std_dev:.2f} seconds",
    }

    # Imprime as estatísticas formatadas como dicionário
    print(stats)

    # Salva as estatísticas em um arquivo, se especificado
    if log_file:
        with open(log_file, "w") as file:
            file.write(str(stats))

    return stats


# Função para analisar os argumentos da linha de comando
def parse_arguments():
    parser = argparse.ArgumentParser(description="Cliente UDP para enviar comandos.")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Endereço do servidor"
    )
    parser.add_argument("--port", type=int, default=5000, help="Porta do servidor")
    parser.add_argument(
        "--requests", type=int, default=10, help="Número de requisições"
    )
    parser.add_argument("--verbose", action="store_true", help="Imprimir respostas")
    parser.add_argument(
        "--log", type=str, help="Arquivo de log para resultados de performance"
    )
    parser.add_argument(
        "--command", type=str, default="GET", help="Comando a ser enviado ao servidor"
    )  # Novo parâmetro
    return parser.parse_args()  # Retorna os argumentos analisados


# Ponto de entrada do script
if __name__ == "__main__":
    args = parse_arguments()  # Analisa os argumentos da linha de comando
    times = execute_requests(
        args.host, args.port, args.requests, args.verbose, args.command
    )  # Executa as requisições
    stats = log_performance(times, args.log)  # Registra o tempo total de execução
    print(stats)  # Imprime as estatísticas como dicionário
