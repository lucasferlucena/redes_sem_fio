import time
import copy
from physcalLayer import Physical

class DataLink(Physical):
    def mediumAccessControl(self, pkg, nos):
        while(True):
            bToneNeighbors = 0
            for neighbor in nos[pkg.dl_header[0]].neighbors:
                bToneNeighbors += nos[neighbor.id].busy_tone
            
            if bToneNeighbors:
                print("canal ocupado")
                time.sleep(2)               #TODO esperar tempo aleatorio
            else:
                print("canal liberado" + str(pkg.rec_node))
                for neighbor in nos[pkg.dl_header[0]].neighbors:
                    pkg_send = copy.deepcopy(pkg)
                    pkg_send.rec_node = neighbor.id 
                    nos[pkg.rec_node].dataLinkSend(pkg_send, nos)
                break
        pass

    def dataLinkSend(self, pkg, nos):
        nos[pkg.rec_node].busy_tone = 1
        super().send(pkg, nos)
        
        pass

    def dataLiknkReceive(self, pkg, nos):
        nos[pkg.rec_node].busy_tone = 0
        print(pkg.data)
        if(pkg.rec_node == pkg.dl_header[1] or pkg.dl_header[1] == -1):
            nos[pkg.rec_node].networkReceive(pkg, nos)
        pass