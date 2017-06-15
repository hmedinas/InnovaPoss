import pika
import time
import subprocess
import os

from Config.cConfig import cConfig as  oConfig
from Queue.cMenssage import cMessage as oMessage
from ConsultHttp import Simulator as oSimulador
from TCPClient import TCPDataAdapter

path = f'/home/pi/innovapos-demo/innovaposs/ejecutables/3001'
print(f"ejecutando 3001 desde {path}")
exit_status = subprocess.popen([path])
print(f"ejecutando 3001 {exit_status}")

path = f'/home/pi/innovapos-demo/innovaposs/ejecutables/ccm'
print(f"ejecutando ccm desde {path}")
exit_status = subprocess.popen([path])
print(f"ejecutando ccm {exit_status}")

time.sleep(2)

path = f'/home/pi/innovapos-demo/InnovaPoss/Ejecutables/Sockserver'
print(f"Ejecutando sockserver desde {path}")
exit_status = subprocess.Popen([path])
print(f"Ejecutando sockserver {exit_status}")
print("Lectura de la maquina")


Conexion=pika.BlockingConnection(pika.URLParameters(oConfig.ConexionRabbit()))
Canal=Conexion.channel()
Canal.queue_declare(queue=oConfig.IN_NameQueue(),durable=True)
ccm_adapter=TCPDataAdapter()
mon_adapter=TCPDataAdapter()
ccm_adapter.open()
mon_adapter.bind_and_setup_listening()

'''
result = ccm_adapter.transact_message("CCM_Getstatus")
print(result)
result = ccm_adapter.transact_message("CCM_Select(1,1)")
print(result)
result = ccm_adapter.transact_message("CCM_Write(1,1)")
print(result)
'''

def monedero_callback(mensaje):
    print(f"New monedero message {mensaje}")
mon_adapter.incoming_msg_handler = monedero_callback

#path = f'/home/pi/innovapos-demo/InnovaPoss/Ejecutables/Sockmon'
#print(f"Ejecutando sockmon desde {path}")
#exit_status = subprocess.Popen([path])
#print(f"Ejecutando sockmon {exit_status}")

def callback(ch, method, properties, body):
    print(body) 
    result=body.decode("utf-8").split('|')  #SR|guid|1|234234
    ch.basic_ack(delivery_tag = method.delivery_tag)
    #oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.IN_NameQueue(),body.decode("utf-8"))
    
    if result[0]=='SR':#servidor
        if result[2]=='1': #Estatus maquina
            Rpt = ccm_adapter.transact_message("CCM_Getstatus")
            #Rpt=oSimulador.CCN_Status()
            concatenado='CL|'+result[1]+'|'+result[2]+'|'+Rpt
            print('Estatus Maquina: '+Rpt)
            oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
        if result[2]=='2': #Despacho maquina #SR|guid|2|1,2
            Rpt = ccm_adapter.transact_message("CCM_Getstatus")
            print(f"GetStatus Result {Rpt}")
            #Rpt=oSimulador.CCN_Status()
            if 'OK' in Rpt:
                # Rpt1=oSimulador.CCN_Preparar(result[3])
                Rpt1= ccm_adapter.transact_message("CCM_Select("+result[3]+")")
                print(f"Select Result {Rpt1}")
                if 'OK' in Rpt1:
                    #Rpt2=oSimulador.CCN_Despachar(result[3])
                    Rpt2= ccm_adapter.transact_message("CCM_Write("+result[3]+")")
                    print(f"Write Result {Rpt2}")
                    if 'OK' in Rpt2:
                        concatenado='CL|'+result[1]+'|'+result[2]+'|Despachando'
                        oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
                    else:
                        concatenado='CL|'+result[1]+'|'+result[2]+'|Error'
                        oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
                else:
                    concatenado='CL|'+result[1]+'|'+result[2]+'|Error'
                    oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
                    print('Error Preparando')
            else:
               concatenado='CL|'+result[1]+'|'+result[2]+'|ERROR'               
               oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
        if result[2]=='3':
            print(f"Sending {result[3]}")
            result_ccm = ccm_adapter.transact_message(result[3])
            print(f"Response {result_ccm}")
            

           
    if result[0]=='CL':#servidor
        print('prueba')

Canal.basic_qos(prefetch_count=1)
Canal.basic_consume(callback,queue=oConfig.IN_NameQueue())
Canal.start_consuming()