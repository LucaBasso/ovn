import copy
import math


class Signal_information:

    def __init__(self,sigPow:float,nodes:list):
        self._path=[]
        self._signal_power=sigPow
        self._noise_power=0.0
        self._latency=0.0
        [self._path.append(stringa) for stringa in nodes]
        self._constant_path=copy.copy(self._path)
        """for stringa in nodes:
            self._path.append(stringa)"""

    @property
    def signal_power(self):
        return self._signal_power

    def update_signal_power(self,increment):
        self._signal_power+=increment

    def update_noise(self,noiseIn):
        self._noise_power+=noiseIn

    @property
    def latency(self):
        return self._latency

    def update_latency(self,increment):
        self._latency+=increment

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,nodes):
        [self._path.append(nodo) for nodo in nodes]
        [self._path.append(nodo) for nodo in nodes]
        self._constant_path=copy.copy(self._path)

    def updatePath(self,crossedNode):
        self._path.remove(crossedNode)

    def calculateSNR(self):
        return 10*math.log((self._signal_power/self._noise_power),10)

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def constant_path(self):
        return self._constant_path


class Connection:
    """
    Class representing a lightpath between two nodes
    """

    def __init__(self,inp:str,out:str,sigPow:float,path=""):
        self._input=copy.copy(inp)
        self._output=copy.copy(out)
        self._signal_power=sigPow
        self._latency=0.0
        self._snr=0.0
        self._bit_rate=0
        self.max_bit_rate=0
        self.path=path

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self,newVal:float):
        self._latency=newVal

    @property
    def snr(self):
        return self._snr

    @snr.setter
    def snr(self,newVal:float):
        self._snr=newVal

    @property
    def bit_rate(self):
        return self._bit_rate

    @bit_rate.setter
    def bit_rate(self,newVal:float):
        self._bit_rate=newVal


class Lightpath(Signal_information):

    def __init__(self, sigPow: float, nodes: list, newChannel: int = 0):
        super().__init__(sigPow, nodes)
        self._channel=newChannel
        self._Rs=0
        self._df=0

    @property
    def channel(self):
        return self._channel

    # @property
    # def path(self):
    #     return self._path
