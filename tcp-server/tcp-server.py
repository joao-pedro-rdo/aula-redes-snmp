import socket
import argparse


# Função que trata a conexão de cada cliente
def handle_client_connection(client_socket, addr):
    print(f"Connection from {addr}")  # Exibe o endereço do cliente conectado
    try:
        while True:
            # Recebe os dados enviados pelo cliente
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Processa a solicitação e gera uma resposta
            response = process_request(data)

            # Envia a resposta de volta ao cliente
            client_socket.sendall(response.encode())
    finally:
        # Fecha a conexão com o cliente após o envio da resposta
        client_socket.close()


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


# Função principal para iniciar o servidor TCP
def start_tcp_server(host, port):
    # Cria um socket TCP (AF_INET para IPv4 e SOCK_STREAM para TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket ao endereço e porta especificados
    server_socket.bind((host, port))

    # Coloca o servidor em modo de escuta, pronto para aceitar conexões
    server_socket.listen(5)
    print(f"TCP Server is listening on {host}:{port}")

    try:
        # Loop principal para aceitar conexões de clientes
        while True:
            # Aceita uma nova conexão de cliente
            client_socket, addr = server_socket.accept()

            # Chama a função para tratar a conexão do cliente
            handle_client_connection(client_socket, addr)
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
        description="Servidor TCP para processar comandos."
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

    # Inicia o servidor TCP com o endereço e a porta especificados
    start_tcp_server(args.host, args.port)
