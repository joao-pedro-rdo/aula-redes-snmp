import subprocess
import json
import os


def executar_docker_compose_tcp(
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
    ]

    # Remove argumentos vazios (caso `--session` seja opcional)
    docker_command = [arg for arg in docker_command if arg]

    try:
        # Executa o comando
        resultado = subprocess.run(docker_command, text=True, capture_output=True)

        # Estrutura os resultados em um dicionário
        new_output = {
            "indentifier": " ".join([str(requests), command, str(keep)]),
            "stdout": resultado.stdout.strip(),
            "stderr": resultado.stderr.strip(),
            "returncode": resultado.returncode,
        }

        save_json(output_file, new_output)

    except Exception as e:
        print(f"Erro ao executar o comando: {e}")


def save_json(output_file, new_output):
    # Inicializa uma lista para salvar as saídas
    all_outputs = []

    # Carrega o JSON existente, se existir
    if os.path.exists(output_file):
        with open(output_file, "r") as json_file:
            try:
                data = json.load(json_file)
                # Verifica se o conteúdo do JSON é uma lista
                if isinstance(data, list):
                    all_outputs = data
                else:
                    print("Arquivo JSON existente não é uma lista. Criando uma nova.")
            except json.JSONDecodeError:
                print("Arquivo JSON existente está corrompido. Criando uma nova lista.")

    # Adiciona a nova saída
    all_outputs.append(new_output)

    # Salva o resultado atualizado no arquivo
    with open(output_file, "w") as json_file:
        json.dump(all_outputs, json_file, indent=4)

    print(f"Saída adicionada ao arquivo {output_file}")


if __name__ == "__main__":
    # Substitua pelos valores desejados ou configure para ler do usuário
    executar_docker_compose_tcp(
        compose_file="compose-tcp.yml",
        service="tcp-client",
        script="tcp-client.py",
        host="10.5.0.2",
        port=8080,
        requests=10,  # Variavel
        command="SNMPWALK",  # varivael
        session=True,
        log="performance.log",
        keep=1,  # variavel
        output_file="output.json",  # variavel
    )
