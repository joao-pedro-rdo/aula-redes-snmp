import subprocess
import json
import os
from parse_argument import get_argments
from save_csv import save_csv


# Função para identificar o protocolo com base no nome do script
def infer_protocol(script_name):
    if "tcp" in script_name.lower():
        return "TCP"
    elif "udp" in script_name.lower():
        return "UDP"
    else:
        return "UNKNOWN"  # Valor padrão caso não seja TCP ou UDP


# Função para executar scripts usando Docker Compose
def execute_docker_compose(
    compose_file,
    service,
    script,
    host,
    port,
    requests,
    command,
    print_to_screen,
    session,
    write_to_file,
):
    # Identifica o protocolo com base no script
    protocol = infer_protocol(script)

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
        "--print_to_screen" if print_to_screen else "",
        "--session" if script != "udp-client.py" else "",
        str(session) if script != "udp-client.py" else "",
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
            "protocol": protocol,  # Adiciona o protocolo
            "requests": requests,
            "command": command,
            "session": session,
            "print_to_screen": print_to_screen,
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


# Função para executar scripts localmente
def execute_local(
    script,
    host,
    port,
    requests,
    command,
    print_to_screen,
    session,
    write_to_file,
):
    # Identifica o protocolo com base no script
    protocol = infer_protocol(script)

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
        "--print_to_screen" if print_to_screen else "",
        "--session" if script != "udp-client.py" else "",
        str(session) if script != "udp-client.py" else "",
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
            "protocol": protocol,  # Adiciona o protocolo
            "requests": requests,
            "command": command,
            "session": session,
            "print_to_screen": print_to_screen,
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
            print_to_screen=args.print_to_screen,
            session=args.session,
            write_to_file=args.write_to_file,
        )
    else:  # Caso contrário, executa localmente
        execute_local(
            script=args.script,
            host=args.host,
            port=args.port,
            requests=args.requests,
            command=args.command,
            print_to_screen=args.print_to_screen,
            session=args.session,
            write_to_file=args.write_to_file,
        )
