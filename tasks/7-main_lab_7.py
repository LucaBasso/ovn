from core.elements import *
from core.info import *
import numpy as np
import matplotlib.pyplot as plt
import random


def main():
    for filename in ["/home/luchino/scuola/ovn/resources/nodes_full_fixed_rate.json",
                     "/home/luchino/scuola/ovn/resources/nodes_full_flex_rate.json",
                     "/home/luchino/scuola/ovn/resources/nodes_full_shannon.json"]:
        net = Network(filename)
        allNodes = list(net.nodes.keys())
        initial_power = 1e-3
        all_connections = []
        totalCapacity=0
        name=filename.replace("/home/luchino/scuola/ovn/resources/nodes_full_","").replace(".json","")

        for i in range(100):
            inputN = random.choice(allNodes)
            output = random.choice(allNodes)
            while output == inputN:
                output = random.choice(allNodes)
            all_connections.append(Connection(inputN, output, initial_power))

        net.stream(all_connections, "snr")

        data = []
        for connessione in all_connections:
            if connessione.snr!=0:
                data.append(connessione.bit_rate)
                totalCapacity+=connessione.bit_rate
        meanCapacity=totalCapacity/len(data)
        print("Total allocated bitrate for {} connection: {}\n\tmean capacity: {}\n".format(name,totalCapacity,meanCapacity))
        f = plt.figure(1)
        bins = np.linspace(2.6e15, 2.9e15, 29-25)
        #plt.hist(data, bins=bins, edgecolor='black')
        plt.hist(data, edgecolor='black')
        plt.title(name)
        plt.xlabel("Capacity in bps")
        plt.ylabel("Number of connections")
        f.show()


if __name__ == "__main__":
    main()
