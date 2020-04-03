import os                                                                       
from multiprocessing import Pool
                                                                                
processos = ('interface.py', 'State_machine_2.py')

def roda_processo(processo):
    os.system('python3 {}'.format(processo))

pool = Pool(processes=2)
pool.map(roda_processo, processos)
