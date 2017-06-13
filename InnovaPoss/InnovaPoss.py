import pika
import time
import subprocess
from Config.cConfig import cConfig as  oConfig
from Queue.cMenssage import cMessage as oMessage
from ConsultHttp import Simulator as oSimulador
from TCPClient import TCPDataAdapter

print("Ejecutando sockserver")
subprocess.call(['./Ejecutables/Sockserver'])
print("Lectura de la maquina")


Conexion=pika.BlockingConnection(pika.URLParameters(oConfig.ConexionRabbit()))
Canal=Conexion.channel()
Canal.queue_declare(queue=oConfig.IN_NameQueue(),durable=True)
ccm_adapter=TCPDataAdapter()
mon_adapter=TCPDataAdapter()
ccm_adapter.open()
mon_adapter.bind_and_setup_listening()
result = ccm_adapter.transact_message("CCM_Getstatus")
print(result)
result = ccm_adapter.transact_message("CCM_Select(1,1)")
print(result)
result = ccm_adapter.transact_message("CCM_Write(1,1)")
print(result)

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
            #Rpt=oSimulador.CCN_Status()
            if Rpt=='KO':
                concatenado='CL|'+result[1]+'|'+result[2]+'|'+Rpt               
                oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
            else:
                Rpt1=oSimulador.CCN_Preparar(result[3])
                if Rpt1=='OK':
                    Rpt2=oSimulador.CCN_Despachar(result[3])
                    if Rpt2=='OK':
                        concatenado='CL|'+result[1]+'|'+result[2]+'|Despachando'
                        oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
                    else:
                        concatenado='CL|'+result[1]+'|'+result[2]+'|Error'
                        oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
                else:
                    concatenado='CL|'+result[1]+'|'+result[2]+'|Error'
                    oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),concatenado)
                    print('Error Preparando')

           
    if result[0]=='CL':#servidor
        print('prueba')

Canal.basic_qos(prefetch_count=1)
Canal.basic_consume(callback,queue=oConfig.IN_NameQueue())
Canal.start_consuming()


