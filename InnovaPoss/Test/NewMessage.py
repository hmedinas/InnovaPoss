import collections
import logging
import warnings
import pika
import pika.frame as frame
import pika.exceptions as exceptions
import pika.spec as spec
from pika.utils import is_callable


import collections
import logging
import warnings
import uuid

import pika.frame as frame
import pika.exceptions as exceptions
import pika.spec as spec
from pika.utils import is_callable
from pika.compat import unicode_type, dictkeys, as_bytes

import datetime


LOGGER = logging.getLogger(__name__)
MAX_CHANNELS = 32768


class Messaje():
    Start:str='{"Comand": "START","QueueIn": "PHONE_START_IN","QueueOut": "PHONE_START_OUT","QueueTime":3600}'
    Prepare:str=' {"Comand": "PREPARE","Phone": ""}'
    Dispachar:str='{"Comand": "DISPACHER","Phone": "-", "Ejecut": "2", "Carril":"1,1", "Price":1,"Promo":"true" } '
    Cancel:str=''
    Finish:str=''
    ServerMsg:str='{"Comand":"DISPACHER","MACHINE":"001233998873","CARRIL":"1,2"}'

class ComandType():
    Start:str='ccm.start'
    Prepare:str='ccm.prepare'
    Disapacher:str='ccm.dispacher'
    Cancel:str='ccm.Cancel'
    Finish:str='ccm.finish'
    ServerMsg:str='ccm.server'
    Stock:str='ccm.stock'


class SendMessageRabbit():
    Credenciales:str='ampqs://innova_demo:dimatica@innova.boromak.com'
    IN_NameQueue_Server:str="IN_123456789"
    PUT_NameQueue_Server:str="OUT_123456789"
    IN_NameQueue_App:str="PHONE_START_IN"
    PUT_NameQueue_App:str="PHONE_START_OUT"

    is_open:bool=False
    def __init__(self):
      self.Conexion=pika.BlockingConnection(pika.URLParameters(self.Credenciales))
      self.Canal=self.Conexion.channel()
      pass
   

    
    def sendStart(self):
       
        Cx=pika.BlockingConnection(pika.URLParameters(self.Credenciales))
        ch=Cx.channel()
        ch.queue_declare(queue='IN_123456789',durable=True)
        Mensaje='{"Comand": "START","QueueIn": "PHONE_START_IN","QueueOut": "PHONE_START_OUT","QueueTime":120}'
        ch.basic_publish(exchange='',
                      routing_key='IN_123456789',
                      body=Mensaje,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent

                      ))
                    
        self.Conexion.close()

    def sendMessage(self,ComandType:str, _Queue:str, _Message:str,_durable:bool=False):
        if(_Queue is None):
            _queue_temp=self.IN_NameQueue_Server
        else:
            _queue_temp=_Queue

        self.Canal.queue_declare(queue=_queue_temp,durable=_durable)
        Mensaje=_Message
        self.Canal.basic_publish(exchange='',
                      routing_key=_queue_temp,
                      body=Mensaje,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                         type=ComandType
                         #,expiration='200000'
                      ))
                    
        #self.Conexion.close()

    def queue_delete(self,_Queue:str=None):  
        if _Queue is None:
             self.Canal.queue_delete(_Queue,False,False)         
        else:
             self.Canal.queue_delete(self.IN_NameQueue_App,False,False)
             self.Canal.queue_delete(self.PUT_NameQueue_App,False,False)

    def queue_purge(self,_Queue:str):
        self.Canal.queue_purge(_Queue)

    def restar_hora(self,hora1,hora2):
        formato = "%H:%M:%S"
        h1 = datetime.strptime(hora1, formato)
        h2 = datetime.strptime(hora2, formato)
        resultado = h1 - h2
        return str(resultado)
    def killProcesos():
        print('iniciando matado de proceso')
        for i in psutil.pids():
            process = psutil.Process(i)
            if process.name() == '3001':
                process.kill()
                print(f'kill 3001')
            if process.name() == 'CCM':
                process.kill()
                print(f'kill CCM')
            if process.name() == 'Sockmon':
                process.kill()
                print(f'kill Sockmon')
            if process.name() == 'Sockserver':
                process.kill()
                print(f'kill Sockserver')

        print('fin de matado de proceso')

            # EJECUTAMOS LOS PROCESOS


if __name__=='__main__':
    msg=SendMessageRabbit()
    _ComandType=ComandType()
    _oMessage=Messaje()
    _server:str=''
    _client:str=''


    fecha:datetime=None
    fecha1=datetime.datetime.now()
    fecha2=datetime.timedelta(minutes=2,seconds=0)
    Resul=fecha1+fecha2
    print(type(Resul))
    print(Resul.strftime('%H:%M:%S'))

    #rpt=msg.restar_hora("10:40:50","10:30:30")
    
    #print(rpt)

    while True:
        rpt=str(input('''¿Ingrese Accion?
K ==> kill procesos
S ==> Inicio Proceso.
P ==> Prepara Maquina.
C ==> Cancelar todo.
D ==> Despachar Producto.
F ==> Finish de proceso
MS ==> Mensaje servidor
ST ==> Stock
del==> Elimina Cola
pur ==> Purga Cola 
'''))
        if rpt=='K':
            killProcesos()
        if rpt=='S':
            #msg.sendStart()
            #print('Mensaje Enviado')
            msg.sendMessage(ComandType=_ComandType.Start,_Queue=None,_Message=_oMessage.Start,_durable=True)
            print('Mensaje Enviado')
        if rpt=='P':
            msg.sendMessage(ComandType=_ComandType.Prepare,_Queue=msg.IN_NameQueue_App,_Message=_oMessage.Prepare,_durable=True)
            print('Preparada')
        if rpt=='C':
            msg.sendMessage(ComandType=_ComandType.Cancel,_Queue='',_Message=_oMessage.Cancel,_durable=True)
            print('Cancelada')
        if rpt=='D':
            msg.sendMessage(ComandType=_ComandType.Disapacher,_Queue=msg.IN_NameQueue_App,_Message=_oMessage.Dispachar,_durable=True)
            print('Despachando')
        if rpt=='F':
            msg.sendMessage(ComandType=_ComandType.Finish,_Queue=msg.IN_NameQueue_App,_Message=_oMessage.Finish,_durable=True)
            print('Finalizado')
        if rpt=='MS':
             msg.sendMessage(ComandType=_ComandType.ServerMsg,_Queue='OUT_ServerREAD',_Message=_oMessage.ServerMsg,_durable=True)
             print('Mensaje Server')
        if rpt=='del':
            msg.queue_delete('INC_123456789')
        if rpt=='ST':
            msg.sendMessage(ComandType=_ComandType.Stock,_Queue=msg.IN_NameQueue_Server,_Message='',_durable=True)
            print('Mensaje Server')