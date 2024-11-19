import socket
import time
import argparse
import json
import statistics


# Função para enviar uma requisição e receber a resposta
def send_request(sock, request):
    # request = " ".join(request)
    # print(f"Enviando comando: {request}")
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


# Função para executar múltiplas requisições ao servidor
def execute_requests(host, port, num_requests, session, verbose, command):
    times = []  # Lista para armazenar os tempos de resposta
    sock = create_connection(host, port, session) if session else None
    command = " ".join(command)
    for _ in range(num_requests):
        start_time = time.time()  # Marca o tempo de início

        if sock:
                

            response = send_request(sock, command)  # Envia o comando especificado
            if verbose:
                print(
                    f"resposta: {response}"
                )  # Imprime a resposta se o modo verbose estiver ativado

            times.append(
                time.time() - start_time
            )  # Calcula e armazena o tempo de resposta
            if not session:
                close_connection(
                    sock
                )  # Fecha a conexão se a sessão não for persistente

    if session:
        close_connection(sock)  # Fecha a conexão se a sessão for persistente

    return times  # Retorna a lista de tempos de resposta


# Função para medir o tempo total de execução com estatísticas detalhadas
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
    print("Performance statistics (in milliseconds):")
    for key, value in stats.items():
        print(f"{key}: {value} ms")

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
    parser = argparse.ArgumentParser(
        description="TCP Client to send commands."
    )  # Cliente TCP
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
        "--command",
        type=str,
        nargs="+",
        default="GET",
        help="Comando a ser enviado ao servidor",
    )  # Novo parâmetro
    return parser.parse_args()  # Retorna os argumentos analisados


# Ponto de entrada do script
if __name__ == "__main__":
    args = parse_arguments()  # Analisa os argumentos da linha de comando
    times = execute_requests(
        args.host, args.port, args.requests, args.session, args.verbose, args.command
    )  # Executa as requisições
    stats = log_performance(times, args.log)  # Registra o tempo total de execução
    print(json.dumps(stats)) # Imprime as estatísticas como dicionário
