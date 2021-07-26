from core.elements import *
from core.info import *
import numpy as np
import matplotlib.pyplot as plt
import random


def main():
    for filename in ["../resources/258211.json"]:
        #           "../resources/nodes_full_shannon.json"
        #           "../resources/nodes_full_flex_rate.json",
        #           "../resources/nodes_full_fixed_rate.json"]:
        net = Network(filename)
        allNodes = list(net.nodes.keys())
        initial_power = 1e-3

        M=1
        name=filename.replace("../resources/nodes_full_","").replace(".json","")
        while not net.saturated:
            all_connections=[]
            totalCapacity=0
            all_connections=net.test_network(M)

            # for i in range(100):
            #     inputN = random.choice(allNodes)
            #     output = random.choice(allNodes)
            #     while output == inputN:
            #         output = random.choice(allNodes)
            #     all_connections.append(Connection(inputN, output, initial_power))
            #
            # net.stream(all_connections, "snr")

            data = []
            for connessione in all_connections:
                if connessione.snr!=0:
                    data.append(connessione.bit_rate)
                    totalCapacity+=connessione.bit_rate
            try:
                meanCapacity=totalCapacity/len(data)
            except ZeroDivisionError:
                print("No accepted connections")
            print("M={}\nTotal allocated bitrate for {} connection: {}\n\tmean capacity: {}\nAccepted connections {}\n".format(M,name,totalCapacity,meanCapacity,len(data)))
            f = plt.figure(1)
            #bins = np.linspace(2.6e15, 2.9e15, 29-25)
            #plt.hist(data, bins=bins, edgecolor='black')
            plt.hist(data,bins=100, edgecolor='black')
            plt.title(name+" with M= "+str(M))
            plt.xlabel("Capacity in bps")
            plt.ylabel("Number of connections")
            f.show()
            M+=1


if __name__ == "__main__":
    main()
