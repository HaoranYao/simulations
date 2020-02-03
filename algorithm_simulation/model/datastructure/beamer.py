import os
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.insert(0, dir_path)

from lb_data_structure import LBDataStructure
from model.packet import Packet

class Beamer(LBDataStructure):
    buckets = []

    def __init__(self, num_of_servers, buckets_factor):
        buckets = [-1] * (num_of_servers * buckets_factor)

    def getNextHop(self, packet):
        return self.buckets[packet.getHash() % len(self.buckets)]
