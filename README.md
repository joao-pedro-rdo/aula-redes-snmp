# aula-redes-snmp
Versionar os codigos do simulado do SNMP da aula redes

Levantar os servidores:  docker compose -f compose-server.yml up --build --remove-orphans 
Cliente UDP: python3 udp-client/udp-client.py   --port 8081 --requests 10 --command INFO
Cliente TCP:  ➜  docker compose -f compose-tcp.yml run tcp-client python tcp-client.py --host 10.5.0.2  --port 8080 --requests 10 --command SNMPWALK --session --log performance.log --keep 1
