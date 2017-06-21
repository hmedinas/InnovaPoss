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
    def TransactMessage(Credenciales,IN_NameQueue, OUT_NameQueue, SendText):
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
        CanalReceive = Conexion.channel()
        response = None
        def receive_callback(ch, method, properties, body):
            response = body

        CanalReceive.basic_consume(receive_callback, OUT_NameQueue, no_ack=False)
        while response is None:
            Conexion.process_data_events(1)
        Conexion.close()
        return response


