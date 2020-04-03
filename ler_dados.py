import sqlite3
import time

count_new = 0
count_old = 0

conn = sqlite3.connect('dados_cube.db')

c = conn.cursor()

while 1:
    rows = c.execute("SELECT COUNT(*) FROM posicao")
    aux = c.fetchall()
    #print(aux)


    count_new = aux[0][0]
    if count_new > count_old:
        rows = c.execute("SELECT * FROM posicao")
        rows = c.fetchall()[-1]
        print(rows[2])
        #for x, y, z, t in ola:
        #    print("{}, {}, {} ,{}".format(x, y, z, t))

        count_old = count_new


conn.close()
