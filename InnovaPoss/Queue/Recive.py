import pika
import time
from Config.cConfig import cConfig as  oConfig
from Queue.cMenssage import cMessage as oMessage
import threading
import time
from threading import Timer

Conexion=pika.BlockingConnection(pika.URLParameters(oConfig.ConexionRabbit()))
Canal=Conexion.channel()
Canal.queue_declare(queue=oConfig.IN_NameQueue(),durable=True)

def callback(ch, method, properties, body):
    print(body) 
    result=body.decode("utf-8").split('|')  #SR|guid|1|234234
    ch.basic_ack(delivery_tag = method.delivery_tag)
    if result[0]=='SR':#servidor
        if result[2]=='1':
            concatenado='CL|'+result[1]+'|'+result[2]+'|OK'
            oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
        if result[2]=='2':
            concatenado='CL|'+result[1]+'|'+result[2]+'Despachando'
            oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
    if result[0]=='CL':#servidor
        print('prueba')

Canal.basic_qos(prefetch_count=1)
Canal.basic_consume(callback,queue=oConfig.IN_NameQueue(), no_ack=True)
try:
    Canal.start_consuming()
except KeyboardInterrupt:
    Canal.stop_consuming()
Conexion.close()