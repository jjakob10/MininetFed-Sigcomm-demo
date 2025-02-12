import paho.mqtt.client as mqtt
import sys
import os
import logging

os.umask(0o000)

n = len(sys.argv)
if (n != 3):
    print("correct use: python network_monitor.py <broker_address> <output.net>.")

class color:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD_START = '\033[1m'
    BOLD_END = '\033[0m'
    RESET = "\x1B[0m"

  
BROKER_ADDR = sys.argv[1]
FILE_NAME  = sys.argv[2]

FORMAT = "%(asctime)s - %(infotype)-6s - %(levelname)s - %(message)s"

logging.basicConfig(level=logging.INFO, filename=FILE_NAME,
                        format=FORMAT, filemode="w")
metricType = {"infotype": "METRIC"}
executionType = {"infotype": "EXECUT"}
logger = logging.getLogger(__name__)

logger.info('start', extra=metricType)

# Callback quando o cliente recebe uma resposta CONNECT do servidor.
def on_connect(client, userdata, flags, rc):
    logger.info("Conectado com o código de resultado "+str(rc), extra=executionType)
    print("Conectado com o código de resultado "+str(rc))
    client.subscribe("$SYS/broker/bytes/#")
    client.subscribe('minifed/stopQueue')

# Callback quando uma mensagem PUBLISH é recebida do servidor.
def on_message(client, userdata, msg):
    tipo = ""
    if 'sent' in msg.topic:
        tipo = "sent:"
    else:
        tipo = "recived:"
    
    logger.info(f'{tipo} {str(msg.payload.decode("utf-8"))}', extra=metricType)
    
    # with open(FILE_NAME, 'a') as f:
    #     f.write(f'{tipo} {str(msg.payload.decode("utf-8"))}\n')


def on_message_stop(client, userdata, message):
    logger.info(f'received message to stop!', extra=executionType)
    print(color.RED + f'received message to stop!')
    exit()


client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add('minifed/stopQueue', on_message_stop)
client.on_message = on_message

client.connect(BROKER_ADDR, bind_port=1883)

client.loop_forever()  # Bloqueie a chamada de rede
