from networkLayer import Network

class Router(Network):
    def __init__(self, id, posX, posY):
        self.id = id
        self.position = [posX,posY]
        self.neighbors = []
        self.routes = {self.id:self.id}
        self.busy_tone = 0
        self.pkg_buffer = []
        self.rreq_buffer = []
        self.rrep_buffer = []
        
