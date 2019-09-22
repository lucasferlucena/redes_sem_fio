class Package():
    id_rrep = 0
    id_rreq = 0
    def __init__(self, id, origem, destino, dado, pkg_type):
        self.id = id
        self.data = dado
        self.net_header = [origem, destino]
        self.dl_header = [origem, -1]
        self.type = pkg_type
        self.rec_node = origem