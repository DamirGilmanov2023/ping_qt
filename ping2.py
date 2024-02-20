import threading
from queue import Queue
from ping3 import ping, verbose_ping
from pyvis.network import Network
import json

print("Открытие ip.json файла")
with open('ip.json', 'r', encoding='utf-8') as f:
    ip = json.load(f)

nt= Network(height='900px', width='100%', bgcolor='#222222', font_color='white')

mass=[]
def pr(q):
    global mass
    while True:
        m=q.get()
        response=ping(str(m))
        print(f"Пинг хоста {m}")
        if response != False and response != None:
            mass.append(m)
            print("Удачно")
        else:
            print("Нет связи")
        q.task_done()
print("Постановка в очередь")
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
print("Запуск потоков")
while i<100:
    th[i].start()
    i+=1
q.join()
for i in ip:
    nt.add_node(i,size='50')
    for ii in ip[i]:
        if ii in mass:
            nt.add_node(ii,size='20',color='Green',label=f'{ip[i][ii]}\n{ii}')
        else:
            nt.add_node(ii,size='20',color='Red',label=f'{ip[i][ii]}\n{ii}')
        nt.add_edge(i,ii)
nt.show_buttons()
'''nt.set_options("""
const options = {
  "nodes": {
    "borderWidth": null,
    "borderWidthSelected": null,
    "opacity": null,
    "size": null
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "selfReferenceSize": null,
    "selfReference": {
      "angle": 0.7853981633974483
    },
    "smooth": false
  },
  "layout": {
    "hierarchical": {
      "enabled": true,
      "direction": "LR"
    }
  },
  "physics": {
    "hierarchicalRepulsion": {
      "centralGravity": 0,
      "avoidOverlap": null
    },
    "minVelocity": 0.75,
    "solver": "hierarchicalRepulsion"
  }
}
""")'''
print("Сохранение nx2.html файла")
nt.show('nx2.html')
print("Сохранено")
