import datetime
import psutil
import sys
import subprocess
import time
import os


print('iniciando matado de proceso')

for i in psutil.pids():
    process = psutil.Process(i)
    if process.name() == '3001' or  process.name() == 'CCM' or  process.name() == 'Sockmon' or process.name() == 'Sockserver':
        print(f'matando proceso : {process.name()}')
        process.kill()
        print('proceso muerto')
   

print('fin de matado de proceso')
