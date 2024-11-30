import os


# Variável para definir quantas vezes cada teste será executado
NUM_REPETICAO = 3


# Comandos a serem executados
commands = [
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10.5.0.2:8080, salvando logs em performance.log e resultados em resultados_linux.csv. Mantendo o ambiente Docker ativo após execução.",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 10.5.0.2 --port 8080 --requests 10000 --command INFO --log performance.log --keep 1 --output_file resultados_linux.csv",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10.5.0.2:8080 com modo detalhado (verbose), salvando logs em performance.log e resultados em resultados_linux.csv. Mantendo o ambiente Docker ativo após execução.",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 10.5.0.2 --port 8080 --requests 10000 --command INFO --log performance.log --verbose true --keep 1 --output_file resultados_linux.csv",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10.5.0.2:8080, salvando logs em performance.log e resultados em resultados_linux.csv. Não mantendo o ambiente ativo após execução.",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 10.5.0.2 --port 8080 --requests 10000 --command INFO --log performance.log --keep 0 --output_file resultados_linux.csv",
    },
    {
        "description": "Executando cliente TCP via Docker Compose para enviar 10000 requisições INFO ao servidor 10.5.0.2:8080 com modo detalhado (verbose), salvando logs em performance.log e resultados em resultados_linux.csv. Não mantendo o ambiente ativo após execução.",
        "command": "python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 10.5.0.2 --port 8080 --requests 10000 --command INFO --log performance.log --verbose true --keep 0 --output_file resultados_linux.csv",
    },
    {
        "description": "Executando cliente TCP local diretamente (sem Docker) para enviar 10000 requisições INFO ao servidor local (127.0.0.1:8080), salvando logs em performance.log e resultados em resultados_linux.csv. Não mantendo o ambiente ativo após execução.",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host 127.0.0.1 --port 8080 --requests 10000 --command INFO --log performance.log --keep 0 --output_file resultados_linux.csv",
    },
    {
        "description": "Executando cliente TCP local diretamente (sem Docker) para enviar 10000 requisições INFO ao servidor local (127.0.0.1:8080) com modo detalhado (verbose), salvando logs em performance.log e resultados em resultados_linux.csv. Não mantendo o ambiente ativo após execução.",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host 127.0.0.1 --port 8080 --requests 10000 --command INFO --log performance.log --verbose true --keep 1 --output_file resultados_linux.csv",
    },
    {
        "description": "Executando cliente TCP local diretamente (sem Docker) para enviar 10000 requisições INFO ao servidor local (127.0.0.1:8080), salvando logs em performance.log e resultados em resultados_linux.csv. Não mantendo o ambiente ativo após execução.",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host 127.0.0.1 --port 8080 --requests 10000 --command INFO --log performance.log --keep 0 --output_file resultados_linux.csv",
    },
    {
        "description": "Executando cliente TCP local diretamente (sem Docker) para enviar 10000 requisições INFO ao servidor local (127.0.0.1:8080) com modo detalhado (verbose), salvando logs em performance.log e resultados em resultados_linux.csv. Não mantendo o ambiente ativo após execução.",
        "command": "python3 main_script.py --script tcp-client/tcp-client.py --host 127.0.0.1 --port 8080 --requests 10000 --command INFO --log performance.log --verbose true --keep 1 --output_file resultados_linux.csv",
    },
]


def start_server():
    print("Iniciando servidor...")
    os.system("docker compose -f compose-server.yml up -d")
    # os.system("python3 tcp-server/tcp-server.py")
    print("Servidor iniciado com sucesso.")


# Função para executar os comandos
def execute_commands():
    for i in range(NUM_REPETICAO):
        print(f"Execução {i+1} de {NUM_REPETICAO}:\n")
        for cmd in commands:
            print(cmd["description"])
            os.system(cmd["command"])
            print("\n")


# Execução principal
if __name__ == "__main__":
    start_server()
    execute_commands()
    print("Todos os comandos foram executados com sucesso.")
