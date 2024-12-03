import os
import subprocess

# Variável para definir quantas vezes cada teste será executado
NUM_REPETICAO = 1


# Comandos a serem executados
commands_docker = [
    #! Teste limpo
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose False --keep 0 --write_to_file 0",
    },
    #! Teste com seção
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose False --keep 1 --write_to_file 0",
    },
    #! Write to file
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose False --keep 0 --write_to_file 1",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose False --keep 0 --write_to_file 0",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose False --keep 1 --write_to_file 1",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose False --keep 1 --write_to_file 0",
    },
    #! Verbose
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose False --keep 0 --write_to_file 0",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 00000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose True --keep 0 --write_to_file 0",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose False --keep 1 --write_to_file 0",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host  10.5.0.2 --port 8080 --requests 15 --command INFO --verbose True  --keep 1 --write_to_file 0",
    },
]
commands_local = [
    #! Teste limpo
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host  127.0.0.1 --port 8080 --requests 15 --command INFO --verbose False  --keep 0 --write_to_file 0",
    },
    #! Teste com seção
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host  127.0.0.1 --port 8080 --requests 15 --command INFO --verbose False  --keep 1 --write_to_file 0",
    },
    #! Write to file
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host  127.0.0.1 --port 8080 --requests 15 --command INFO --verbose False  --keep 0 --write_to_file 1",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host 127.0.0.1 --port 8080 --requests 15 --command INFO --verbose False  --keep 0 --write_to_file 0",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host  127.0.0.1 --port 8080 --requests 15 --command INFO --verbose False  --keep 1 --write_to_file 1",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host  127.0.0.1 --port 8080 --requests 15 --command INFO --verbose False  --keep 1 --write_to_file 0",
    },
    #! Verbose
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host  127.0.0.1 --port 8080 --requests 15 --command INFO --verbose False  --keep 0 --write_to_file 0",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 00000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host  127.0.0.1 --port 8080 --requests 15 --command INFO --verbose True  --keep 0 --write_to_file 0",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host  127.0.0.1 --port 8080 --requests 15 --command INFO --verbose False  --keep 1 --write_to_file 0",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10000 10.5.0.2:8080",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host  127.0.0.1 --port 8080 --requests 15 --command INFO --verbose True   --keep 1 --write_to_file 0",
    },
]
# Comandos UDP via Docker
commands_docker_udp = [
    #! Teste limpo
    {
        "description": "Executando cliente UDP via Docker Compose para enviar 15 requisições INFO ao servidor Docker 10.5.0.4:8081 sem prints e sem escrita em arquivo.",
        "command": "python3 main_script.py --compose_file compose-udp.yml --service udp-client --script udp-client.py --host 10.5.0.4 --port 8081 --requests 15 --command INFO --verbose False --keep 0 --write_to_file 0",
    },
    #! Write to file
    {
        "description": "Executando cliente UDP via Docker Compose para enviar 15 requisições INFO ao servidor Docker 10.5.0.4:8081 com escrita em arquivo.",
        "command": "python3 main_script.py --compose_file compose-udp.yml --service udp-client --script udp-client.py --host 10.5.0.4 --port 8081 --requests 15 --command INFO --verbose False --keep 0 --write_to_file 1",
    },
    #! Verbose
    {
        "description": "Executando cliente UDP via Docker Compose para enviar 15 requisições INFO ao servidor Docker 10.5.0.4:8081 com prints no terminal (verbose).",
        "command": "python3 main_script.py --compose_file compose-udp.yml --service udp-client --script udp-client.py --host 10.5.0.4 --port 8081 --requests 15 --command INFO --verbose True --keep 0 --write_to_file 0",
    },
]

# Comandos UDP local
commands_local_udp = [
    #! Teste limpo
    {
        "description": "Executando cliente UDP local diretamente (sem Docker) para enviar 15 requisições INFO ao servidor local 127.0.0.1:8081 sem prints e sem escrita em arquivo.",
        "command": "python3 main_script.py --script udp-client/udp-client.py --host 127.0.0.1 --port 8081 --requests 15 --command INFO --verbose False --keep 0 --write_to_file 0",
    },
    #! Write to file
    {
        "description": "Executando cliente UDP local diretamente (sem Docker) para enviar 15 requisições INFO ao servidor local 127.0.0.1:8081 com escrita em arquivo.",
        "command": "python3 main_script.py --script udp-client/udp-client.py --host 127.0.0.1 --port 8081 --requests 15 --command INFO --verbose False --keep 0 --write_to_file 1",
    },
    #! Verbose
    {
        "description": "Executando cliente UDP local diretamente (sem Docker) para enviar 15 requisições INFO ao servidor local 127.0.0.1:8081 com prints no terminal (verbose).",
        "command": "python3 main_script.py --script udp-client/udp-client.py --host 127.0.0.1 --port 8081 --requests 15 --command INFO --verbose True --keep 0 --write_to_file 0",
    },
]


def start_server():
    print("Iniciando servidor...")
    os.system("docker compose -f compose-server.yml up -d --remove-orphans")
    # os.system("python3 tcp-server/tcp-server.py")
    print("Servidor iniciado com sucesso.")


def start_docker_server():
    command = ["docker", "compose", "-f", "compose-server.yml", "run", "tcp-server"]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Servidor iniciado em segundo plano.")


# Função para executar os comandos
def execute_commands_docker_tcp():
    for i in range(NUM_REPETICAO):
        print(f"Execução {i+1} de {NUM_REPETICAO}:\n")
        for cmd in commands_docker:
            start_server()
            print(cmd["description"])
            os.system(cmd["command"])
            print("\n")


def execute_commands_docker_udp():
    for i in range(NUM_REPETICAO):
        print(f"Execução {i+1} de {NUM_REPETICAO}:\n")
        for cmd in commands_docker_udp:
            start_server()
            print(cmd["description"])
            os.system(cmd["command"])
            print("\n")


# Função para executar os comandos
def execute_commands_local_tcp():
    for i in range(NUM_REPETICAO):
        print(f"Execução {i+1} de {NUM_REPETICAO}:\n")
        for cmd in commands_local:
            print(cmd["description"])
            os.system(cmd["command"])
            print("\n")


# Função para executar os comandos
def execute_commands_local_udp():
    for i in range(NUM_REPETICAO):
        print(f"Execução {i+1} de {NUM_REPETICAO}:\n")
        for cmd in commands_local_udp:
            print(cmd["description"])
            os.system(cmd["command"])
            print("\n")


# Execução principal
if __name__ == "__main__":
    # start_server()
    execute_commands_docker_tcp()
    execute_commands_local_tcp()
    execute_commands_docker_udp()
    execute_commands_local_udp()
    print("Todos os comandos foram executados com sucesso.")
