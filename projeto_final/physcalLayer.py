class Physical():
    def send(self, pkg, nos): 
        nos[pkg.rec_node].receive(pkg,nos)
        pass

    def receive(self, pkg, nos):
        nos[pkg.rec_node].dataLiknkReceive(pkg, nos)
        pass
