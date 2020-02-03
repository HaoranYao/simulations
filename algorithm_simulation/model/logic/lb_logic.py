


class LBLogic(object):

    def __init__(self, args):
        self.number_of_servers = args.server_number
        self.server_dictionary = {x: [] for x in range(self.number_of_servers)}
        self.server_load = {x: 0 for x in range(self.number_of_servers)}
        self.connection_dictionary = {}
        self.number_of_servers = self.number_of_servers

    def addNewConnection(self, packet):
        pass

    def removeConnection(self, packet):
        pass

    def addServer(self):
        pass

    def removeServer(self, serverId):
        pass

    def pick_server(self):
        # Basic function! Return the first server!
        # Only pick the first server.
        return 0
