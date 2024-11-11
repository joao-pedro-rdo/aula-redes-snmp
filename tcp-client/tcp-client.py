import socket
import time
import argparse
import statistics


# Função para enviar uma requisição e receber a resposta
def envia_requisicao(sock, requisicao):
    sock.send(requisicao.encode())  # Envia a requisição codificada
    resposta = sock.recv(1024).decode()  # Recebe a resposta e decodifica
    return resposta


# Função para criar uma conexão com o servidor
def cria_conexao(host, porta, session):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
    try:
        sock.connect((host, porta))  # Conecta ao servidor
    except ConnectionRefusedError:
        print(f"Connection to {host}:{porta} refused. Ensure the server is running.")
        return None
    return (
        sock if session else None
    )  # Retorna o socket se a sessão for persistente, caso contrário, retorna None


# Função para fechar a conexão
def fecha_conexao(sock):
    if sock:
        sock.close()  # Fecha o socket se ele existir


# Função para executar múltiplas requisições ao servidor
def executa_requisicao(host, porta, num_requisicao, session, verbose, comando):
    times = []  # Lista para armazenar os tempos de resposta
    sock = cria_conexao(host, porta, session) if session else None

    for _ in range(num_requisicao):
        start_time = time.time()  # Marca o tempo de início

        if sock:
            resposta = envia_requisicao(sock, comando)  # Envia o comando especificado
            if verbose:
                print(
                    f"resposta: {resposta}"
                )  # Imprime a resposta se o modo verbose estiver ativado

            times.append(
                time.time() - start_time
            )  # Calcula e armazena o tempo de resposta
            if not session:
                fecha_conexao(sock)  # Fecha a conexão se a sessão não for persistente

    if session:
        fecha_conexao(sock)  # Fecha a conexão se a sessão for persistente

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
    parser.add_argument("--porta", type=int, default=5000, help="Porta do servidor")
    parser.add_argument(
        "--requisicao", type=int, default=10, help="Número de requisições"
    )
    parser.add_argument(
        "--session", action="store_true", help="Usar sessão persistente"
    )
    parser.add_argument("--verbose", action="store_true", help="Imprimir respostas")
    parser.add_argument(
        "--log", type=str, help="Arquivo de log para resultados de performance"
    )
    parser.add_argument(
        "--comando", type=str, default="GET", help="Comando a ser enviado ao servidor"
    )  # Novo parâmetro
    return parser.parse_args()  # Retorna os argumentos analisados


# Ponto de entrada do script
if __name__ == "__main__":
    args = parse_arguments()  # Analisa os argumentos da linha de comando
    times = executa_requisicao(
        args.host, args.porta, args.requests, args.session, args.verbose, args.comando
    )  # Executa as requisições
    stats = log_performance(times, args.log)  # Registra o tempo total de execução
    print(stats)  # Imprime as estatísticas como dicionário
