import sys
import pika

class cMessage:  
    def WriteMessage(Credenciales,IN_NameQueue,SendText):
        Conexion=pika.BlockingConnection(pika.URLParameters(Credenciales))
        Canal=Conexion.channel()
        Canal.queue_declare(queue=IN_NameQueue,durable=True)
        Mensaje=SendText
        Canal.basic_publish(exchange='',
                      routing_key=IN_NameQueue,
                      body=Mensaje,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
        Conexion.close()


