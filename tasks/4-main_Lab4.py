from core.elements_6th_lab import *
from core.info import *
import numpy as np
import matplotlib.pyplot as plt
import random


def main():
    """Creates 100 connections between random nodes of the network and streams them
    to show in two histograms their latencies and SNRs after the propagation"""
    net=Network("/home/luchino/scuola/ovn/resources/nodes.json")
    allNodes=list(net.nodes.keys())
    initial_power=1e-3
    all_connections=[]
    #commented lines were useful in part 6
    #all_connections2=[]

    for i in range(100):
        input=random.choice(allNodes)
        output=random.choice(allNodes)
        while output==input:
            output = random.choice(allNodes)
        all_connections.append(Connection(input,output,initial_power))
        #all_connections2.append(Connection(input,output,initial_power))

    data = []
    net.stream(all_connections,"snr")
    [data.append(connessione.snr) for connessione in all_connections]

    f = plt.figure(1)
    #bins=np.linspace(71,80,80-70)
    #plt.hist(data,bins=bins,edgecolor='black')
    plt.hist(data, edgecolor='black')
    plt.title("SNRs")
    plt.xlabel("SNR in dB")
    plt.ylabel("Number of connections")
    f.show()

    #used only in part 6
    """net.stream(all_connections2,"latency")
    data=[]
    [data.append(connessione.latency) for connessione in all_connections2]
    g=plt.figure(2)
    plt.hist(data, edgecolor='black')
    plt.title("latencies")
    plt.xlabel("Latency in seconds")
    plt.ylabel("Number of connections")
    g.show()"""


if __name__ == "__main__":
    main()


def esempio():
    """Old main I used in order to learn how to draw histograms"""
    #you can use _ as a dummy variable when you are not interested in the returned result of a function

    net=Network()
    #data=[60,60,61,63,63,64,65,67,67,68,67,66,66,69,71,62,71,70,70.1]
    data=net._weighted_paths["SNR"].values
    print(data)
    bins=np.linspace(60,72,(72-60)+1)

    plt.hist(data, bins=bins, edgecolor="black")
    plt.grid(True)
    plt.title("SNRs")
    plt.xlabel("SNRs in dB")
    plt.ylabel("Number of lines")

    plt.show()
