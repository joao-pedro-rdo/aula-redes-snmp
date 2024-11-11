#!/bin/bash

# Define o endereço do servidor SNMP
SERVER="snmp-server"

# OIDs para as consultas específicas
OID_SYS_DESCR="1.3.6.1.2.1.1.1.0"       # Descrição do sistema
OID_SYS_UPTIME="1.3.6.1.2.1.1.3.0"      # Tempo de atividade do sistema
OID_CPU_MODEL="1.3.6.1.2.1.25.3.2.1.3.3" # Modelo da CPU
OID_CPU_LOAD="1.3.6.1.4.1.2021.10.1.3.1" # Carga média do CPU
OID_MEM_TOTAL="1.3.6.1.4.1.2021.4.5.0"   # Memória total
OID_MEM_AVAIL="1.3.6.1.4.1.2021.4.6.0"   # Memória disponível
OID_RUNNING_PROCESSES="1.3.6.1.2.1.25.1.6.0" # Número de processos em execução

# Define os arquivos de saída
OUTPUT_FILE_SYSTEM="/app/consultas_sistema.txt"
OUTPUT_FILE_SNMPWALK="/app/todos_os_oids.txt"

# Realiza cada consulta e salva no arquivo de sistema
echo "Realizando consultas SNMP ao servidor $SERVER para informações do sistema..." > "$OUTPUT_FILE_SYSTEM"

# Descrição do sistema
SYS_DESCR=$(snmpget -v 2c -c public $SERVER $OID_SYS_DESCR | awk -F ": " '{print $2}')
echo "Descrição do sistema: $SYS_DESCR" >> "$OUTPUT_FILE_SYSTEM"

# Tempo de atividade do sistema
SYS_UPTIME=$(snmpget -v 2c -c public $SERVER $OID_SYS_UPTIME | awk -F ": " '{print $2}')
echo "Tempo de atividade do sistema: $SYS_UPTIME" >> "$OUTPUT_FILE_SYSTEM"

# Modelo da CPU
CPU_MODEL=$(snmpget -v 2c -c public $SERVER $OID_CPU_MODEL | awk -F ": " '{print $2}')
echo "Modelo da CPU: $CPU_MODEL" >> "$OUTPUT_FILE_SYSTEM"

# Carga média do CPU
CPU_LOAD=$(snmpget -v 2c -c public $SERVER $OID_CPU_LOAD | awk -F ": " '{print $2}')
echo "Carga média do CPU: $CPU_LOAD" >> "$OUTPUT_FILE_SYSTEM"

# Memória total em MB
MEM_TOTAL_KB=$(snmpget -v 2c -c public $SERVER $OID_MEM_TOTAL | awk -F ": " '{print $2}')
MEM_TOTAL_MB=$((MEM_TOTAL_KB / 1024))
echo "Memória total: $MEM_TOTAL_MB MB" >> "$OUTPUT_FILE_SYSTEM"

# Memória disponível em MB
MEM_AVAIL_KB=$(snmpget -v 2c -c public $SERVER $OID_MEM_AVAIL | awk -F ": " '{print $2}')
MEM_AVAIL_MB=$((MEM_AVAIL_KB / 1024))
echo "Memória disponível: $MEM_AVAIL_MB MB" >> "$OUTPUT_FILE_SYSTEM"

# Memória em uso em MB
MEM_USED_MB=$((MEM_TOTAL_MB - MEM_AVAIL_MB))
echo "Memória em uso: $MEM_USED_MB MB" >> "$OUTPUT_FILE_SYSTEM"

# Número de processos em execução
RUNNING_PROCESSES=$(snmpget -v 2c -c public $SERVER $OID_RUNNING_PROCESSES | awk -F ": " '{print $2}')
echo "Processos em execução: $RUNNING_PROCESSES" >> "$OUTPUT_FILE_SYSTEM"

# Mapeamento completo de todos os OIDs
echo "Iniciando mapeamento de todos os OIDs disponíveis no dispositivo $SERVER..."
snmpwalk -v 2c -c public "$SERVER" > "$OUTPUT_FILE_SNMPWALK"
echo "Mapeamento concluído. Resultados salvos em $OUTPUT_FILE_SNMPWALK"
