import serial
import sqlite3


varType = 0
varData = 0
time_stamp = 0
lido = ''



def Conf_S(State):
    global lido
    print("Passou pelo Conf_S")
    State = 0
    if lido[:8] == '10100101':
        lido = lido[8:]
        State = 1
    else:
        lido = lido[8:]
        State = 0
    return State

def Type(State):
    global varType, lido
    varType = lido[:8]
    print("Type")
    if '00010001' <= varType <= '00011100':
        lido = lido[8:]
        State = 2
    elif '11111011' <= varType <= '11111111':
        lido = lido[8:]
        State = 2
    else:
        State = 0
    return State

def Time_Stmp(State):
    global lido, time_stamp
    print("Time Stamp")
    time_stamp = int(lido[:16], 2)
    lido = lido[16:]
    State = 3
    return State

def Data(State, conn):
    global varData, lido, time_stamp
    if varType == '00010001': 
        print("Câmera")
        State = 4
    elif varType == '00010010':
        print("Velocidade")
        varData = lido[:48]
        conn.execute("INSERT INTO velocidade VALUES (?, ?, ?, ?)", (int(varData[:15], 2), int(varData[16:31], 2), int(varData[32:], 2), time_stamp))
        conn.commit()
        lido = lido[48:]
        State = 4
    elif varType == '00010011':
        print("Posição")
        varData = lido[:48]
        conn.execute("INSERT INTO posicao VALUES (?, ?, ?, ?)", (int(varData[:15], 2), int(varData[16:31], 2), int(varData[32:], 2), time_stamp))
        conn.commit()
        lido = lido[48:]
        State = 4
    elif varType == '00010100':
        print("Aceleração")
        varData = lido[:48]
        conn.execute("INSERT INTO aceleracao VALUES (?, ?, ?, ?)", (int(varData[:15], 2), int(varData[16:31], 2), int(varData[32:], 2), time_stamp))
        conn.commit()
        lido = lido[48:]
        State = 4
    elif varType == '00010101':
        print("Temperatura")
        varData = lido[:8]
        conn.execute("INSERT INTO temperatura VALUES (?, ?)", (int(varData, 2), time_stamp))
        conn.commit()
        lido = lido[8:]
        State = 4
    elif varType == '00010110':
        print("Pressão")
        varData = lido[:24]
        conn.execute("INSERT INTO pressao VALUES (?, ?)", (int(varData, 2), time_stamp))
        conn.commit()
        lido = lido[24:]
        State = 4
    elif varType == '00010111':
        print("Tensão")
        varData = lido[:24]
        conn.execute("INSERT INTO tensao VALUES (?, ?)", (int(varData, 2), time_stamp))
        conn.commit()
        lido = lido[24:]
        State = 4
    elif varType == '00011000':
        print("Corrente")
        varData = lido[:24]
        conn.execute("INSERT INTO corrente VALUES (?, ?)", (int(varData, 2), time_stamp))
        conn.commit()
        lido = lido[24:]
        State = 4
    elif varType == '00011001':
        print("Potência")
        varData = lido[:24]
        conn.execute("INSERT INTO potencia VALUES (?, ?)", (int(varData, 2), time_stamp))
        conn.commit()
        lido = lido[24:]
        State = 4
    elif varType == '00011010':
        print("Taxa de Transmissão")
        varData = lido[:8]
        conn.execute("INSERT INTO taxa_de_transmissao VALUES (?, ?)", (int(varData, 2), time_stamp))
        conn.commit()
        lido = lido[8:]
        State = 4
    elif varType == '00011011':
        print("Campo Magnético")
        varData = lido[:48]
        conn.execute("INSERT INTO campo_magnetico VALUES (?, ?, ?, ?)", (int(varData[:15], 2), int(varData[16:31], 2), int(varData[32:], 2), time_stamp))
        conn.commit()
        lido = lido[48:]
        State = 4
    elif varType == '00011100':
        print("GPS")
        varData = lido[:8]
        conn.execute("INSERT INTO gps VALUES (?, ?)", (int(varData, 2), time_stamp))
        conn.commit()
        lido = lido[8:]
        State = 4
    elif '11111011' == varType:
        print("Cheacagem")
        lido = lido[8:]
    else:
        lido = lido[8:]
    print(varData)
    return State

def Conf_E(State):
    global lido
    print("Conf_E")
    if(lido[:8] == '01011010'):
        lido = lido[8:]
        State = 0
    else:
        lido = lido[8:]
        State = 4
    return State


if __name__ == '__main__':
    State = 0
    comport = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
    conn = sqlite3.connect('dados_cube.db')

    try:
        conn.execute("CREATE TABLE velocidade (vel_x REAL, vel_y REAL, vel_z REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE posicao (pos_x REAL, pos_y REAL, pos_z REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE aceleracao (ac_x REAL, ac_y REAL, ac_z REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE temperatura (temp REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE pressao (press REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE tensao (tensao REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE corrente (corrente REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE potencia (pot REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE taxa_de_transmissao (tt REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE campo_magnetico (mag_x REAL, mag_y REAL, mag_z REAL, time_stamp REAL)")
        conn.execute("CREATE TABLE gps (gps REAL, time_stamp REAL)")
    except sqlite3.OperationalError:
        pass

    conn.commit()

    while 1:
        if lido == '':
            lido = str(comport.readline())
            lido = ''.join(i for i in lido if i.isnumeric())
        if State == 0:
            State = Conf_S(State)
        elif State == 1:
            State = Type(State)
        elif State == 2:
            State = Time_Stmp(State)
        elif State == 3:
            State = Data(State, conn)
        elif State == 4:
            State = Conf_E(State)
    comport.close()
    conn.close()
