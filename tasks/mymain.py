from core.elements_6th_lab import *
from core.info import *

def main():
    net=Network()
    net.connect()
    #print(net.find_paths("A","F"))
    #sigProva=Signal_information(1e-3,["A","D","B","F","E","C"])
    #net.propagate(sigProva)
    #net.draw()
    #[print(net._weighted_paths.loc[label]) for label in net._weighted_paths.index]
    #print(net._weighted_paths.loc['A->B'])#['latency'])
    #print(net.weighted_paths.to_string())
    bestlat=net.find_best_snr('A','F')
    print(net._weighted_paths.loc[bestlat]["SNR"])
    print(net._weighted_paths.loc[bestlat]["latency"])
    #print(Network.path_to_list('A->B->C'))
    connections=[]
    connA=Connection("A","B",1e-3)
    connB=Connection("A","F",1e-3)
    connections.append(connA)
    connections.append(connB)
    net.stream(connections,"snr")
    #print("Conn1 snr={} lat={}".format(connections[0].snr,connections[0].latency))
    #print("Conn2 snr={} lat={}".format(connections[1].snr,connections[1].latency))

if __name__ == "__main__":
    main()