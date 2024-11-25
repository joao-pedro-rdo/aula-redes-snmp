import subprocess
import json
import os
from parse_argument import get_argments
from save_csv import save_csv
from generate_graphics import genrate_praphics

# * É necessario levantar o seridor docker antes de executar o script
# *  docker compose -f compose-server.yml run tcp-server

#! python main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 127.0.0.1 --port 8080 --requests 1000 --command SNMPWALK --log performance.log --keep 1 --output_file resultados.csv
#! python3 main_script.py  --script tcp-client/tcp-client.py --host localhost --port 8080 --requests 1000 --command SNMPWALK --log performance.log --keep 0 --output_file resultados.csv


def execute_docker_compose(
    compose_file,
    service,
    script,
    host,
    port,
    requests,
    command,
    session,
    log,
    keep,
    output_file,
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
        "--session" if session else "",
        "--log",
        log,
        "--keep",
        str(keep),
        # "--remove-orphans",
    ]

    # Remove argumentos vazios (caso `--session` seja opcional)
    docker_command = [arg for arg in docker_command if arg]

    try:
        # Executa o comando
        resultado = subprocess.run(docker_command, text=True, capture_output=True)

        # Estrutura os resultados em um dicionário
        new_output = {
            "indentifier": " ".join(["docker", str(requests), command, str(keep)]),
            "stdout": resultado.stdout.strip(),
            "stderr": resultado.stderr.strip(),
            "returncode": resultado.returncode,
        }

        save_csv(output_file, new_output)

    except Exception as e:
        print(f"Erro ao execute o comando: {e}")

    compose_down(args.compose_file)


def execute_local(
    script,
    host,
    port,
    requests,
    command,
    session,
    log,
    keep,
    output_file,
):
    """
    Executa o script diretamente no ambiente local, sem Docker.
    """
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
        "--session" if session else "",
        "--log",
        log,
        "--keep",
        str(keep),
    ]

    # Remove argumentos vazios (caso `--session` seja opcional)
    local_command = [arg for arg in local_command if arg]

    try:
        # Executa o comando localmente
        resultado = subprocess.run(local_command, text=True, capture_output=True)

        # Estrutura os resultados em um dicionário
        new_output = {
            "indentifier": " ".join(["local", str(requests), command, str(keep)]),
            "stdout": resultado.stdout.strip(),
            "stderr": resultado.stderr.strip(),
            "returncode": resultado.returncode,
        }

        save_csv(output_file, new_output)

    except Exception as e:
        print(f"Erro ao executar o comando local: {e}")


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
            session=args.session,
            log=args.log,
            keep=args.keep,
            output_file=args.output_file,
        )
        compose_down(args.compose_file)
    else:  # Caso contrário, executa localmente
        execute_local(
            script=args.script,
            host=args.host,
            port=args.port,
            requests=args.requests,
            command=args.command,
            session=args.session,
            log=args.log,
            keep=args.keep,
            output_file=args.output_file,
        )
    #! FALTA O VERBOSE

    genrate_praphics(args.output_file)  # TODO: Os graficos precisam ser melhorados
