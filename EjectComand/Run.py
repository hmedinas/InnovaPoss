import sys
import subprocess
import time
import psutil
import os

def startProcess():
    # return
    # verificamos Procesos que se estan ejecutando

    for i in psutil.pids():
        process = psutil.Process(i)
        if process.name() == '3001':
            process.kill()
        if process.name() == 'CCM':
            process.kill()
        if process.name() == 'Sockmon':
            process.kill()
        if process.name() == 'Sockserver':
            process.kill()

    # EJECUTAMOS LOS PROCESOS
    time.sleep(2)
    path3001 = f'/home/pi/AppInnova/Eject/3001'
    pathCCM = f'/home/pi/AppInnova/Eject/CCM'
    pathSockserver = f'/home/pi/AppInnova/Eject/Sockserver'
    pathSockmon = f'/home/pi/AppInnova/Eject/Sockmon'
    print('HMS: Ejecutando 3001')
    status3001 = subprocess.Popen([path3001])
    time.sleep(1)
    print('HMS: Ejecutando CCM')
    statusCCM = subprocess.Popen([pathCCM])
    time.sleep(1)
    print('HMS: Ejecutando Sockserver')
    statusSockserver = subprocess.Popen([pathSockserver])
    time.sleep(1)
    print('HMS: Ejecutando Sockmon')
    statusSockmon = subprocess.Popen([pathSockmon])


def startCCM():
    pathCCM = f'/home/pi/AppInnova/Eject/CCM'
    print('HMS: Ejecutando CCM')
    statusCCM = subprocess.Popen([pathCCM])
def start3001():
    path3001 = f'/home/pi/AppInnova/Eject/3001'
    print('HMS: Ejecutando 3001')
    status3001 = subprocess.Popen([path3001])
def startSockserver():
    pathSockserver = f'/home/pi/AppInnova/Eject/Sockserver'
    print('HMS: Ejecutando Sockserver')
    statusSockserver = subprocess.Popen([pathSockserver])
def startSockmon():
    pathSockmon = f'/home/pi/AppInnova/Eject/Sockmon'
    print('HMS: Ejecutando Sockmon')
    statusSockmon = subprocess.Popen([pathSockmon])
    
def killProces():
    for i in psutil.pids():
        process = psutil.Process(i)
    if process.name() == '3001':
        process.kill()
    if process.name() == 'CCM':
        process.kill()
    if process.name() == 'Sockmon':
        process.kill()
    if process.name() == 'Sockserver':
        process.kill()



if __name__ == "__main__": 
    os.system("fuser -k 3000/tcp")
    os.system("fuser -k 3001/tcp")
    
    print('close puertos por seguridad')
    #startProcess()

    i=0
    while True:
        rpt=str(input('''¿Iniciar Servicios?
X ==> Matar todos los procesos
A ==> Inicia CCM
B ==> Inicia 3001.
C ==> Inicia Sockserver.
E ==> Inicia Sockmon.

'''))
        if rpt=='X':
            killProces()
            print('Proceso Matado')
        if rpt=='A':
            os.system("fuser -k 3000/tcp")
            startCCM()           
        if rpt=='B':
            os.system("fuser -k 3001/tcp")
            start3001()
        if rpt=='C':
            startSockserver()
        if rpt=='D':
            startSockmon()
        

