import socket
import argparse


# Função que processa o comando enviado pelo cliente
def process_request(data):
    # Se o comando recebido for "PING", responde com "PONG"
    if data.strip().upper() == "GET":
        return "SIMULACAO SNMP"

    # Comando simulado "GETNEXT" para retornar informações do sistema
    elif data.strip().upper() == "GETNEXT":
        # Dados fictícios para simular informações do sistema
        system_info = {
            "CPU": "Intel Core i7-9700K",
            "Memory": "16GB DDR4",
            "Disk": "512GB SSD",
            "OS": "Ubuntu 20.04",
            "Network": "Ethernet 1000 Mbps",
        }

        # Converte o dicionário em uma string formatada para enviar ao cliente
        response = "\n".join([f"{key}: {value}" for key, value in system_info.items()])
        return response

    # Caso contrário, apenas retorna uma mensagem com o conteúdo recebido
    return f"Received: {data}"


# Função principal para iniciar o servidor UDP
def start_udp_server(host, port):
    # Cria um socket UDP (AF_INET para IPv4 e SOCK_DGRAM para UDP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Associa o socket ao endereço e porta especificados
    server_socket.bind((host, port))
    print(f"UDP Server is listening on {host}:{port}")

    try:
        # Loop principal para processar dados recebidos de clientes
        while True:
            # Recebe dados do cliente junto com o endereço
            data, addr = server_socket.recvfrom(1024)  # Recebe até 1024 bytes
            # print(f"Received message from {addr}")

            # Processa a solicitação e gera uma resposta
            response = process_request(data.decode())

            # Envia a resposta de volta ao cliente
            server_socket.sendto(response.encode(), addr)
    except KeyboardInterrupt:
        # Captura o sinal de interrupção do teclado (Ctrl+C) para finalizar o servidor
        print("Shutting down server.")
    finally:
        # Fecha o socket do servidor ao encerrar
        server_socket.close()


# Função para configurar e analisar argumentos da linha de comando
def parse_arguments():
    # Cria um objeto ArgumentParser para lidar com argumentos
    parser = argparse.ArgumentParser(
        description="Servidor UDP para processar comandos."
    )

    # Define o argumento '--host' para especificar o endereço do servidor
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Endereço do servidor"
    )

    # Define o argumento '--port' para especificar a porta do servidor
    parser.add_argument("--port", type=int, default=8080, help="Porta do servidor")

    # Retorna os argumentos analisados
    return parser.parse_args()


# Código principal do programa
if __name__ == "__main__":
    # Obtém os argumentos da linha de comando
    args = parse_arguments()

    # Inicia o servidor UDP com o endereço e a porta especificados
    start_udp_server(args.host, args.port)
