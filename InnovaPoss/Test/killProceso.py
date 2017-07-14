import datetime
import sys
import subprocess
import time
import os


print('iniciando matado de proceso')
import psutil

for process in psutil.process_iter():
   
    if process.name == '3001' or  process.name == 'CCM' or  process.name== 'Sockmon' or process.name == 'Sockserver':
        print(f'matando proceso : {process.name}')
        process.kill()
        print('proceso muerto')
   

print('fin de matado de proceso')
