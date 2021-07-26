from core.elements import *
import matplotlib.pyplot as plt


def main():
    filename="../resources/258211.json"
    for strategy in ["shannon"]:#["fixed_rate","flex_rate","shannon"]:
        net=Network(filename,transceiver=strategy)

        M=1
        while not net.saturated:
            totalCapacity=0
            all_connections=net.test_network(M)

            capacities=[]
            SNRs=[]
            totalSNR=0
            for connessione in all_connections:
                if connessione.snr!=0:
                    capacities.append(connessione.bit_rate)
                    SNRs.append(connessione.snr)
                    totalSNR+=connessione.snr
                    totalCapacity+=connessione.bit_rate
            try:
                meanSNR=totalSNR/len(capacities)
                meanCapacity=totalCapacity/len(capacities)
            except ZeroDivisionError:
                print("No accepted connections")
                meanCapacity=0
                meanSNR=0
            #if M>=3:
            #    print(f"{strategy} with M={M}\nTotal allocated bitrate: {totalCapacity}\n\tmean capacity: {meanCapacity}\n"
            #          f"Accepted connections {len(capacities)}\nMean SNR={meanSNR}\nTotal SNR={totalSNR}\n")
            print(f"{strategy} with M={M}\nTotal allocated bitrate: {totalCapacity}\n\tmean capacity: {meanCapacity}\n"
                  f"Accepted connections {len(capacities)}\nMean SNR={meanSNR}\nTotal SNR={totalSNR}\n")

            plt.figure(1*M)
            #bins = np.linspace(2.6e15, 2.9e15, 29-25)
            #plt.hist(data, bins=bins, edgecolor='black')
            plt.hist(capacities, bins=100, edgecolor='black')
            plt.title(strategy+" with M= "+str(M))
            plt.xlabel("Capacity in Gbps")
            plt.ylabel("Number of connections")
            # if M>=5:
            #     f.show()

            plt.figure(9*M)
            #bins = np.linspace(2.6e15, 2.9e15, 29-25)
            #plt.hist(data, bins=bins, edgecolor='black')
            plt.hist(SNRs, bins=100, edgecolor='black')
            plt.title(strategy+" with M= "+str(M))
            plt.xlabel("SNR")
            plt.ylabel("Number of connections")
            # if M>=5:
            #     g.show()
            plt.show()

            M+=1


if __name__ == "__main__":
    main()
