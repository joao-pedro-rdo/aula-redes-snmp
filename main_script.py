import subprocess
import json
import os
from parse_argument import get_argments
from save_csv import save_csv


# Função para executar scripts usando Docker Compose
def execute_docker_compose(
    compose_file,
    service,
    script,
    host,
    port,
    requests,
    command,
    verbose,
    keep,
    write_to_file,
):
    # Monta o comando dinamicamente
    docker_command = [
        "docker",
        "compose",
        "-f",
        compose_file,
        "run",
        service,
        "python",
        script,
        "--host",
        host,
        "--port",
        str(port),
        "--requests",
        str(requests),
        "--command",
        command,
        "--verbose" if verbose else "",
        "--keep" if script != "udp-client.py" else "",
        str(keep) if script != "udp-client.py" else "",
        "--write_to_file",
        str(write_to_file),
    ]

    # Remove argumentos vazios
    docker_command = [arg for arg in docker_command if arg]

    try:
        # Executa o comando
        resultado = subprocess.run(docker_command, text=True, capture_output=True)

        # Estrutura os resultados em um dicionário
        new_output = {
            "execution_location": "docker",
            "requests": requests,
            "command": command,
            "keep": keep,
            "verbose": verbose,  # Adicione o flag verbose
            "write_to_file": write_to_file,
            "stdout": resultado.stdout.strip(),
            "stderr": resultado.stderr.strip(),
            "returncode": resultado.returncode,
        }

        save_csv(new_output)
        print(new_output)
        compose_down(compose_file)

    except Exception as e:
        print(f"Erro ao executar o comando Docker: {e}")
    ...


# Função para executar scripts localmente
def execute_local(
    script,
    host,
    port,
    requests,
    command,
    verbose,
    keep,
    write_to_file,
):
    # Monta o comando dinamicamente
    local_command = [
        "python3",
        script,
        "--host",
        host,
        "--port",
        str(port),
        "--requests",
        str(requests),
        "--command",
        command,
        "--verbose" if verbose else "",
        "--keep" if script != "udp-client.py" else "",
        str(keep) if script != "udp-client.py" else "",
        "--write_to_file",
        str(write_to_file),
    ]

    # Remove argumentos vazios
    local_command = [arg for arg in local_command if arg]

    try:
        # Executa o comando localmente
        resultado = subprocess.run(local_command, text=True, capture_output=True)

        # Estrutura os resultados em um dicionário
        new_output = {
            "execution_location": "local",
            "requests": requests,
            "command": command,
            "keep": keep,
            "verbose": verbose,  # Adicione o flag verbose
            "write_to_file": write_to_file,
            "write_to_file": write_to_file,
            "stdout": resultado.stdout.strip(),
            "stderr": resultado.stderr.strip(),
            "returncode": resultado.returncode,
        }

        save_csv(new_output)
        print(new_output)

    except Exception as e:
        print(f"Erro ao executar o comando local: {e}")


# Função para desmontar serviços Docker Compose
def compose_down(compose_file):
    subprocess.run(
        ["docker", "compose", "-f", compose_file, "down", "--remove-orphans"],
        text=True,
        capture_output=True,
    )


if __name__ == "__main__":
    # Faz o parse dos argumentos
    args = get_argments()

    # Escolha entre execução com Docker ou local
    if args.service:  # Se o serviço foi especificado, assume execução com Docker
        execute_docker_compose(
            compose_file=args.compose_file,
            service=args.service,
            script=args.script,
            host=args.host,
            port=args.port,
            requests=args.requests,
            command=args.command,
            verbose=args.verbose,
            keep=args.keep,
            write_to_file=args.write_to_file,
        )
    else:  # Caso contrário, executa localmente
        execute_local(
            script=args.script,
            host=args.host,
            port=args.port,
            requests=args.requests,
            command=args.command,
            verbose=args.verbose,
            keep=args.keep,
            write_to_file=args.write_to_file,
        )
