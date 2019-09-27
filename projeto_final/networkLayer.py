from datalinkLayer import DataLink
from scipy.spatial import distance
import package as pk
import copy

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
                print("nao tem na tabela")
                nos[pkg_send.rec_node].routeRequest(nos, pkg_send)
                print("enviar dado")
                pkg_send.dsr = nos[pkg_send.rec_node].routes.get(pkg_send.net_header[1])
            else:
                print("tem na tabela")
                pkg_send.dsr = nos[pkg_send.rec_node].routes.get(pkg_send.net_header[1])
        pkg_send.dl_header = [pkg_send.dsr[0], pkg_send.dsr[1]]
        pkg_send.dsr.pop(0)
        super().mediumAccessControl(pkg_send, nos)
        pass

    def networkReceive(self, pkg, nos):
        print(str(pkg.type+" aqui?? " + str(pkg.id) +"  "+str(pkg.rec_node)+"  "+str(nos[pkg.rec_node].rreq_buffer))+" " +str(pkg.net_header[1]))
        if(pkg.type == "DATA"):
            if(pkg.rec_node == pkg.net_header[1]):
                print("O pacote "+str(pkg.id)+" chegou ao destino "+str(pkg.net_header[1]))
            else:
                nos[pkg.rec_node].networkSend(pkg, nos)

        if((pkg.type == "RREQ") and not(pkg.id in nos[pkg.rec_node].rreq_buffer)):
            print("aqui ne")
            pkg_cpy = copy.deepcopy(pkg)
            pkg_cpy.data.append(pkg.rec_node)
            data_cpy = copy.deepcopy(pkg_cpy.data)
            nos[pkg.rec_node].fillTable(nos, pkg_cpy)
            if(pkg.rec_node == pkg.net_header[1]):  
                print("o 8 deve entrar aq")
                data_cpy.reverse()
                rrep = pk.Package(pkg.id, pkg.net_header[1], pkg.net_header[0], data_cpy, "RREP")
                rrep.dsr = copy.deepcopy(data_cpy)
                nos[pkg.rec_node].rrep_buffer.append(rrep.id)
                print("pacote RREP: ")
                nos[pkg.rec_node].networkSend(rrep, nos)                                                                                    #envia rrep
            else:
                print("dps aq")
                pkg_cpy.dl_header = [pkg.rec_node, -1]
                nos[pkg.rec_node].rreq_buffer.append(pkg.id)
                print(str(pkg_cpy.dl_header)+ " " +str(pkg.rec_node))
                super().mediumAccessControl(pkg_cpy, nos)                                                                                   #reenvia rreq
                
        if(pkg.type == "RREP" and not(pkg.id in nos[pkg.rec_node].rrep_buffer)):
            print("aqui??")
            nos[pkg.rec_node].fillTable(nos, pkg)
            if(pkg.rec_node == pkg.net_header[1]):
                print(pkg.data)
                #nos[pkg.rec_node].networkSend(nos[pkg.rec_node].pkg_buffer[-1], nos)                                                        #apos a execuçao do aodv, eniva o pacote inicial que está no buffer
            else:
                nos[pkg.rec_node].rrep_buffer.append(pkg.id)
                nos[pkg.rec_node].networkSend(pkg, nos)                                                                                     #reenvia rrep
        pass
    
    def routeRequest(self, nos, pkg):    
        print("route request de " +str(pkg.net_header[0]) + " "+str(nos[pkg.net_header[0]].rreq_buffer))
        dado = [pkg.net_header[0]]
        pk.Package.id_rreq = pk.Package.id_rreq + 1
        rreq = pk.Package(pk.Package.id_rreq, pkg.net_header[0], pkg.net_header[1], dado, "RREQ")    
        nos[pkg.net_header[0]].rreq_buffer.append(rreq.id)
        nos[pkg.net_header[0]].pkg_buffer.append(pkg)                                          
        super().mediumAccessControl(rreq, nos)                                                                                               #envia rreq
        pass

    def fillTable(self, nos, pkg):
        node_index = pkg.data.index(nos[pkg.rec_node].id)
        pkg_copy = copy.deepcopy(pkg.data)
        
        print(node_index)

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

        print(nos[pkg.rec_node].routes)
        
        pass