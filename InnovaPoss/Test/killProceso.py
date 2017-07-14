import datetime
import psutil
import sys
import subprocess
import time
import os

psutil.pids()
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
