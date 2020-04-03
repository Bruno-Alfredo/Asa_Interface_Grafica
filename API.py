from time import sleep 
from random import randint 
import random
import time

#Variable global 
estado = '1' 
data_type = 0
start = 0

#Estados 

        

def Conf_Start(entrada):
    global estado
    print("Confirmação")
    if entrada == 0xa5:
        estado = 2
    

def Type(entrada): 
    global estado, start, data_type
    print('Type') 
    if(entrada == 0x01 and start == 0):#Start of Transmission
        start = 1
        estado = 3
        data_type = entrada
    if(entrada == 0x03 and start == 1):#End Of Transmission
        start = 0
        estado = 3
        data_type = entrada
    if entrada >= 0x10 and entrada <= 0x15 and start == 1: 
        estado = 3
        data_type = entrada
        print("Sensores") 
    if entrada >= 0xfa and entrada <= 0xff and start == 1: 
        estado = 3 
        data_type = entrada
        print("Mensagem") 
    
         
def Time_Stamp(entrada): 
    global estado 
    print('Time_stamp') 
    if data_type >= 0x10 and data_type <= 0x15: 
        estado = 3 
        print("Dados") 
    if data_type >= 0xfa and data_type <= 0xff: 
        estado =  5
        print("Conf_End") 

def Data(entrada): 
    global estado, data_type
    print("Dados")
    if data_type == 0x11:
        print("Câmera")
    elif data_type == 0x12:
        print("Velocidade")
    elif data_type == 0x13:
        print("Posição")
    elif data_type == 0x14:
        print("Aceleração")
    elif data_type == 0x15:
        print("Temperatura")
    elif data_type == 0x16:
        print("Pressão")
    elif data_type == 0x17:
        print("Tensão")
    elif data_type == 0x18:
        print("Corrente")
    elif data_type == 0x19:
        print("Potência")
    elif data_type == 0x20:
        print("Taxa de Transmissão")
    elif data_type == 0x21:
        print("Campo Magnético")
    elif data_type == 0x22:
        print("GPS")
    estado = 5
            

        
def Conf_End(entrada):
    global estado
    print("Confirmação Saída")
    if entrada == 0x5a:
        estado = 1

#Finite State Machine (FSM) 
def FSM(entrada):
    global estado
    switch = {
        1 :Conf_Start,
        2 :Type,
		3 :Time_Stamp,
        4 :Data,
        5 :Conf_End,
    } 
    func = switch.get(estado, lambda: None)
    return func(entrada)

#Programa Principal 
while True:     
	lst = []
	lst.append('0x5a')
	lst_type = ['0x11', '0x12', '0x13', '0x14', '0x15', '0x16', '0x17', '0x18', '0x19', '0x20', '0x21', '0x22']

	random.seed(time.time)
	lst.append(lst_type[random.randint(0, len(lst_type)-1)])
	for i in range(0,8):
		lst.append(hex(random.getrandbits(8)))

	lst.append('0x5a')
	for i in range(len(lst)):
		lst[i] = int(lst[i], 16)


	for i in range(len(lst)):
		FSM(lst[i]) 
	
	sleep(1)
