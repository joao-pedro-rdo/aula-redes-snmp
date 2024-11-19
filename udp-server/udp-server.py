import socket
import argparse

# Dados simulados do sistema
system_info = {
    0: "Name: Computador Simulado",
    1: "CPU: Intel Core i7-9700K",
    2: "Memory: 16GB DDR4",
    3: "Disk: 512GB SSD",
    4: "OS: Ubuntu 20.04",
    5: "Network: Ethernet 1000 Mbps",
}

# Função que processa o comando enviado pelo cliente
def process_request(data):
    # Inicializa a resposta padrão
    response = "Comando não reconhecido"

    # Divide a entrada em partes
    parts = data.strip().split()
    if not parts:
        return "Erro: Nenhum comando enviado"

    # O primeiro elemento é o comando principal
    command = parts[0].upper()

    if command == "INFO":
        return "Computador Simulado"

    elif command == "SNMPGET":
        response = process_snmpget(parts)

    elif command == "SNMPSET":
        response = process_snmpset(parts)

    elif command == "SNMPWALK":
        response = "\n".join([f"{key}: {value}" for key, value in system_info.items()])

    return response


def process_snmpget(parts):
    if len(parts) != 2:
        return "Erro: Comando SNMPGET inválido. Use: SNMPGET <indice>"

    try:
        snmp_identifier = int(parts[1])
        return system_info.get(snmp_identifier, "Erro: Índice não encontrado")
    except ValueError:
        return "Erro: Índice inválido. Deve ser um número inteiro."


def process_snmpset(parts):
    if len(parts) != 3:
        return "Erro: Comando SNMPSET inválido. Use: SNMPSET <indice> <novo_valor>"

    try:
        snmp_identifier = int(parts[1])
        snmp_value = parts[2]
        system_info[snmp_identifier] = snmp_value
        return "Valor alterado com sucesso"
    except ValueError:
        return "Erro: Índice inválido. Deve ser um número inteiro."


# Função principal para iniciar o servidor UDP
def start_udp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"UDP Server is listening on {host}:{port}")

    try:
        while True:
            data, addr = server_socket.recvfrom(1024)
            response = process_request(data.decode())
            server_socket.sendto(response.encode(), addr)
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_socket.close()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Servidor UDP para processar comandos.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Endereço do servidor")
    parser.add_argument("--port", type=int, default=8080, help="Porta do servidor")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    start_udp_server(args.host, args.port)
