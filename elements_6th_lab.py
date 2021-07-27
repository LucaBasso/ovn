import copy
import json,math,matplotlib.pyplot as plt,pandas
import sys

import scipy.constants

from core.info import Signal_information
import scipy.special as spsp

NUMBER_OF_CHANNELS=10
BERt=1e-3
Rs=32e9
Bn=12.5e9


class Node:
    """Class representing a node of the network"""
    def __init__(self, label:str, pos, connectedNodes, transceiver:str="fixed-rate"):
        self._label=label
        self._position=pos
        self._connected_nodes=connectedNodes
        self._successive={}  #linee adiacenti
        self._switching_matrix=None
        self._transceiver=transceiver

    @property
    def transceiver(self):
        return self._transceiver

    def propagate(self,sigIn:Signal_information,node1:str,node2:str,channelIndex:int):
        """Propagates the signal information through the node

        :param sigIn: signal information to be updated
        :param node1: node crossed before the current one
        :param node2: node to cross after the current one
        :param channelIndex: channel to occupy (-1if no occupation is required)"""
        sigIn.updatePath(self._label)
        if channelIndex!=-1:
            self._switching_matrix[node1][node2][channelIndex]=0


class Line:
    def __init__(self,newLab:str,newLen=0.0):
        self._label=newLab
        self._length=newLen
        self._successive={}  #nodi adiacenti
        self._state=[1 for i in range(NUMBER_OF_CHANNELS)]

    @property
    def state(self):
        return self._state

    def latency_generation(self):
        return self._length/(scipy.constants.c*2/3)
        #return self._length*(2/3)*3e8

    def noise_generation(self,sigPow:float):
        return 1e-9*sigPow*self._length
        #return sigPow/(2*self._length)

    def propagate(self,sigIn:Signal_information,channel:int):
        """Updates the Signal_Information argument

        :param sigIn: Signal_information to be propagated
        :param channel: number of the the channel to occupy or -1 if no channel has to be occupied"""
        sigIn.update_latency(self.latency_generation())
        sigIn.update_signal_power(self.noise_generation(sigIn.signal_power))
        sigIn.update_noise(self.noise_generation(sigIn.signal_power))
        if channel != -1:
            self._state[channel]=0

    def occupy(self,channelIndex:int):
        """Sets the given channel of the line as occupied"""
        self._state[channelIndex]=0

    def freeAllChannels(self):
        self._state=[1for i in range(len(self._state))]


def db2nu(dbvalue:float):
    """Transforms an SNR in dB into its equivalent in natural units"""
    return 10**(dbvalue/10)


