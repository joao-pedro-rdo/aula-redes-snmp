import socket
import time
import argparse
import json
import statistics
import os

ARQUIVO_ESCRITA = "output.txt"


# Função para enviar uma requisição e receber a resposta
def send_request(sock, request):
    # request = " ".join(request)
    # print(f"Enviando comando: {request}")
    sock.send(request.encode())  # Envia a requisição codificada
    response = sock.recv(1024).decode()  # Recebe a resposta e decodifica
    return response


# Função para criar uma conexão com o servidor
def create_connection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
    try:
        sock.connect((host, port))  # Conecta ao servidor
    except ConnectionRefusedError:
        print(f"Connection to {host}:{port} refused. Ensure the server is running.")
        return None
    return sock


# Função para fechar a conexão
def close_connection(sock):
    if sock:
        sock.close()  # Fecha o socket se ele existir


def print_to_file(response):
    with open(ARQUIVO_ESCRITA, "a") as file:
        file.write(response)


def del_file():
    if os.path.exists(ARQUIVO_ESCRITA):  # Verifica se o arquivo existe
        os.remove(ARQUIVO_ESCRITA)  # Remove o arquivo
        print(f"Arquivo {ARQUIVO_ESCRITA} excluído com sucesso.")
    else:
        print(f"Arquivo {ARQUIVO_ESCRITA} não encontrado.")


# Função para executar múltiplas requisições ao servidor
def execute_requests(host, port, num_requests, verbose, command, keep, write_to_file):

    times = []  # Lista para armazenar os tempos de resposta
    command = " ".join(command)
    if keep == 0:
        sock = create_connection(host, port)
        for _ in range(num_requests):
            start_time = time.time()  # Marca o tempo de início
            if sock:
                response = send_request(sock, command)  # Envia o comando especificado
                if verbose == True:
                    print(f"resposta: {response}")
                if write_to_file == 1:
                    print_to_file(response)
                # Calcula e armazena o tempo de resposta
                times.append(time.time() - start_time)
        close_connection(sock)  # Fecha a conexão se a sessão for persistente
        del_file()
        return times  # Retorna a lista de tempos de resposta
    elif keep == 1:
        for _ in range(num_requests):
            start_time = time.time()
            sock = create_connection(host, port)
            if sock:
                response = send_request(sock, command)  # Envia o comando especificado
                if verbose == True:
                    print(f"resposta: {response}")
                if write_to_file == 1:
                    print_to_file(response)
                # Calcula e armazena o tempo de resposta
                times.append(time.time() - start_time)
                close_connection(sock)  # Fecha a conexão se a sessão for persistente
        del_file()
        return times  # Retorna a lista de tempos de resposta


# Função para medir o tempo total de execução com estatísticas detalhadas
def log_performance(times):
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

    # Cria um dicionário de estatísticas
    stats = {
        "tempo_de_execucao_total_ms": round(execution_time, 3),
        "tempo_medio_ms": round(avg_time, 3),
        "tempo_minimo_ms": round(min_time, 3),
        "tempo_maximo_ms": round(max_time, 3),
        "desvio_padrao_ms": round(std_dev, 3),
    }
    return stats


# Função para analisar os argumentos da linha de comando
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="TCP Client to send commands."
    )  # Cliente TCP
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Endereço do servidor"
    )
    parser.add_argument("--port", type=int, default=8080, help="Porta do servidor")
    parser.add_argument(
        "--requests", type=int, default=10, help="Número de requisições"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",  # Trata como flag booleana
        default=False,
        help="Habilita ou desabilita o modo verbose",
    )

    parser.add_argument(
        "--command",
        type=str,
        nargs="+",
        default="GET",
        help="Comando a ser enviado ao servidor",
    )
    # Para manter ou nao a seção da conexão
    parser.add_argument("--keep", default=0, type=int)

    # Para escrever ou nao os prints em um arquivo
    parser.add_argument("--write_to_file", default=0, type=int)

    return parser.parse_args()  # Retorna os argumentos analisados


# Ponto de entrada do script
if __name__ == "__main__":
    args = parse_arguments()  # Analisa os argumentos da linha de comando
    times = execute_requests(
        args.host,
        args.port,
        args.requests,
        args.verbose,
        args.command,
        args.keep,
        args.write_to_file,
    )  # Executa as requisições
    stats = log_performance(times)  # Registra o tempo total de execução
    print(json.dumps(stats))  # Imprime as estatísticas como dicionário
