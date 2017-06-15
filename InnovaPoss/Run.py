import sys
import pika
import time
import subprocess
import os
from cConfig import cConfig as  oConfig
from cMenssage import cMessage as oMessage
from ConsultHttp import Simulator as oSimulador
from TCPClient import TCPDataAdapter

ccm_adapter=TCPDataAdapter()
mon_adapter=TCPDataAdapter()
ccm_adapter.open()
mon_adapter.bind_and_setup_listening()
mon_adapter.incoming_msg_handler = monedero_callback

def Run():
    #Cargar Procesos
    
    ccm_adapter=TCPDataAdapter()
    mon_adapter=TCPDataAdapter()
    ccm_adapter.open()
    mon_adapter.bind_and_setup_listening()
    mon_adapter.incoming_msg_handler = monedero_callback


    Ejct=RunEjecutablesPi(mon_adapter)

    if Ejct==True:
        #lectura de colas
        Print('qwwq')
    else:
        Print('RunEjecutablesPi ==>Error...')
        #Escribir un log del proceso
        sys.exit()
    

def RunEjecutablesPi():
    print('=============================================')
    print('======       Iniciando Ejecutables   ========')
    print('=============================================')

    path=f'/home/pi/innovapos-demo/InnovaPoss/Ejecutables/3001'
    print(f"Ejecutando 3001 desde {path}")
    exit_status = subprocess.Popen([path])
    print(f"Result 3001: {exit_status}")
    time.sleep(1)
    path = f'/home/pi/innovapos-demo/InnovaPoss/Ejecutables/CCM'
    print(f"Ejecutando CCM desde {path}")
    exit_status = subprocess.Popen([path])
    print(f"Result CCM: {exit_status}")
    time.sleep(2)
    path = f'/home/pi/innovapos-demo/InnovaPoss/Ejecutables/Sockserver'
    print(f"Ejecutando sockserver desde {path}")
    exit_status = subprocess.Popen([path])
    print(f"Result sockserver {exit_status}")

    path = f'/home/pi/innovapos-demo/InnovaPoss/Ejecutables/Sockmon'
    print(f"Ejecutando sockmon desde {path}")
    exit_status = subprocess.Popen([path])
    print(f"Result sockmon: {exit_status}")

    return True;

def monedero_callback(mensaje):
    print(f"New monedero message {mensaje}")
    

def CallBack(ch, method, properties, body):
    result=body.decode("utf-8").split('|')
    Cmd_Eject=result
    ch.basic_ack(delivery_tag = method.delivery_tag)
    if result[0]=='SR' and result[2]=='1':
        Rtp=GetStatus(f'{result[0]}|result[1]|result[2]',True)
    if result[0]=='SR' and result[2]=='2':
        Rtp=DispacherMachine(f'{result[0]}|result[1]|result[2]')

    return True;



def DispacherMachine(Parr):
    r=Parr.split('|')
    #Verificamos Estatus
    _Rpt=GetStatus(r[0]+'|'+r[1]+'|1',False)
    _Error='KO|Status'
    if(_Rpt==True):
        #Pre Seleccionamos 
        _Rpt=GetSelect(r[3])
        _Error='KO|SelecionProducto'
        if(_Rpt==True):
            _Rpt=WriteProducto(r[3])
            _Error='KO|SelecionProducto'
            return True
    
    _Error=r[0]+'|'+r[1]+'|'+r[2]+'|'+_Error
    oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),_Error)
    return False
    #Pre seleccionamos
    #verificamos el Monto en Monedero
    #Despachamos
 
def GetStatus(Parr,sendMessage):
    _Rpt=ccm_adapter.transact_message('CCM_Getstatus')
    if 'OK' in _Rpt:
        _msg='OK'
        _return=False
    else:
        _msg='KO'
        _return=True
    Parr=Parr+'|'+_msg
    if sendMessage==True:
        oMessage.WriteMessage(oConfig.ConexionRabbit(),oConfig.OUT_NameQueue(),Parr)
    return _return;

def GetSelect(Parr):
    _Rpt=ccm_adapter.transact_message("CCM_Select("+Parr+")")
    if 'OK' in _Rpt:
        return False
    else:
        return True;

def WriteProducto():
    _Rpt=ccm_adapter.transact_message("CCM_Write("+result[3]+")")
    if 'OK' in _Rpt:
        return True
    return False

def EnvioProducto():
    Rpt2= ccm_adapter.transact_message("CCM_Write("+result[3]+")")
    print(f"Write Result {Rpt2}")
def SeletMachine():
    return True;



if __name__=='__main__':
    ccm_adapter=TCPDataAdapter()
    mon_adapter=TCPDataAdapter()
    ccm_adapter.open()
    mon_adapter.bind_and_setup_listening()
    mon_adapter.incoming_msg_handler = monedero_callback
    Run()
