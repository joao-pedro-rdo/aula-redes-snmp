# aula-redes-snmp
Versionar os codigos do simulado do SNMP da aula redes

Levantar os servidores:  docker compose -f compose-server.yml up --build --remove-orphans 
Cliente UDP: python3 udp-client/udp-client.py   --port 8081 --requests 10 --command INFO
Cliente TCP:  ➜  docker compose -f compose-tcp.yml run tcp-client python tcp-client.py --host 10.5.0.2  --port 8080 --requests 10 --command SNMPWALK --session --log performance.log --session 1


#! python main_script.py --compose_file compose-tcp.yml --service tcp-client --script tcp-client.py --host 127.0.0.1 --port 8080 --requests 1000 --command SNMPWALK --log performance.log --session 1 --output_file resultados.csv
#! python3 main_script.py  --script tcp-client/tcp-client.py --host localhost --port 8080 --requests 1000 --command SNMPWALK --log performance.log --session 0 --output_file resultados.csv



Servidores (tcp-server.py e udp-server.py) - porta padrao 8080 mas pode ser mudado passando o parametro --port <porta>