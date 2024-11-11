import socket
import time
import argparse
import statistics


# Função para enviar uma requisição e receber a resposta
def send_request(sock, request):
    sock.send(request.encode())  # Envia a requisição codificada
    response = sock.recv(1024).decode()  # Recebe a resposta e decodifica
    return response


# Função para criar uma conexão com o servidor
def create_connection(host, port, session):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
    try:
        sock.connect((host, port))  # Conecta ao servidor
    except ConnectionRefusedError:
        print(f"Connection to {host}:{port} refused. Ensure the server is running.")
        return None
    return (
        sock if session else None
    )  # Retorna o socket se a sessão for persistente, caso contrário, retorna None


# Função para fechar a conexão
def close_connection(sock):
    if sock:
        sock.close()  # Fecha o socket se ele existir


# Função para executar múltiplas requisições ao servidor e registrar as saídas em um arquivo
def execute_requests_with_logging(
    host, port, num_requests, session, verbose, command, output_file
):
    times = []  # Lista para armazenar os tempos de resposta
    sock = (
        create_connection(host, port, session) if session else None
    )  # Cria uma conexão se a sessão for persistente

    # Abre o arquivo para gravação das saídas de cada requisição
    with open(output_file, "w") as file:
        for i in range(num_requests):
            start_time = time.time()  # Marca o tempo de início
            if not session:
                sock = create_connection(
                    host, port, session
                )  # Cria uma nova conexão se a sessão não for persistente

            if sock:
                response = send_request(sock, command)  # Envia o comando especificado
                elapsed_time = time.time() - start_time  # Calcula o tempo de resposta
                times.append(elapsed_time)  # Armazena o tempo de resposta

                # Grava a resposta e o tempo de execução no arquivo
                file.write(
                    f"Request {i + 1}: Response: {response}, Time: {elapsed_time:.2f} seconds\n"
                )

                if verbose:
                    print(
                        f"Response: {response}"
                    )  # Imprime a resposta se o modo verbose estiver ativado

                if not session:
                    close_connection(
                        sock
                    )  # Fecha a conexão se a sessão não for persistente

    if session:
        close_connection(sock)  # Fecha a conexão se a sessão for persistente

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
    parser = argparse.ArgumentParser(description="Cliente TCP para enviar comandos.")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Endereço do servidor"
    )
    parser.add_argument("--port", type=int, default=5000, help="Porta do servidor")
    parser.add_argument(
        "--requests", type=int, default=10, help="Número de requisições"
    )
    parser.add_argument(
        "--session", action="store_true", help="Usar sessão persistente"
    )
    parser.add_argument("--verbose", action="store_true", help="Imprimir respostas")
    parser.add_argument(
        "--log", type=str, help="Arquivo de log para resultados de performance"
    )
    parser.add_argument(
        "--command", type=str, default="GET", help="Comando a ser enviado ao servidor"
    )  # Novo parâmetro
    parser.add_argument(
        "--output",
        type=str,
        default="output.txt",
        help="Arquivo para salvar as saídas de cada requisição",
    )  # Novo parâmetro
    return parser.parse_args()  # Retorna os argumentos analisados


# Ponto de entrada do script
if __name__ == "__main__":
    args = parse_arguments()  # Analisa os argumentos da linha de comando
    times = execute_requests_with_logging(
        args.host,
        args.port,
        args.requests,
        args.session,
        args.verbose,
        args.command,
        args.output,
    )  # Executa as requisições e salva saídas
    stats = log_performance(times, args.log)  # Registra o tempo total de execução
    print(stats)  # Imprime as estatísticas como dicionário
