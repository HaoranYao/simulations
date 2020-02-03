


class Packet():
    ip_src = None
    ip_dst = None
    tcp_src = None
    tcp_dst = None

    def __init__(self, ip_src, ip_dst, tcp_src, tcp_dst):
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.tcp_src = tcp_src
        self.tcp_dst = tcp_dst

    def getHeader(self):
        return str(self.ip_src) +  str(self.ip_dst) +  str(self.tcp_src) +  str(self.tcp_dst)

    def getHash(self):
        return hash(str(self.ip_src) +  str(self.ip_dst) +  str(self.tcp_src) +  str(self.tcp_dst))