class Physical():
    def send(self, pkg, nos):
        print("nivel fisico")
        print("Pacote " + str(pkg.id)+ "do tipo "+str(pkg.type)+ "enviado do no " +str(nos[pkg.dl_header[0]].id)+" para no "+str(nos[pkg.rec_node].id))
        nos[pkg.rec_node].receive(pkg,nos)
        pass

    def receive(self, pkg, nos):
        nos[pkg.rec_node].dataLiknkReceive(pkg, nos)
        pass
