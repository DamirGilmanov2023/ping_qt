import threading
from queue import Queue
from ping3 import ping, verbose_ping
import json
mass=[]
#flag_ping=False
def pr(q):
    global mass
    while True:
        m = q.get()
        response = ping(str(m))
        #        print(f"Пинг хоста {m}")
        if response != False and response != None:
            mass.append(m)
        #            print("Удачно")
        else:
            pass
        #            print("Нет связи")
        q.task_done()
def go():
    global mass#,flag_ping
    print("work")
    #flag_ping=True
    with open('ip.json', 'r', encoding='utf-8') as f:
        ip = json.load(f)

    #print("Постановка в очередь")
    q=Queue()
    for i in ip:
        for x in ip[i]:
            q.put(x)
    th=[]
    i=0
    while i<100:
        th.append(threading.Thread(target=pr,args=(q,),daemon=True))
        i+=1
    i=0
    #print("Запуск потоков")
    while i<100:
        th[i].start()
        i+=1
    q.join()
    #flag_ping=False
    return mass
