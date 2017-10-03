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

import json


LOGGER = logging.getLogger(__name__)
MAX_CHANNELS = 32768


class Messaje():
    Start:str='{"Comand": "START","QueueIn": "PHONE_START_IN","QueueOut": "PHONE_START_OUT","QueueTime":60}'
    Prepare:str=' {"Comand": "PREPARE","Phone": "","Carril":"2,1"}'
    Dispachar:str='{"Comand": "DISPACHER","Phone": "-", "Ejecut": "2", "Carril":"2,1", "Price":1,"Promo":"true","User":"null","Camp":"null"}'
    Cancel:str=''
    Finish:str=''
    ServerMsg:str='{"Comand":"DISPACHER","MACHINE":"001233998873","CARRIL":"1,2"}'

    SetStock:str='{"Comand":"SET_STOCK","CARRIL":{"11":2,"12":5,"13":6,"14":5,"15":7, "16":5,"21":5,"22":6,"23":6,"24":6,"25":7,"26":8,"31":5,"32":6,"33":7,"34":8,"35":7,"36":8,"41":5,"42":6,"43":7,"44":8,"45":7,"46":8,"51":5,"52":6,"53":7,"54":8,"55":7,"56":8}}'
    SetStock:str='{"Comand":"SET_STOCK","CARRIL":{"51":1}}'
    GetStock:str='{"Comand":"GET_STOCK","CARRIL":"51"}'
    
    SetStockFull:str='{"Comand":"SET_STOCK_FULL","CARRIL":"11:2,12:5,13:6,14:5,15:8,16:8,21:8,22:8,23:8,24:8,25:9,26:8,31:8,32:8,33:8,34:8,35:8,36:8,41:8,42:8,43:8,44:8,45:8,46:8,51:8,52:8,53:8,54:8,55:8,56:8"}'
    GetStockFull:str='{"Comand":"GET_STOCK_FULL"}'
    SetPrecio:str='{"Comand":"SET_PRICE","CARRIL":"46","PRICE":"150"}'
    LocalStart:str='{"Comand": "START","QueueIn": "","QueueOut": "","QueueTime":60}'
    LocalPrepare:str=' {"Comand": "PREPARE","Phone": "","Carril":"4,5"}'
    localDispacher:str='{"Comand": "DISPACHER","Phone": "-", "Ejecut": "2", "Carril":"4,5", "Price":0,"Promo":"false","User":"Localhost","Camp":"null"}'

class ComandType():
    Start:str='ccm.start'
    Prepare:str='ccm.prepare'
    Disapacher:str='ccm.dispacher'
    Cancel:str='ccm.Cancel'
    Finish:str='ccm.finish'
    ServerMsg:str='ccm.server'
    Stock:str='ccm.stock'

    SetStock:str='ccm.SetStock'
    GetStock:str='ccm.GetStock'

    SetStockFull:str='ccm.SetStockFull'
    GetStockFull:str='ccm.GetStockFull'
    SetPrecio:str='ccm.SetPrecio'

    LocalStart:str='ccm.start'
    LocalPrepare:str='PrepareProduct'
    LocalDipacher:str='DispacherProduct'


class SendMessageRabbit():
    '''ampqs://innova_demo:dimatica@innova.boromak.com
        ampq://guest:guest@localhost:5672
    '''
    Credenciales:str='ampqs://innova_demo:dimatica@innova.boromak.com'
    IN_NameQueue_Server:str="IN_123456789"
    PUT_NameQueue_Server:str="OUT_123456789"
    IN_NameQueue_App:str="PHONE_START_IN"
    PUT_NameQueue_App:str="PHONE_START_OUT"

    is_open:bool=False
    def __init__(self):
      self.Conexion=pika.BlockingConnection(pika.URLParameters(self.Credenciales))
      self.Canal=self.Conexion.channel()
      
   
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
  

            # EJECUTAMOS LOS PROCESOS





if __name__=='__main__':
    msg=SendMessageRabbit()
    _ComandType=ComandType()
    _oMessage=Messaje()
    _server:str=''
    _client:str=''

    params: dict = json.loads('{"Comand":"SET_STOCK","CARRILES":{"11":2,"12":5,"13":6,"14":5}}')
    dd=params['CARRILES']

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
SS ==> Set Stock
GS ==> Get Stock por Carril
SSF ==> Set Stock Full
GSF ==> Get Stock Full
SP  ==> Set precio 
=================*==========
LS ==> Local Start
LP ==> Local Prepare
LD ==> Local Dispacher
'''))
        if rpt=='K':
            msg.killProcesos()
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
            msg.sendMessage(ComandType=_ComandType.Finish,_Queue=msg.IN_NameQueue_Server,_Message=_oMessage.Finish,_durable=True)
            print('Finalizado')
        if rpt=='MS':
             msg.sendMessage(ComandType=_ComandType.ServerMsg,_Queue='OUT_ServerREAD',_Message=_oMessage.ServerMsg,_durable=True)
             print('Mensaje Server')
        if rpt=='del':
            msg.queue_delete('INC_123456789')
        if rpt=='ST':
            msg.sendMessage(ComandType=_ComandType.Stock,_Queue=msg.IN_NameQueue_Server,_Message='',_durable=True)
            print('Mensaje Server')
        if rpt=='SS':
            msg.sendMessage(ComandType=_ComandType.SetStock,_Queue=msg.IN_NameQueue_Server,_Message=_oMessage.SetStock,_durable=True)
            print('Put stock Server')
        if rpt=='GS':
            msg.sendMessage(ComandType=_ComandType.GetStock,_Queue=msg.IN_NameQueue_Server,_Message=_oMessage.GetStock,_durable=True)
            print('Get stock Server')
        if rpt=='SSF':
            msg.sendMessage(ComandType=_ComandType.SetStockFull,_Queue=msg.IN_NameQueue_Server,_Message=_oMessage.SetStockFull,_durable=True)
            print('set full stock')
        if rpt=='GSF':
            msg.sendMessage(ComandType=_ComandType.GetStockFull,_Queue=msg.IN_NameQueue_Server,_Message=_oMessage.GetStockFull,_durable=True)
            print('Get full Stock')
        if rpt=='SP':
            msg.sendMessage(ComandType=_ComandType.SetPrecio,_Queue=msg.IN_NameQueue_Server,_Message=_oMessage.SetPrecio,_durable=True)
            print('Set Price')
        if rpt=='LS':
            msg.sendMessage(ComandType=_ComandType.LocalStart,_Queue=msg.IN_NameQueue_Server,_Message=_oMessage.LocalStart,_durable=True)
            print('inicio LocalHost')
        if rpt=='LP':
            msg.sendMessage(ComandType=_ComandType.LocalStart,_Queue=msg.IN_NameQueue_Server,_Message=_oMessage.LocalStart,_durable=True)
            print('inicio LocalHost')
        if rpt=='LD':
            msg.sendMessage(ComandType=_ComandType.LocalDipacher,_Queue=msg.IN_NameQueue_Server,_Message=_oMessage.localDispacher,_durable=True)
            print('Despachando LocalHost')