class Network:
    """Class representing a network

    :param filename: elenco nodi
    :type _nodes: dict
    """
    def __init__(self,filename:str):
        self._nodes={}
        self._lines={}

        #toRead=open("/home/luchino/scuola/ovn/resources/nodes.json","r")
        toRead=open(filename,"r")
        dati=toRead.read()

        obj=json.loads(dati)    #reads the whole json file as a dictionary
        """for key in obj.keys():
        print(obj[key]["connected_nodes"])"""
        for key in obj.keys():  #every node is a {key:value} couple in the dictionary read with json.loads
            #nuoviPar={}
            #nuoviPar.update({"label":key})  #every key is the node name
                #every value associated to a label is a dictionary itself and contains the node's data
               #nuoviPar.update({chiave:obj[key][chiave]})
            if "transceiver" in obj[key].keys():
                newNode=Node(key, obj[key]["position"], obj[key]["connected_nodes"], obj[key]["transceiver"])
            else:
                newNode=Node(key, obj[key]["position"], obj[key]["connected_nodes"])

            self._nodes.update({key:newNode})

        for nodo in self._nodes.values():
            #for every node in _nodes, a line is created between the node and the other nodes connected to it
            for adiac in nodo._connected_nodes:
                newLabel=nodo._label+adiac
                newDist=self.distance(nodo._label,adiac)
                self._lines.update({newLabel:Line(newLabel,newDist)})

        self.connect()
        self._route_space=None  #dataframe indicating the free and occupied channels of each possible path
        self._weighted_paths=self.create_dataframe()
        #dataframe indicating various characteristics for each channel of each path

    @property
    def nodes(self):
        return self._nodes

    @property
    def weighted_paths(self):
        return self._weighted_paths

    def distance(self,label1:str,label2:str):
        node1=self._nodes[label1]
        node2=self._nodes[label2]
        return math.sqrt((node1._position[0]-node2._position[0])**2+(node1._position[1]-node2._position[1])**2)

    def connect(self):
        """
        fills the _successive dictionaries present in every node/line to indicate the lines/nodes connected to it
        and createse the switching matrix for each node
        """
        for linea in self._lines.values():
            nodeLabel=linea._label[0]
            linea._successive.update({nodeLabel:self._nodes[nodeLabel]})
            self._nodes[nodeLabel]._successive.update({linea._label:linea})
        for nodo in self._nodes.values():
            nodo._switching_matrix={}
            length=len(nodo._connected_nodes)
            new_dict={}
            for nodo2 in nodo._connected_nodes:
                for nodo3 in nodo._connected_nodes:
                    newVect=[]
                    if nodo2==nodo3:
                        [newVect.append(0) for i in range(NUMBER_OF_CHANNELS)]
                    else:
                        [newVect.append(1) for i in range(NUMBER_OF_CHANNELS)]
                    new_dict.update({nodo3:copy.copy(newVect)})
                nodo._switching_matrix.update({nodo2:copy.copy(new_dict)})

    def find_paths(self,label1:str,label2:str):
        """Finds all the possible paths connecting two nodes

        :param label1: label for starting node
        :param label2: label for ending node
        :return: a list containing all the paths, represented as lists of node labels
        """
        if not (self._nodes.keys().__contains__(label1)) or not (self._nodes.keys().__contains__(label2)):
            print("Nodi inesistenti")
            return []
        found_paths=[]  #lista di tutte le soluzioni trovate
        percorso=[label1]  #lista in cui si salveranno i nodi attraversati
        crossable={}  #indica quali nodi siano attraversabili

        [crossable.update({nodo:True}) for nodo in self._nodes.keys()]
        """for nodo in self._nodes.keys():
            crossable.update({nodo:True})"""  #less efficient: in-line loops are preferable
        crossable[label1]=False
        self.find_pathsR(label1,label2,crossable,percorso,found_paths)
        return found_paths

    def find_pathsR(self,label1,label2,crossable,percorso,found_paths):
        """Recursive version of the wrapper function find_paths

        :param label1: starting node
        :param label2: ending node
        :param crossable: dictionary which associates every node label to the possibility of crossing it
        :param percorso: list of crossed nodes
        :param found_paths: list of paths already found
        """
        if label1==label2:
            found_paths.append(list.copy(percorso))
            return

        for line in self._nodes[label1]._successive.keys():
            if crossable[line[1]]:
                percorso.append(line[1])
                crossable[line[1]]=False
                self.find_pathsR(line[1],label2,crossable,percorso,found_paths)
                crossable[line[1]]=True
                percorso.remove(line[1])

    @staticmethod
    def multiply_vectors(v1:list,v2:list):
        toReturn=[]
        [toReturn.append(v1[i]*v2[i]) for i in range(len(v1))]
        return toReturn

    def propagate(self,sigIn:Signal_information,channel:int):  #we can assume only correct paths can be passed
        """
        It can propagate the Signal_information without occupying the crossed path: this is useful if you want to just
        simulate the crossing of a lightpath

        :param sigIn: the Signal_information to propagate
        :param channel: the channel we want to make the Signal_information to propagate on; it must be -1 if you want to use the method just as a simulation method without occupying any channel
        """
        path=copy.copy(sigIn.path)

        if channel != -1:   #this part will be executed only if a channel has to be occupied
            for i in range(len(path) - 1):  #iterates on every line in the path
                toUpdate=[]
                #self._lines[path[i] + path[i + 1]].occupy(channel)
                for label in self._route_space.index:
                    if path[i]+"->"+path[1+i] in label:
                        toUpdate.append(label)
                self._lines[path[i] + path[i + 1]].propagate(sigIn, channel)
            for j in range(len(path)-1)[1:len(path)-1]:
                self._nodes[path[j]].propagate(sigIn,path[j-1],path[j+1],channel)
            for lab in toUpdate:
                label=self.path_to_list(lab)
                vect=[1 for i in range(NUMBER_OF_CHANNELS)]
                for i in range(len(label)-1):   #moltiplica per tutti i vettori di stato delle linee del path
                    vect=self.multiply_vectors(vect,self._lines[label[i]+label[i+1]].state)
                for i in range(len(label)-1)[1:]:
                    vect=self.multiply_vectors(vect,self._nodes[label[i]]._switching_matrix[label[i-1]][label[i+1]])
                self._route_space.loc[lab]=copy.copy(vect)
        else:
            [self._lines[path[i] + path[i + 1]].propagate(sigIn, channel) for i in range(len(path) - 1)]
            [self._nodes[nodo].propagate(sigIn,"","",channel) for nodo in list.copy(path)]

        return sigIn

    def draw(self):
        for linea in self._lines.values():
            p1=self._nodes[linea._label[0]]
            p2=self._nodes[linea._label[1]]
            x=[p1._position[0],p2._position[0]]
            y=[p1._position[1],p2._position[1]]
            plt.plot(x,y)
        for nodo in self._nodes.values():
            plt.scatter(nodo._position[0],nodo._position[1])
            plt.annotate(nodo._label,nodo._position)
        plt.show()

    @staticmethod
    def list_to_path(listIn:list):
        strOut=""
        for i in range(len(listIn)-1):
            strOut+=(listIn[i]+"->")
        strOut+=listIn[len(listIn)-1]
        return strOut

    @staticmethod
    def list_to_string(listIn):
        """transforms a labels list into a string, useful to initialize the Signal_information variable of create_dataframe"""
        strOut=""
        for nodo in listIn:
            strOut+=nodo
        return strOut

    @staticmethod
    def path_to_list(path:str):
        toReturn=[]
        [toReturn.append(label) for label in path.split('->')]
        return toReturn

    def create_dataframe(self):
        """Creates a pandas dataframe associating every possible path in the net with its latency, noise and SNR"""
        """data={'apples':[3,2,0,1],'oranges':[0,3,7,2]}
        purchases=pandas.DataFrame(data,index=['June','Robert','Lily','David'])
        print(purchases.to_string())"""
        initial_power=1e-3
        data={"latency":[],"noise":[],"SNR":[]}
        data2={}
        [data2.update({i:[]}) for i in range(NUMBER_OF_CHANNELS)]
        indexes=[]
        for nodo1 in self._nodes.values():
            for nodo2 in self._nodes.values():
                if nodo1==nodo2:
                    indexes.append(nodo1._label)
                    data["latency"].append(0)
                    data["noise"].append(0)
                    data["SNR"].append(0)
                    [data2[i].append(1) for i in range(NUMBER_OF_CHANNELS)]
                else:
                    for percorso in self.find_paths(nodo1._label,nodo2._label):
                        indexes.append(self.list_to_path(percorso))
                        #sig=Signal_information(initial_power,self.list_to_string(percorso))
                        sig = Signal_information(initial_power, percorso)
                        self.propagate(sig,-1)
                        data["latency"].append(sig.latency)
                        data["noise"].append(sig._noise_power)
                        #data["SNR"].append(10*math.log((sig.signal_power/sig._noise_power),math.e))
                        data["SNR"].append(sig.calculateSNR())
                        [data2[i].append(1) for i in range(NUMBER_OF_CHANNELS)]
        purchases=pandas.DataFrame(data,indexes)
        self._route_space=pandas.DataFrame(data2,indexes)
        return purchases

    def available_path(self,pathAsList:list):
        """
        :param pathAsList: the path you want to cross (passed as list of crossed nodes' labels)
        :return: a boolean value indicating whether there is a free channel for the given path or not
        """

        #Old implementation with single-channel lines:
        # for i in range(len(pathAsList)-1):
        #     if self._lines[pathAsList[i]+pathAsList[i+1]].state==0:
        #         return False
        # return True

        path=self.list_to_path(pathAsList)
        for i in range(NUMBER_OF_CHANNELS):
            if self._route_space.loc[path][i]==1:
                return True
        return False    #we get to this point only if no free channel is found

    def find_best_snr(self,n1: str ,n2: str):
        """
        :param n1: start node label
        :param n2: end node label
        :return: path (as a string) giving the highest SNR (the string will be empty if no available path is found)
        """

        #NOTES ON HOW TO MANAGE PANDAS DATAFRAMES
        #net._weighted_paths.index #returns all indexes
        #net._weighted_paths.loc[label][columnName] #returns the value at label row and columnName column
        #net._weighted_paths.loc['A->B']  #returns information about the row with 'A->B' index
        bestPath=""
        biggestSNR=0.0
        for label in self._weighted_paths.index:    #label will be a string like "A->B->C"
            if label[0]==n1 and label[len(label)-1]==n2:
                if self.available_path(self.path_to_list(label)): #checks if all lines in the path are free
                    newSNR = self._weighted_paths.loc[label]['SNR']
                    if newSNR>biggestSNR:
                        biggestSNR=newSNR
                        bestPath=copy.copy(label)
        return bestPath

    def find_best_latency(self, n1:str, n2:str):
        """
        :param n1: start node
        :param n2: end node
        :return: the path in the form "A->B->..." giving the lowest latency (the string will be empty if no available path is found)
        """

        bestPath=""
        lowestLatency=sys.maxsize
        for label in self._weighted_paths.index:
            if label[0]==n1 and label[len(label)-1]==n2:
                if self.available_path(self.path_to_list(label)):  #checks if all lines in the path are free
                    newLatency=self._weighted_paths.loc[label]['latency']
                    if newLatency<lowestLatency:
                        lowestLatency=newLatency
                        bestPath=copy.copy(label)
        return bestPath

    def occupy_path(self,path:list,channelIndex:int):
        """Sets as occupied all lines in the given path

        :param path: the list of the crossed nodes' labels
        :param channelIndex: index of the channel to occcupy in every line of the path
        """
        for i in range(len(path) - 1):  #iterates on every line in the path
            #self._lines[path[i]+path[i+1]].state[channelIndex]=0
            self._lines[path[i] + path[i + 1]].occupy(channelIndex)
            for label in self._route_space.index:
                if path[i]+"->"+path[i+1] in label:
                    self._route_space.loc[label][channelIndex]=0

    def free_all_lines(self):
        """Sets every line as free: useful if called at the end of stream, it allows to perform a new simulation"""
        for linea in self._lines.values():
            linea.freeAllChannels()

    def first_free_channel(self,path:str):
        """:param path: a path in the form "A->B->..."
        :return: the index of the first free channel available in the given path"""
        for i in range(NUMBER_OF_CHANNELS):
            if self._route_space.loc[path][i]==1:
                return i
        return -1   #this line should never be reached, since we
        #assume that this method only gets called upon paths with at least one free channel

    def stream(self,connections:list,choice:str="latency"):
        """
        Updates every connection in the list setting its latency and SNR to the
        ones it would have if it crossed the path giving the best latency/snr

        :param connections: list of Connection objects
        :param choice: indicates if the chosen path has to give the highest snr or the lowest latency
        """
        if choice == "latency":
            for conn in connections:
                bestPath=self.find_best_latency(conn.input,conn.output)
                if bestPath=="":
                    conn.snr=0
                    conn.latency=None
                else:
                    newPath=self.path_to_list(bestPath)
                    sigInf=Signal_information(conn.signal_power,newPath)
                    chann = self.first_free_channel(bestPath)
                    self.propagate(sigInf,chann)
                    conn.latency=sigInf.latency
                    conn.snr=sigInf.calculateSNR()
            self.free_all_lines()
        elif choice == "snr":
            for conn in connections:
                bestPath=self.find_best_snr(conn.input,conn.output)
                if bestPath == "":   #if no path is available, default values are set
                    conn.snr=0
                    conn.latency=None
                else:
                    bitrate=self.calculate_bit_rate(bestPath,self._nodes[bestPath[0]].transceiver)
                    if bitrate==0:
                        conn.snr=0
                        conn.latency=None
                    else:
                        newPath=self.path_to_list(bestPath)
                        sigInf=Signal_information(conn.signal_power,newPath)
                        chann = self.first_free_channel(bestPath)
                        self.propagate(sigInf,chann)
                        conn.latency=sigInf.latency
                        conn.snr=sigInf.calculateSNR()
                    conn.bit_rate=bitrate
            #print(self._route_space.to_string())
            self.free_all_lines()
        else:
            print("Choice must be \"latency\" or \"snr\"")

    def calculate_bit_rate(self,path:str,strategy:str):
        """
        Evaluates the bit rate supported by a specific path

        :param path: the path to examine
        :param strategy: a string among "fixed_rate", "flex_rate" and "shannon" (any other string will be rejected)
        :return: the bit rate in Gbps supported by the path
        """
        gsnr=db2nu(self._weighted_paths.loc[path]["SNR"])
        if strategy=="fixed_rate":
            if gsnr>=2*(spsp.erfcinv(2*BERt)**2)*Rs/Bn:
                return 100e9
            else:
                return 0
        elif strategy=="flex_rate":
            if gsnr>=10*(spsp.erfcinv((8/3)*BERt)**2)*(Rs/Bn):   #0.000143
                return 400e9
            elif gsnr>=(14/3)*(spsp.erfcinv((3/2)*BERt)**2)*(Rs/Bn):   #2.11e-5
                return 200e9
            elif gsnr>=2*(spsp.erfcinv(2*BERt)**2)*(Rs/Bn):    #1.61e-5
                return 100e9
            else:
                return 0
        elif strategy=="shannon":
            #return 2*Rs*math.log(1+gsnr*Bn/Rs,2)*1e9
            return 2*Rs*math.log(1+gsnr*Bn/Rs, 2)
        else:
            print("Strategy must be fixed_rate, flex_rate or shannon\n")
            toReturn=-1
        return toReturn