import socket
import argparse

system_info = {
    0: "Name: Computador Simuladnmo",
    1: "CPU: Intel Core i7-9700K",
    2: "Memory: 16GB DDR4",
    3: "Disk: 512GB SSD",
    4: "OS: Ubuntu 20.04",
    5: "Network: Ethernet 1000 Mbps",
}


# Função que trata a conexão de cada cliente
def handle_client_connection(client_socket, addr):
    # print(f"Connection from {addr}")  # Exibe o endereço do cliente conectado
    try:
        while True:
            # Recebe os dados enviados pelo cliente e trasforma de bytes para strings
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
    # Inicializa response com uma mensagem padrão
    response = "Comando não reconhecido"

    # Divide a entrada em partes
    parts = data.strip().split()
    if not parts:
        return "Erro: Nenhum comando enviado"

    # O primeiro elemento é o comando principal
    command = parts[0].upper()  # Comando em maiúsculas

    if command == "INFO":
        return "Computador Simulado"

    elif command == "SNMPGET":
        # Retorna o valor de um OID em system_info
        response = process_snmpget(parts)

    elif command == "SNMPSET":
        # Altera o valor de um OID em system_info
        response = process_snmpset(parts)

    elif command == "SNMPWALK":
        # Converte o dicionário em uma string formatada para enviar ao cliente
        response = "\n".join([f"{key}: {value}" for key, value in system_info.items()])

    return response


def process_snmpget(parts):
    # Verifica se o comando contém o argumento necessário
    if len(parts) != 2:
        return "Erro: Comando SNMPGET inválido. Use: SNMPGET <indice>"

    try:
        snmp_identifier = int(parts[1])  # Converte o índice para inteiro
        return system_info.get(snmp_identifier, "Erro: Índice não encontrado")
    except ValueError:
        return "Erro: Índice inválido. Deve ser um número inteiro."


def process_snmpset(parts):
    # Verifica se o comando contém os argumentos necessários
    if len(parts) != 3:
        return "Erro: Comando SNMPSET inválido. Use: SNMPSET <indice> <novo_valor>"

    try:
        snmp_identifier = int(parts[1])  # Índice
        snmp_value = parts[2]  # Novo valor
        system_info[snmp_identifier] = snmp_value  # Atualiza o valor no dicionário
        return "Valor alterado com sucesso"
    except ValueError:
        return "Erro: Índice inválido. Deve ser um número inteiro."


# Função principal para iniciar o servidor TCP
def start_tcp_server(host, port):
    # Cria um socket TCP (AF_INET para IPv4 e SOCK_STREAM para TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket ao endereço e porta especificados
    server_socket.bind((host, port))

    # Coloca o servidor em modo de escuta, pronto para aceitar conexões
    server_socket.listen(1024)
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
