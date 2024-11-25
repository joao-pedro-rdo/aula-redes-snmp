#!/bin/bash

# Script para executar comandos Python em sequência com descrições detalhadas

echo "Comando 1: Executando cliente TCP via Docker Compose para enviar 10000 requisições SNMPWALK ao servidor 10.5.0.2:8080, salvando logs em performance.log e resultados em resultados.csv. Mantendo o ambiente Docker ativo após execução."
python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 10.5.0.2 --port 8080 --requests 10000 --command SNMPWALK --log performance.log --keep 1 --output_file resultados.csv

echo "Comando 2: Executando cliente TCP via Docker Compose para enviar 10000 requisições SNMPWALK ao servidor 10.5.0.2:8080 com modo detalhado (verbose), salvando logs em performance.log e resultados em resultados.csv. Mantendo o ambiente Docker ativo após execução."
python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 10.5.0.2 --port 8080 --requests 10000 --command SNMPWALK --log performance.log --verbose true --keep 1 --output_file resultados.csv

echo "Comando 3: Executando cliente TCP via Docker Compose para enviar 10000 requisições SNMPWALK ao servidor 10.5.0.2:8080, salvando logs em performance.log e resultados em resultados.csv. Mantendo o ambiente Docker ativo após execução."
python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 10.5.0.2 --port 8080 --requests 10000 --command SNMPWALK --log performance.log --keep 0 --output_file resultados.csv

echo "Comando 4: Executando cliente TCP via Docker Compose para enviar 10000 requisições SNMPWALK ao servidor 10.5.0.2:8080 com modo detalhado (verbose), salvando logs em performance.log e resultados em resultados.csv. Mantendo o ambiente Docker ativo após execução."
python3 main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 10.5.0.2 --port 8080 --requests 10000 --command SNMPWALK --log performance.log --verbose true --keep 0 --output_file resultados.csv

echo "Comando 5: Executando cliente TCP local diretamente (sem Docker) para enviar 10000 requisições SNMPWALK ao servidor local (127.0.0.1:8080), salvando logs em performance.log e resultados em resultados.csv. Não mantendo o ambiente ativo após execução."
python3 main_script.py --script tcp-client/tcp-client.py --host 127.0.0.1 --port 8080 --requests 10000 --command SNMPWALK --log performance.log --keep 0 --output_file resultados.csv

echo "Comando 6: Executando cliente TCP local diretamente (sem Docker) para enviar 10000 requisições SNMPWALK ao servidor local (127.0.0.1:8080) com modo detalhado (verbose), salvando logs em performance.log e resultados em resultados.csv. Não mantendo o ambiente ativo após execução."
python3 main_script.py --script tcp-client/tcp-client.py --host 127.0.0.1 --port 8080 --requests 10000 --command SNMPWALK --log performance.log --verbose true --keep 1 --output_file resultados.csv

echo "Comando 7: Executando cliente TCP local diretamente (sem Docker) para enviar 10000 requisições SNMPWALK ao servidor local (127.0.0.1:8080), salvando logs em performance.log e resultados em resultados.csv. Não mantendo o ambiente ativo após execução."
python3 main_script.py --script tcp-client/tcp-client.py --host 127.0.0.1 --port 8080 --requests 10000 --command SNMPWALK --log performance.log --keep 0 --output_file resultados.csv

echo "Comando 8: Executando cliente TCP local diretamente (sem Docker) para enviar 10000 requisições SNMPWALK ao servidor local (127.0.0.1:8080) com modo detalhado (verbose), salvando logs em performance.log e resultados em resultados.csv. Não mantendo o ambiente ativo após execução."
python3 main_script.py --script tcp-client/tcp-client.py --host 127.0.0.1 --port 8080 --requests 10000 --command SNMPWALK --log performance.log --verbose true --keep 1 --output_file resultados.csv

echo "Todos os comandos foram executados com sucesso."
