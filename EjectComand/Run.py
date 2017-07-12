import sys
import subprocess
import time


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

if __name__ == "__main__":  
    startProcess()
    while True:
        print("...")


