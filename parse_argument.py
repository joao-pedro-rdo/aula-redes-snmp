import argparse


def get_argments():
    """
    Configura e retorna os argumentos passados via linha de comando.
    """
    parser = argparse.ArgumentParser(
        description="Executa testes de desempenho TCP via Docker Compose."
    )

    # Argumentos obrigatórios e opcionais
    parser.add_argument(
        "--compose_file",
        # required=True,
        # default="compose-tcp.yml",
        type=str,
        help="Arquivo Docker Compose (ex: compose-tcp.yml)",
    )
    parser.add_argument(
        "--service",
        # required=True,
        # default="tcp-client",
        type=str,
        help="Serviço no Docker Compose (ex: tcp-client)",
    )
    parser.add_argument(
        "--script",
        # required=True,
        default="tcp-client.py",
        type=str,
        help="Script Python a ser executado (ex: tcp-client.py)",
    )
    #! Argumento obrigatório
    parser.add_argument("--host", required=True, help="Endereço do host (ex: 10.5.0.2)")
    parser.add_argument(
        "--port",
        # required=True,
        default=8080,
        type=int,
        help="Porta do servidor TCP (ex: 8080)",
    )
    parser.add_argument(
        "--requests",
        # required=True,
        default=10000,
        type=int,
        help="Número de requisições a serem enviadas",
    )
    parser.add_argument(
        "--command",
        # required=True,
        default="SNMPWALK",
        help="Comando a ser executado (ex: SNMPWALK)",
    )
    parser.add_argument(
        "--session",
        action="store_true",
        default="session",
        help="Habilita flag de sessão",
    )
    parser.add_argument(
        "--log",
        # required=True,
        default="performace.log",
        type=str,
        help="Arquivo de log (ex: performance.log)",
    )
    parser.add_argument(
        "--verbose",
        help="Flag de manter conexões (0 - mantem a conexao ou 1 - fecha conexão a cada chamada)",
    )
    parser.add_argument(
        "--keep",
        required=True,
        type=int,
        help="Flag de manter conexões (0 - mantem a conexao ou 1 - fecha conexão a cada chamada)",
    )
    parser.add_argument(
        "--output_file",
        # required=True,
        default="output.csv",
        help="Arquivo JSON de saída (ex: output.json)",
    )

    return parser.parse_args()
