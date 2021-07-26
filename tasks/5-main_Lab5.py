from core.elements_6th_lab import *
from core.info import *
import numpy as np
import matplotlib.pyplot as plt
import random


def main():
    net = Network("/home/luchino/scuola/ovn/resources/nodes.json")
    allNodes = list(net.nodes.keys())
    initial_power = 1e-3
    all_connections = []

    for i in range(100):
        inputN = random.choice(allNodes)
        output = random.choice(allNodes)
        while output == inputN:
            output = random.choice(allNodes)
        all_connections.append(Connection(inputN, output, initial_power))

    net.stream(all_connections, "snr")

    data = []
    [data.append(connessione.snr) for connessione in all_connections]
    f = plt.figure(1)
    bins = np.linspace(68, 83, 83 - 67)
    plt.hist(data, bins=bins, edgecolor='black')
    plt.title("SNRs")
    plt.xlabel("SNR in dB")
    plt.ylabel("Number of connections")
    f.show()


if __name__ == "__main__":
    main()
