import socket
import time
import argparse
import json
import statistics
import os

ARQUIVO_ESCRITA = "output.txt"


# Função para enviar uma requisição e receber a resposta
def send_request(sock, server_address, request):
    sock.sendto(request.encode(), server_address)
    response, _ = sock.recvfrom(1024)
    return response.decode()


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
def execute_requests(host, port, num_requests, print_to_screen, command, write_to_file):
    times = []
    server_address = (host, port)
    command = " ".join(command)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for _ in range(num_requests):
        start_time = time.time()  # Marca o tempo de início
        response = send_request(sock, server_address, command)  # Envia a requisição

        if print_to_screen == True:
            print(f"resposta: {response}")
        if write_to_file == 1:
            print_to_file(response)

        times.append(time.time() - start_time)

    sock.close()
    return times


# Função para calcular estatísticas de desempenho
def log_performance(times):
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
    parser.add_argument(
        "--print_to_screen",
        action="store_true",  # Trata como flag booleana
        default=False,
        help="Habilita ou desabilita o modo print_to_screen",
    )
    parser.add_argument(
        "--command", type=str, nargs="+", default="INFO", help="Comando a ser enviado"
    )
    # Para escrever ou nao os prints em um arquivo
    parser.add_argument("--write_to_file", default=0, type=int)
    # recebe session mas nao faz nada

    parser.add_argument("--session", default=0, type=int)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    times = execute_requests(
        args.host,
        args.port,
        args.requests,
        args.print_to_screen,
        args.command,
        args.write_to_file,
    )
    stats = log_performance(times)
    print(json.dumps(stats))
