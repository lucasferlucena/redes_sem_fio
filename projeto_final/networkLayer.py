from datalinkLayer import DataLink
from scipy.spatial import distance
import package as pk
import copy
import logging

class Network(DataLink):
    def findNeighbors(self, id, nos):
        for no in nos:
            if (distance.seuclidean(nos[id].position, no.position, [1, 1]) <= 1.5) and (nos[id].position is not no.position):
                nos[id].neighbors.append(no)
        pass


    def networkSend(self, pkg, nos):
        pkg_send = copy.deepcopy(pkg)
        if pkg_send.dsr[0] == -1:
            if nos[pkg_send.rec_node].routes.get(pkg_send.net_header[1]) is None:
                logging.info("Processo de descobrimento de rota iniciado pela nó["+str(pkg.net_header[0])+"] para o nó["+str(pkg.net_header[1])+"]")
                nos[pkg_send.rec_node].routeRequest(nos, pkg_send)
                pkg_send.dsr = nos[pkg_send.rec_node].routes.get(pkg_send.net_header[1])
            else:
                pkg_send.dsr = nos[pkg_send.rec_node].routes.get(pkg_send.net_header[1])
        pkg_send.dl_header = [pkg_send.dsr[0], pkg_send.dsr[1]]
        pkg_send.dsr.pop(0)
        super().mediumAccessControl(pkg_send, nos)
        pass

    def networkReceive(self, pkg, nos):
        logging.info("Pacote["+str(pkg.id)+"]["+str(pkg.type)+"] dado:["+str(pkg.data)+"] originario do nó "+str(pkg.dl_header[0])+" recebido pelo nó "+str(pkg.rec_node))
        if(pkg.type == "DATA"):
            if(pkg.rec_node == pkg.net_header[1]):
                logging.info("Pacote["+str(pkg.id)+"]["+str(pkg.type)+"]chegou ao destino final "+str(pkg.rec_node))
                pass                                                                              #pacote de dado chegou ao destino final
            else:
                nos[pkg.rec_node].networkSend(pkg, nos)

        if((pkg.type == "RREQ") and not(pkg.id in nos[pkg.rec_node].rreq_buffer)):
            nos[pkg.rec_node].rreq_buffer.append(pkg.id)
            pkg_cpy = copy.deepcopy(pkg)
            pkg_cpy.data.append(pkg.rec_node)
            data_cpy = copy.deepcopy(pkg_cpy.data)
            nos[pkg.rec_node].fillTable(nos, pkg_cpy)
            if(pkg.rec_node == pkg.net_header[1]):  
                data_cpy.reverse()
                rrep = pk.Package(pkg.id, pkg.net_header[1], pkg.net_header[0], data_cpy, "RREP")
                rrep.dsr = copy.deepcopy(data_cpy)
                nos[pkg.rec_node].networkSend(rrep, nos)                                          #envia rrep
            else:
                pkg_cpy.dl_header = [pkg.rec_node, -1]
                nos[pkg.rec_node].rreq_buffer.append(pkg.id)
                super().mediumAccessControl(pkg_cpy, nos)                                         #reenvia rreq
                
        if(pkg.type == "RREP" and not(pkg.id in nos[pkg.rec_node].rrep_buffer)):
            nos[pkg.rec_node].fillTable(nos, pkg)
            nos[pkg.rec_node].rrep_buffer.append(pkg.id)
            if(pkg.rec_node == pkg.net_header[1]):
                pass                                                                              #apos a execuçao do dsr, eniva o pacote inicial que está no buffer
            else:
                nos[pkg.rec_node].networkSend(pkg, nos)                                           #reenvia rrep
        pass
    
    def routeRequest(self, nos, pkg):    
        dado = [pkg.net_header[0]]
        pk.Package.id_rreq = pk.Package.id_rreq + 1
        rreq = pk.Package(pk.Package.id_rreq, pkg.net_header[0], pkg.net_header[1], dado, "RREQ")    
        nos[pkg.net_header[0]].rreq_buffer.append(rreq.id)                                    
        super().mediumAccessControl(rreq, nos)                                                                                               #envia rreq
        pass

    def fillTable(self, nos, pkg):
        node_index = pkg.data.index(nos[pkg.rec_node].id)
        pkg_copy = copy.deepcopy(pkg.data)
        
        #caminho adquirido com o RREQ
        leftPath = pkg_copy[:node_index+1]
        leftPath.reverse()
        if node_index != 0:
            for i in range(1,len(leftPath)):
                if nos[pkg.rec_node].routes.get(leftPath[i]) is None:
                    nos[pkg.rec_node].routes[leftPath[i]] = leftPath[:i+1]
                elif len(nos[pkg.rec_node].routes[leftPath[i]]) > len(leftPath[:i+1]):
                    nos[pkg.rec_node].routes[leftPath[i]] = leftPath[:i+1]

        #caminho adquirido com o RREP
        rightPath = pkg_copy[node_index:]
        if node_index != (len(pkg.data) - 1):
            for i in range(1,len(rightPath)):
                if nos[pkg.rec_node].routes.get(rightPath[i]) is None:
                    nos[pkg.rec_node].routes[rightPath[i]] = rightPath[:i+1]
                elif len(nos[pkg.rec_node].routes[rightPath[i]]) > len(rightPath[:i+1]):
                    nos[pkg.rec_node].routes[rightPath[i]] = rightPath[:i+1]        

        logging.info("Rotas do nó "+str(pkg.rec_node)+": "+str(nos[pkg.rec_node].routes))
        pass